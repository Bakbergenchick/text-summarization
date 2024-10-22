import asyncio
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from text_analyzer import TextAnalyzer
from file_handler import extract_text_from_docx, extract_text_from_pdf

app = FastAPI()
templates = Jinja2Templates(directory="templates")
analyzer = TextAnalyzer()

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return templates.TemplateResponse("index.html", {"request": {}})

async def async_extract_text(file_ext, file):
    if file_ext == "docx":
        return await asyncio.to_thread(extract_text_from_docx, file)
    elif file_ext == "pdf":
        return await asyncio.to_thread(extract_text_from_pdf, file)
    else:
        return "Unsupported file type"

@app.post("/analyze")
async def analyze_text(file: UploadFile = File(...), length: str = Form("средняя")):
    file_ext = file.filename.split(".")[-1].lower()
    
    text = await async_extract_text(file_ext, file.file)
    
    if "Ошибка" in text:
        return {"error": text}

    async def analyze():
        # Анализ языка выполняется асинхронно
        language_task = asyncio.to_thread(analyzer.detect_language, text)
        
        # Асинхронная суммаризация
        summary_task = asyncio.to_thread(analyzer.summarize_text, text, length)
        
        # Асинхронное извлечение ключевых слов
        keywords_task = asyncio.to_thread(analyzer.extract_keywords, text)
        
        # Запуск всех задач параллельно
        language, summary, keywords = await asyncio.gather(language_task, summary_task, keywords_task)
        
        return {"language": language, "summary": summary, "keywords": keywords}

    return await analyze()
