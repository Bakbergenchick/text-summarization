import asyncio
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from text_analyzer import TextAnalyzer
from ontology_handler import OntologyHandler
from file_handler import extract_text_from_docx, extract_text_from_pdf
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
analyzer = TextAnalyzer()
ontology_handler = OntologyHandler()

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
        
        # Обработка онтологии
        ontology_graph, ontology_formula = analyzer.process_ontology(keywords)
        
        return {"language": language, "summary": summary, "keywords": keywords, "ontology_formula": ontology_formula}

    return await analyze()

@app.get("/visualize_ontology")
async def visualize_ontology():
    graph_path = "data/ontology_graph.gml"
    if not os.path.exists(graph_path):
        return {"error": "Ontology graph not found. Please analyze a file first."}

    import networkx as nx
    import matplotlib.pyplot as plt
    import io
    
        # Чтение графа
    graph = nx.read_gml(graph_path)

    # Создание графика
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, font_size=12, font_weight="bold")
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels={(u, v): d["relation"] for u, v, d in graph.edges(data=True)}
    )

    # Сохранение графика в поток
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Используем StreamingResponse для передачи потока
    return StreamingResponse(buf, media_type="image/png")