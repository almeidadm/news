# Imagem base com Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências e instala
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o código do projeto para o container
COPY . .

# Comando padrão para executar o spider (substitua 'exemplo' pelo nome do seu spider, se necessário)
CMD  ["tail", "-f", "/dev/null"]
# ["scrapy", "crawl", "o_globo"]
