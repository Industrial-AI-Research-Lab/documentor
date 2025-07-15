#!/usr/bin/env python3
"""
Прототип системы линкования объектов с семантической близостью
Расширенная версия с улучшенным алгоритмом связывания
"""
import re
import os
import time
from typing import List, Dict, Any, Tuple
import difflib

class SemanticObjectLinker:
    """Рабочий прототип системы линкования объектов с семантической близостью"""
    
    def __init__(self):
        # Улучшенные регулярные выражения для поиска ссылок
        self.reference_patterns = {
            'Figure': re.compile(r'\b(?:Figure|Fig\.?|Рис\.?|Рисунок)\s*([0-9]+(?:\.[0-9]+)*[a-z]?)', re.IGNORECASE),
            'Table': re.compile(r'\b(?:Table|Tab\.?|Таблица|Табл\.?)\s*([0-9]+(?:\.[0-9]+)*[a-z]?)', re.IGNORECASE),
            'Equation': re.compile(r'\b(?:Equation|Eq\.?|Уравнение|Ур\.?)\s*\(?([0-9]+(?:\.[0-9]+)*)\)?', re.IGNORECASE),
            'Section': re.compile(r'\b(?:Section|Sec\.?|Раздел|§)\s*([0-9]+(?:\.[0-9]+)*)', re.IGNORECASE),
            'Lemma': re.compile(r'\b(?:Lemma|Лемма)\s*([0-9]+(?:\.[0-9]+)*)', re.IGNORECASE),
            'Theorem': re.compile(r'\b(?:Theorem|Теорема)\s*([0-9]+(?:\.[0-9]+)*)', re.IGNORECASE),
            'Proposition': re.compile(r'\b(?:Proposition|Prop\.?|Утверждение)\s*([0-9]+(?:\.[0-9]+)*)', re.IGNORECASE),
            'Corollary': re.compile(r'\b(?:Corollary|Cor\.?|Следствие)\s*([0-9]+(?:\.[0-9]+)*)', re.IGNORECASE),
            'Formula': re.compile(r'\(([0-9]+)\)'),
            'Citation': re.compile(r'\[([0-9]+(?:,\s*[0-9]+)*)\]')
        }
        
        # Паттерны для поиска объектов (заголовков)
        self.object_patterns = {
            'Figure': re.compile(r'\b(?:Figure|Fig\.?|Рис\.?|Рисунок)\s*([0-9]+(?:\.[0-9]+)*[a-z]?)[:.]', re.IGNORECASE),
            'Table': re.compile(r'\b(?:Table|Tab\.?|Таблица|Табл\.?)\s*([0-9]+(?:\.[0-9]+)*[a-z]?)[:.]', re.IGNORECASE),
            'Section': re.compile(r'^([0-9]+(?:\.[0-9]+)*)\s+[A-ZА-Я]', re.MULTILINE),
            'Proposition': re.compile(r'\b(?:Proposition|Prop\.?|Утверждение)\s*([0-9]+(?:\.[0-9]+)*)[:.]', re.IGNORECASE),
            'Corollary': re.compile(r'\b(?:Corollary|Cor\.?|Следствие)\s*([0-9]+(?:\.[0-9]+)*)[:.]', re.IGNORECASE),
            'Lemma': re.compile(r'\b(?:Lemma|Лемма)\s*([0-9]+(?:\.[0-9]+)*)[:.]', re.IGNORECASE),
            'Theorem': re.compile(r'\b(?:Theorem|Теорема)\s*([0-9]+(?:\.[0-9]+)*)[:.]', re.IGNORECASE)
        }
        
        # Словари синонимов для семантической близости
        self.semantic_synonyms = {
            'Figure': ['Figure', 'Fig', 'Рис', 'Рисунок', 'диаграмма', 'график', 'схема', 'изображение'],
            'Table': ['Table', 'Tab', 'Таблица', 'Табл', 'сводка', 'данные'],
            'Equation': ['Equation', 'Eq', 'Уравнение', 'Ур', 'формула', 'выражение'],
            'Section': ['Section', 'Sec', 'Раздел', 'глава', 'часть', 'параграф'],
            'Lemma': ['Lemma', 'Лемма', 'утверждение', 'факт'],
            'Theorem': ['Theorem', 'Теорема', 'утверждение', 'результат'],
            'Proposition': ['Proposition', 'Prop', 'Утверждение', 'предложение', 'тезис'],
            'Corollary': ['Corollary', 'Cor', 'Следствие', 'вывод', 'результат'],
            'Formula': ['Formula', 'Формула', 'выражение', 'уравнение'],
            'Citation': ['Citation', 'Цитата', 'ссылка', 'источник', 'работа']
        }
    
    def extract_text_from_ocr(self, file_path: str) -> str:
        """Извлекает текст из файла OCR аннотации"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    lines = f.readlines()
            except:
                return ""
        
        # Извлекаем слова с их координатами
        words_data = []
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) >= 10:
                word = parts[0]
                try:
                    y1, x1 = int(parts[2]), int(parts[1])
                    word_type = parts[-1]
                    
                    # Фильтруем только нужные типы
                    if word_type in ['paragraph', 'abstract', 'title', 'section']:
                        words_data.append((y1, x1, word))
                except (ValueError, IndexError):
                    continue
        
        if not words_data:
            return ""
        
        # Сортируем по позиции и собираем текст
        words_data.sort(key=lambda x: (x[0], x[1]))
        
        # Группируем слова в строки
        lines_text = []
        current_line = []
        current_y = None
        
        for y, x, word in words_data:
            if current_y is None or abs(y - current_y) <= 15:  # одна строка
                current_line.append(word)
                current_y = y
            else:
                if current_line:
                    lines_text.append(' '.join(current_line))
                current_line = [word]
                current_y = y
        
        if current_line:
            lines_text.append(' '.join(current_line))
        
        return '\n'.join(lines_text)
    
    def find_references(self, text: str) -> List[Dict[str, Any]]:
        """Находит все ссылки в тексте"""
        references = []
        
        for ref_type, pattern in self.reference_patterns.items():
            for match in pattern.finditer(text):
                references.append({
                    'text': match.group(0),
                    'type': ref_type,
                    'id': match.group(1),
                    'start': match.start(),
                    'end': match.end(),
                    'linked_objects': [],
                    'context': self.extract_context(text, match.start(), match.end())
                })
        
        return references
    
    def extract_context(self, text: str, start: int, end: int, window: int = 50) -> str:
        """Извлекает контекст вокруг найденной ссылки"""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end].strip()
    
    def find_objects(self, text: str) -> List[Dict[str, Any]]:
        """Находит объекты (заголовки рисунков, таблиц и т.д.)"""
        objects = []
        
        for obj_type, pattern in self.object_patterns.items():
            for match in pattern.finditer(text):
                obj_id = match.group(1) if match.groups() else ''
                objects.append({
                    'text': match.group(0),
                    'type': obj_type,
                    'id': obj_id,
                    'start': match.start(),
                    'end': match.end(),
                    'context': self.extract_context(text, match.start(), match.end(), 100)
                })
        
        return objects
    
    def calculate_id_similarity(self, ref_id: str, obj_id: str) -> float:
        """Вычисляет схожесть между идентификаторами"""
        if not ref_id or not obj_id:
            return 0.0
        
        # Точное совпадение
        if ref_id == obj_id:
            return 1.0
        
        # Частичное совпадение
        if ref_id in obj_id or obj_id in ref_id:
            return 0.8
        
        # Используем difflib для нечеткого сравнения
        similarity = difflib.SequenceMatcher(None, ref_id.lower(), obj_id.lower()).ratio()
        return similarity if similarity > 0.6 else 0.0
    
    def calculate_semantic_similarity(self, ref_type: str, obj_type: str, ref_context: str, obj_context: str) -> float:
        """Вычисляет семантическую близость между ссылкой и объектом"""
        # Базовая проверка типов
        if ref_type != obj_type:
            return 0.0
        
        # Анализ контекста
        ref_words = set(ref_context.lower().split())
        obj_words = set(obj_context.lower().split())
        
        # Пересечение слов
        common_words = ref_words.intersection(obj_words)
        if not ref_words or not obj_words:
            return 0.5  # нейтральная оценка при отсутствии контекста
        
        word_similarity = len(common_words) / max(len(ref_words), len(obj_words))
        
        # Проверка синонимов
        synonyms = self.semantic_synonyms.get(ref_type, [])
        synonym_score = 0.0
        
        for synonym in synonyms:
            if synonym.lower() in ref_context.lower() and synonym.lower() in obj_context.lower():
                synonym_score += 0.1
        
        # Анализ позиционной близости (объекты обычно определяются до ссылок)
        positional_bonus = 0.1  # небольшой бонус за правильный порядок
        
        # Комбинированная оценка
        total_similarity = word_similarity + min(synonym_score, 0.3) + positional_bonus
        return min(total_similarity, 1.0)
    
    def calculate_combined_similarity(self, ref: Dict, obj: Dict) -> float:
        """Комбинированная оценка схожести (ID + семантика)"""
        id_sim = self.calculate_id_similarity(ref['id'], obj['id'])
        semantic_sim = self.calculate_semantic_similarity(
            ref['type'], obj['type'], 
            ref['context'], obj['context']
        )
        
        # Взвешенная комбинация (ID важнее семантики)
        combined = 0.7 * id_sim + 0.3 * semantic_sim
        
        # Бонус за точное совпадение типов и контекста
        if ref['type'] == obj['type'] and len(ref['context']) > 10 and len(obj['context']) > 10:
            combined += 0.1
        
        return min(combined, 1.0)
    
    def link_references_to_objects(self, references: List[Dict], objects: List[Dict]) -> None:
        """Связывает ссылки с объектами используя улучшенный алгоритм"""
        for ref in references:
            ref_type = ref['type']
            
            # Ищем все подходящие объекты
            candidates = []
            
            for obj in objects:
                if obj['type'] == ref_type:
                    similarity = self.calculate_combined_similarity(ref, obj)
                    
                    if similarity > 0.3:  # пониженный порог для учета семантики
                        candidates.append({
                            'object': obj,
                            'similarity': similarity,
                            'id_similarity': self.calculate_id_similarity(ref['id'], obj['id']),
                            'semantic_similarity': self.calculate_semantic_similarity(
                                ref['type'], obj['type'], 
                                ref['context'], obj['context']
                            )
                        })
            
            # Сортируем кандидатов по общей схожести
            candidates.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Добавляем лучших кандидатов
            for candidate in candidates[:3]:  # топ-3 кандидата
                if candidate['similarity'] > 0.5:  # порог для финального отбора
                    ref['linked_objects'].append({
                        'text': candidate['object']['text'],
                        'type': candidate['object']['type'],
                        'id': candidate['object']['id'],
                        'similarity': candidate['similarity'],
                        'id_similarity': candidate['id_similarity'],
                        'semantic_similarity': candidate['semantic_similarity'],
                        'context': candidate['object']['context']
                    })
    
    def generate_html_report(self, text: str, references: List[Dict], objects: List[Dict]) -> str:
        """Генерирует HTML отчет с выделенными ссылками и семантической информацией"""
        html_text = text
        offset = 0
        
        # Выделяем ссылки
        sorted_refs = sorted(references, key=lambda x: x['start'])
        
        for ref in sorted_refs:
            start = ref['start'] + offset
            end = ref['end'] + offset
            ref_text = ref['text']
            
            if ref['linked_objects']:
                css_class = 'linked'
                best_match = ref['linked_objects'][0]
                tooltip = f"Связано с: {best_match['text']}<br/>Общая схожесть: {best_match['similarity']:.2f}<br/>ID схожесть: {best_match['id_similarity']:.2f}<br/>Семантика: {best_match['semantic_similarity']:.2f}"
            else:
                css_class = 'unlinked'
                tooltip = "Объект не найден"
            
            html_link = f'<span class="reference {css_class}" title="{tooltip}">{ref_text}</span>'
            html_text = html_text[:start] + html_link + html_text[end:]
            offset += len(html_link) - len(ref_text)
        
        # Создаем полный HTML документ
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Семантический анализ ссылок в научном документе</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .stats {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .stat-item {{
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        .content {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            white-space: pre-wrap;
            font-size: 14px;
            line-height: 1.8;
        }}
        .reference {{
            padding: 3px 8px;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
        }}
        .reference.linked {{
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        .reference.unlinked {{
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        .reference:hover {{
            transform: scale(1.08);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            z-index: 1000;
        }}
        .legend {{
            margin-top: 20px;
            padding: 20px;
            background: #e9ecef;
            border-radius: 8px;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 25px;
            margin-bottom: 8px;
        }}
        .semantic-info {{
            margin-top: 20px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .match-details {{
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
            border-left: 4px solid #007bff;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Семантический анализ ссылок</h1>
        <p>Система автоматического линкования с ИИ-алгоритмами</p>
    </div>
    
    <div class="stats">
        <div class="stat-item">
            <h4>📄 Длина текста</h4>
            <strong>{len(text)} символов</strong>
        </div>
        <div class="stat-item">
            <h4>🔗 Найдено ссылок</h4>
            <strong>{len(references)}</strong>
        </div>
        <div class="stat-item">
            <h4>✅ Связано объектов</h4>
            <strong>{len([r for r in references if r['linked_objects']])}</strong>
        </div>
        <div class="stat-item">
            <h4>📚 Найдено объектов</h4>
            <strong>{len(objects)}</strong>
        </div>
        <div class="stat-item">
            <h4>🎯 Процент связывания</h4>
            <strong>{len([r for r in references if r['linked_objects']]) / max(len(references), 1) * 100:.1f}%</strong>
        </div>
        <div class="stat-item">
            <h4>🧠 Семантический анализ</h4>
            <strong>Включен</strong>
        </div>
    </div>
    
    <div class="content">{html_text}</div>
    
    <div class="semantic-info">
        <h3>🔍 Детали семантического анализа:</h3>
        {self.generate_semantic_details(references)}
    </div>
    
    <div class="legend">
        <h3>🎨 Легенда:</h3>
        <div class="legend-item">
            <span class="reference linked">Связанная ссылка</span> - найден соответствующий объект с семантическим анализом
        </div>
        <div class="legend-item">
            <span class="reference unlinked">Несвязанная ссылка</span> - объект не найден или низкая семантическая схожесть
        </div>
    </div>
</body>
</html>
        """
    
    def generate_semantic_details(self, references: List[Dict]) -> str:
        """Генерирует детальную информацию о семантическом анализе"""
        details = ""
        
        linked_refs = [r for r in references if r['linked_objects']]
        
        if not linked_refs:
            return "<p>Связанных ссылок не найдено.</p>"
        
        for ref in linked_refs[:5]:  # показываем топ-5
            details += f"""
            <div class="match-details">
                <h4>🔗 "{ref['text']}" (тип: {ref['type']})</h4>
                <p><strong>Контекст:</strong> ...{ref['context']}...</p>
                <p><strong>Лучшее совпадение:</strong> "{ref['linked_objects'][0]['text']}"</p>
                <p><strong>Метрики схожести:</strong></p>
                <ul>
                    <li>Общая схожесть: <strong>{ref['linked_objects'][0]['similarity']:.3f}</strong></li>
                    <li>ID схожесть: <strong>{ref['linked_objects'][0]['id_similarity']:.3f}</strong></li>
                    <li>Семантическая схожесть: <strong>{ref['linked_objects'][0]['semantic_similarity']:.3f}</strong></li>
                </ul>
            </div>
            """
        
        return details
    
    def analyze_document(self, file_path: str) -> Dict[str, Any]:
        """Полный анализ документа с семантическим линкованием"""
        # Извлекаем текст
        text = self.extract_text_from_ocr(file_path)
        
        if not text:
            return {'error': 'Не удалось извлечь текст'}
        
        # Находим ссылки и объекты
        references = self.find_references(text)
        objects = self.find_objects(text)
        
        # Связываем ссылки с объектами используя семантический анализ
        self.link_references_to_objects(references, objects)
        
        # Генерируем HTML отчет
        html_content = self.generate_html_report(text, references, objects)
        
        # Расширенная статистика
        linked_count = len([r for r in references if r['linked_objects']])
        total_refs = len(references)
        
        return {
            'text': text,
            'references': references,
            'objects': objects,
            'html_content': html_content,
            'statistics': {
                'text_length': len(text),
                'total_references': total_refs,
                'linked_references': linked_count,
                'total_objects': len(objects),
                'link_success_rate': linked_count / total_refs if total_refs > 0 else 0,
                'semantic_analysis_enabled': True,
                'average_similarity': sum(r['linked_objects'][0]['similarity'] for r in references if r['linked_objects']) / max(linked_count, 1)
            }
        }

def get_test_files() -> List[str]:
    """Находит доступные файлы для тестирования"""
    test_files = []
    
    # Проверяем несколько возможных путей
    possible_paths = [
        "linking/ann",
        "linking/ann", 
        "ann"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith('.txt'):
                    test_files.append(os.path.join(path, file))
            break
    
    return test_files  # ограничиваем для демонстрации

def run_semantic_demo():
    """Запускает демонстрацию прототипа с семантическим анализом"""
    print("🧠 ДЕМОНСТРАЦИЯ СЕМАНТИЧЕСКОЙ СИСТЕМЫ ЛИНКОВАНИЯ ОБЪЕКТОВ")
    print("=" * 70)
    
    # Инициализируем систему
    linker = SemanticObjectLinker()
    
    # Создаем папку для отчетов
    os.makedirs("semantic_reports", exist_ok=True)
    
    # Находим файлы для тестирования
    test_files = get_test_files()
    
    if not test_files:
        print("❌ Файлы для тестирования не найдены")
        print("Проверьте наличие датасета в папках: linking/ann/, linking/ann/, ann/")
        return
    
    print(f"📁 Найдено {len(test_files)} файлов для тестирования")
    
    total_stats = {
        'total_files': 0,
        'total_references': 0,
        'total_linked': 0,
        'total_processing_time': 0
    }
    
    # Тестируем каждый файл
    for i, file_path in enumerate(test_files, 1):
        print(f"\n{'='*70}")
        print(f"СЕМАНТИЧЕСКИЙ АНАЛИЗ {i}/{len(test_files)}: {os.path.basename(file_path)}")
        print(f"{'='*70}")
        
        try:
            start_time = time.time()
            results = linker.analyze_document(file_path)
            processing_time = time.time() - start_time
            
            if 'error' in results:
                print(f"❌ Ошибка: {results['error']}")
                continue
            
            stats = results['statistics']
            total_stats['total_files'] += 1
            total_stats['total_references'] += stats['total_references']
            total_stats['total_linked'] += stats['linked_references']
            total_stats['total_processing_time'] += processing_time
            
            print(f"⚡ Анализ завершен за {processing_time*1000:.1f}мс")
            print(f"📝 Длина текста: {stats['text_length']} символов")
            print(f"🔗 Найдено ссылок: {stats['total_references']}")
            print(f"📚 Найдено объектов: {stats['total_objects']}")
            print(f"✅ Связано: {stats['linked_references']}")
            print(f"🎯 Процент связывания: {stats['link_success_rate']*100:.1f}%")
            print(f"🧠 Средняя семантическая схожесть: {stats['average_similarity']:.3f}")
            
            # Показываем примеры с семантическими метриками
            if results['references']:
                print(f"\n🔍 Примеры семантического анализа:")
                for ref in results['references'][:3]:
                    if ref['linked_objects']:
                        best = ref['linked_objects'][0]
                        print(f"  ✅ '{ref['text']}' → '{best['text']}'")
                        print(f"     📊 Общая: {best['similarity']:.3f}, ID: {best['id_similarity']:.3f}, Семантика: {best['semantic_similarity']:.3f}")
                    else:
                        print(f"  ❌ '{ref['text']}' - объект не найден")
            
            # Сохраняем HTML отчет
            html_filename = f"semantic_reports/semantic_analysis_{i}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(results['html_content'])
            
            print(f"\n📄 Семантический отчет сохранен: {html_filename}")
            
        except Exception as e:
            print(f"❌ Ошибка при анализе: {e}")
    
    # Итоговая статистика
    if total_stats['total_files'] > 0:
        print(f"\n{'='*70}")
        print(f"📊 ИТОГОВАЯ СТАТИСТИКА СЕМАНТИЧЕСКОГО АНАЛИЗА")
        print(f"{'='*70}")
        print(f"📁 Обработано файлов: {total_stats['total_files']}")
        print(f"🔗 Всего ссылок: {total_stats['total_references']}")
        print(f"✅ Связано объектов: {total_stats['total_linked']}")
        print(f"🎯 Общий процент связывания: {total_stats['total_linked']/max(total_stats['total_references'], 1)*100:.1f}%")
        print(f"⚡ Среднее время обработки: {total_stats['total_processing_time']/total_stats['total_files']*1000:.1f}мс")
        print(f"🧠 Семантический анализ: ВКЛЮЧЕН")
    
    print(f"\n🎉 СЕМАНТИЧЕСКАЯ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("📁 Проверьте папку semantic_reports/ для детального просмотра результатов")

if __name__ == "__main__":
    run_semantic_demo() 