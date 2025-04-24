# projeto_fastapi/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
from pathlib import Path

app = FastAPI()

# Define os caminhos para as pastas 'static' e 'templates'
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_FILE = BASE_DIR / "data" / "nucleos_com_coordenadas.json"

# Monta o diretório de arquivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Configura o Jinja2 para renderizar os templates HTML
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Função para carregar os dados dos núcleos do arquivo JSON
def carregar_nucleos():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo de dados não encontrado em {DATA_FILE}")
        return []
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar JSON do arquivo {DATA_FILE}")
        return []

# Rota para a página inicial
@app.get("/", response_class=None)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para a página de núcleos
@app.get("/nucleos", response_class=None)
async def nucleos_page(request: Request):
    nucleos = carregar_nucleos() 
    return templates.TemplateResponse("nucleos.html", {"request": request, "data": nucleos})


# Rota para a página de contatos (exemplo de página estática)
@app.get("/contatos", response_class=None)
async def contatos(request: Request):
    return templates.TemplateResponse("contatos.html", {"request": request})

# Rota para a página de eventos (exemplo de página estática)
@app.get("/eventos", response_class=None)
async def eventos(request: Request):
    return templates.TemplateResponse("eventos.html", {"request": request})

@app.get("/nucleo/{municipio}", response_class=None)
async def nucleo_detalhe(request: Request, municipio: str):
    nucleos = carregar_nucleos()
    municipio = municipio.replace('-', ' ') # Formata o nome do município
    nucleo_encontrado = None
    for nucleo in nucleos:
        print(nucleo)
        if nucleo.get('localizacao') and nucleo['localizacao'][-1].lower() == municipio.lower():
            nucleo_encontrado = nucleo
            break
    if nucleo_encontrado:
        return templates.TemplateResponse("nucleo.html", {"request": request, "nucleo": nucleo_encontrado})
    else:
        return RedirectResponse("/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)