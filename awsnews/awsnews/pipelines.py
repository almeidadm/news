# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import spacy
import sqlite3


class AwsnewsPipeline:
    def process_item(self, item, spider):
        return item

class SQLitePipeline:
    def open_spider(self, spider):
        """Executado quando o spider é iniciado."""
        self.connection = sqlite3.connect("news.db")  # Cria um arquivo SQLite chamado 'news.db'
        self.cursor = self.connection.cursor()
        
        # Criar a tabela se ela ainda não existir
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            article_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,  -- Garantir que URLs não sejam duplicadas
            date_published TEXT,
            author TEXT,
            summary TEXT,
            content TEXT,
            html_content TEXT,
            tags TEXT,
            section TEXT,
            comments_count INTEGER,
            image_urls TEXT,
            source TEXT,
            scraped_date TEXT,
            language TEXT,
            keywords TEXT
        )
        """)
        self.connection.commit()

    def close_spider(self, spider):
        """Executado quando o spider é encerrado."""
        self.connection.close()

    def process_item(self, item, spider):
        """Salva os itens no banco de dados."""
        try:
            self.cursor.execute("""
            INSERT INTO news (
                title, url, date_published, author, summary, content, html_content,
                tags, section, comments_count, image_urls, source, scraped_date, 
                language, keywords
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get('title'),
                item.get('url'),
                item.get('date_published'),
                item.get('author'),
                item.get('summary'),
                item.get('content'),
                item.get('html_content'),
                ','.join(item.get('tags', [])) if isinstance(item.get('tags'), list) else item.get('tags'),
                item.get('section'),
                item.get('comments_count'),
                ','.join(item.get('image_urls', [])) if isinstance(item.get('image_urls'), list) else item.get('image_urls'),
                item.get('source'),
                item.get('scraped_date'),
                item.get('language'),
                ','.join(item.get('keywords', [])) if isinstance(item.get('keywords'), list) else item.get('keywords')
            ))
            self.connection.commit()
        except sqlite3.IntegrityError:
            spider.logger.info(f"Duplicate entry found for URL: {item.get('url')}")
        
        return item



class KeywordExtractionPipeline:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    def process_item(self, item, spider):
        content = item.get("content")
        if content:
            doc = self.nlp(content)

            keywords = [ent.text for ent in doc.ents]

            if not keywords:
                keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]

            item["keywords"] = keywords
        
        return item
