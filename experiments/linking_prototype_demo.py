#!/usr/bin/env python3
"""
Финальная демонстрация работающего прототипа системы линкования объектов
Тестирует на реальных данных из датасета linking
"""
import re
import os
import time
from typing import List, Dict, Any, Tuple

class ObjectLinker:
    """Рабочий прототип системы линкования объектов в научных статьях"""
    
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
                y1, x1 = int(parts[2]), int(parts[1])
                word_type = parts[-1]
                
                # Фильтруем только нужные типы
                if word_type in ['paragraph', 'abstract', 'title', 'section']:
                    words_data.append((y1, x1, word))
        
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
                    'linked_objects': []
                })
        
        return references
    
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
                    'end': match.end()
                })
        
        return objects
    
    def link_references_to_objects(self, references: List[Dict], objects: List[Dict]) -> None:
        """Связывает ссылки с объектами"""
        for ref in references:
            ref_type = ref['type']
            ref_id = ref['id']
            
            # Ищем объекты того же типа
            for obj in objects:
                if obj['type'] == ref_type:
                    similarity = self.calculate_similarity(ref_id, obj['id'])
                    
                    if similarity > 0.7:  # порог схожести
                        ref['linked_objects'].append({
                            'text': obj['text'],
                            'type': obj['type'],
                            'id': obj['id'],
                            'similarity': similarity
                        })
        
        # Сортируем связанные объекты по схожести
        for ref in references:
            ref['linked_objects'].sort(key=lambda x: x['similarity'], reverse=True)
    
    def calculate_similarity(self, ref_id: str, obj_id: str) -> float:
        """Вычисляет схожесть между идентификаторами"""
        if not ref_id or not obj_id:
            return 0.0
        
        # Точное совпадение
        if ref_id == obj_id:
            return 1.0
        
        # Частичное совпадение
        if ref_id in obj_id or obj_id in ref_id:
            return 0.8
        
        return 0.0
    
    def generate_html_report(self, text: str, references: List[Dict], objects: List[Dict]) -> str:
        """Генерирует HTML отчет с выделенными ссылками"""
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
                tooltip = f"Связано с {len(ref['linked_objects'])} объектами"
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
    <title>Анализ ссылок в научном документе</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            background: #007bff;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .stats {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .content {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            white-space: pre-wrap;
            font-size: 14px;
        }}
        .reference {{
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .reference.linked {{
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        .reference.unlinked {{
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        .reference:hover {{
            transform: scale(1.05);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        .legend {{
            margin-top: 20px;
            padding: 15px;
            background: #e9ecef;
            border-radius: 8px;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 5px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔗 Анализ ссылок в научном документе</h1>
        <p>Система автоматического линкования объектов</p>
    </div>
    
    <div class="stats">
        <h3>📊 Статистика анализа:</h3>
        <p><strong>📄 Длина текста:</strong> {len(text)} символов</p>
        <p><strong>🔗 Найдено ссылок:</strong> {len(references)}</p>
        <p><strong>✅ Связано объектов:</strong> {len([r for r in references if r['linked_objects']])}</p>
        <p><strong>📚 Найдено объектов:</strong> {len(objects)}</p>
        <p><strong>🎯 Процент связывания:</strong> {len([r for r in references if r['linked_objects']]) / len(references) * 100:.1f}% {'' if references else '(нет ссылок)'}</p>
    </div>
    
    <div class="content">{html_text}</div>
    
    <div class="legend">
        <h3>🎨 Легенда:</h3>
        <div class="legend-item">
            <span class="reference linked">Связанная ссылка</span> - найден соответствующий объект
        </div>
        <div class="legend-item">
            <span class="reference unlinked">Несвязанная ссылка</span> - объект не найден
        </div>
    </div>
</body>
</html>
        """
    
    def analyze_document(self, file_path: str) -> Dict[str, Any]:
        """Полный анализ документа"""
        # Извлекаем текст
        text = self.extract_text_from_ocr(file_path)
        
        if not text:
            return {'error': 'Не удалось извлечь текст'}
        
        # Находим ссылки и объекты
        references = self.find_references(text)
        objects = self.find_objects(text)
        
        # Связываем ссылки с объектами
        self.link_references_to_objects(references, objects)
        
        # Генерируем HTML отчет
        html_content = self.generate_html_report(text, references, objects)
        
        return {
             'text': text,
             'references': references,
             'objects': objects,
             'html_content': html_content,
                          'statistics': {
                 'text_length': len(text),
                 'total_references': len(references),
                 'linked_references': len([r for r in references if r['linked_objects']]),
                 'total_objects': len(objects),
                 'link_success_rate': len([r for r in references if r['linked_objects']]) / len(references) if len(references) > 0 else 0
             }
         }

def get_test_files() -> List[str]:
    """Находит доступные файлы для тестирования"""
    test_files = []
    ann_dir = "linking/ann"
    
    if os.path.exists(ann_dir):
        for file in os.listdir(ann_dir):
            if file.endswith('.txt'):
                test_files.append(os.path.join(ann_dir, file))
    
    return test_files  # ограничиваем количество для демонстрации

def run_prototype_demo():
    """Запускает демонстрацию прототипа"""
    print("🚀 ДЕМОНСТРАЦИЯ ПРОТОТИПА СИСТЕМЫ ЛИНКОВАНИЯ ОБЪЕКТОВ")
    print("=" * 60)
    
    # Инициализируем систему
    linker = ObjectLinker()
    
    # Находим файлы для тестирования
    test_files = get_test_files()
    
    if not test_files:
        print("❌ Файлы для тестирования не найдены в папке linking/ann/")
        print("Убедитесь, что датасет распакован корректно")
        return
    
    print(f"📁 Найдено {len(test_files)} файлов для тестирования")
    
    # Тестируем каждый файл
    for i, file_path in enumerate(test_files, 1):
        print(f"\n{'='*60}")
        print(f"ТЕСТ {i}/{len(test_files)}: {os.path.basename(file_path)}")
        print(f"{'='*60}")
        
        try:
            start_time = time.time()
            results = linker.analyze_document(file_path)
            processing_time = time.time() - start_time
            
            if 'error' in results:
                print(f"❌ Ошибка: {results['error']}")
                continue
            
            stats = results['statistics']
            
            print(f"✅ Анализ завершен за {processing_time*1000:.1f}мс")
            print(f"📝 Длина текста: {stats['text_length']} символов")
            print(f"🔗 Найдено ссылок: {stats['total_references']}")
            print(f"📚 Найдено объектов: {stats['total_objects']}")
            print(f"✅ Связано: {stats['linked_references']}")
            print(f"🎯 Процент связывания: {stats['link_success_rate']*100:.1f}%")
            
            # Показываем примеры найденных ссылок
            if results['references']:
                print(f"\n📋 Примеры найденных ссылок:")
                for ref in results['references'][:5]:
                    status = "✅" if ref['linked_objects'] else "❌"
                    print(f"  {status} '{ref['text']}' (тип: {ref['type']}, ID: {ref['id']})")
            
            # Показываем найденные объекты
            if results['objects']:
                print(f"\n📚 Найденные объекты:")
                for obj in results['objects'][:3]:
                    print(f"  • '{obj['text']}' (тип: {obj['type']}, ID: {obj['id']})")
            
            # Сохраняем HTML отчет
            html_filename = f"linking_reports/analysis_report_{i}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(results['html_content'])
            
            print(f"\n📄 HTML отчет сохранен: {html_filename}")
            
        except Exception as e:
            print(f"❌ Ошибка при анализе: {e}")
    
    print(f"\n🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("📁 Проверьте созданные HTML файлы для детального просмотра результатов")

if __name__ == "__main__":
    run_prototype_demo() 