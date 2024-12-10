import re
from langdetect import detect
from transformers import pipeline
from keybert import KeyBERT
from ontology_handler import OntologyHandler

class TextAnalyzer:
    def __init__(self):
        self.summarizer = pipeline("summarization")
        self.keyword_extractor = KeyBERT()
        self.ontology_handler = OntologyHandler()
    
    def detect_language(self, text):
        try:
            return detect(text)
        except Exception as e:
            return f"Ошибка при определении языка: {e}"

    def clean_text(self, text):
        # Удаление лишних символов, пробелов и специальных символов
        text = re.sub(r'\s+', ' ', text)  # Замена множества пробелов на один
        text = re.sub(r'[^\x00-\x7Fа-яА-Я]', '', text)  # Удаление не-ASCII символов, за исключением кириллицы
        return text.strip()

    def summarize_text(self, text, length="средняя"):
        max_chunk_size = 800
        text_chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

        summarized_text = []
        max_length = 50 if length == "краткая" else 100 if length == "средняя" else 200

        try:
            for chunk in text_chunks:
                # Проверка длины текста для корректной суммаризации
                adjusted_max_length = min(max_length, len(chunk) // 2)  # Уменьшаем max_length, если текст слишком короткий
                summary = self.summarizer(chunk, max_length=adjusted_max_length , min_length=30, do_sample=False)
                if summary and len(summary) > 0:
                    clean_summary = self.clean_text(summary[0]['summary_text'])  # Очистка итогового текста
                    summarized_text.append(clean_summary)

            return ' '.join(summarized_text)
        except Exception as e:
            return f"Ошибка при аннотировании текста: {e}"

    def extract_keywords(self, text, num_keywords=5):
        try:
            keywords = self.keyword_extractor.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=num_keywords)
            return [kw[0] for kw in keywords if kw]
        except Exception as e:
            return [f"Ошибка при извлечении ключевых слов: {e}"]
        
    def process_ontology(self, keywords):
        """
        Создание графа онтологии, генерация формулы и сохранение.
        """
        graph = self.ontology_handler.build_ontology(keywords)
        formula = self.ontology_handler.export_ontology_formula(graph)
        self.ontology_handler.save_ontology(graph, formula)
        return graph, formula
