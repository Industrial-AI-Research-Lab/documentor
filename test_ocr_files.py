"""Тест OCR пайплайна на реальных файлах."""

import sys
import os
from pathlib import Path

# Добавляем путь к модулю documentor
sys.path.insert(0, str(Path(__file__).parent / "documentor"))

from PIL import Image
from documentor.pipelines.ocr import PDFProcessor, OCRPipelineConfig


def test_image_processing(image_path: str):
    """Тест обработки изображения."""
    print(f"\n🖼️ Тестируем изображение: {image_path}")
    print("=" * 50)
    
    try:
        # Загружаем изображение
        image = Image.open(image_path)
        print(f"✅ Изображение загружено: {image.size[0]}x{image.size[1]} пикселей")
        
        # Создаем конфигурацию
        config = OCRPipelineConfig.create_default()
        print(f"✅ Конфигурация создана")
        
        # Создаем процессор
        processor = PDFProcessor(config)
        print(f"✅ PDFProcessor создан")
        
        # Обрабатываем изображение
        print(f"🔄 Обрабатываем изображение...")
        fragments = list(processor.process_image(image))
        
        print(f"✅ Обработка завершена! Найдено фрагментов: {len(fragments)}")
        
        # Выводим результаты
        for i, fragment in enumerate(fragments, 1):
            print(f"\n--- Фрагмент {i} ---")
            print(f"Тип: {type(fragment).__name__}")
            print(f"Текст: {fragment.value[:100]}{'...' if len(fragment.value) > 100 else ''}")
            if hasattr(fragment, 'style') and fragment.style:
                print(f"Стиль: {fragment.style}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обработке изображения: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pdf_processing(pdf_path: str):
    """Тест обработки PDF."""
    print(f"\n📄 Тестируем PDF: {pdf_path}")
    print("=" * 50)
    
    try:
        # Проверяем наличие PyPDF2
        try:
            import PyPDF2
            print("✅ PyPDF2 доступен")
        except ImportError:
            print("⚠️ PyPDF2 не установлен - selectable text недоступен")
        
        # Создаем конфигурацию
        config = OCRPipelineConfig.create_default()
        print(f"✅ Конфигурация создана")
        
        # Создаем процессор
        processor = PDFProcessor(config)
        print(f"✅ PDFProcessor создан")
        
        # Для PDF нужен page_image, попробуем извлечь первую страницу
        try:
            # Простая попытка конвертации PDF в изображение (если доступно)
            print("🔄 Пытаемся обработать PDF...")
            
            # Пока что просто проверим, что файл существует
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"✅ PDF файл найден: {file_size} байт")
                
                # Попробуем извлечь selectable text
                selectable_text = processor.extract_selectable_text(pdf_path, page_num=0)
                if selectable_text:
                    print(f"✅ Selectable text найден: {len(selectable_text)} символов")
                    print(f"Первые 200 символов: {selectable_text[:200]}...")
                else:
                    print("⚠️ Selectable text не найден - нужен OCR")
                
                return True
            else:
                print(f"❌ PDF файл не найден: {pdf_path}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при обработке PDF: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Ошибка при создании процессора: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Основная функция тестирования."""
    print("🚀 Запуск тестов OCR пайплайна")
    print("=" * 60)
    
    # Тестируем изображение
    image_path = "example.jpg"
    if os.path.exists(image_path):
        test_image_processing(image_path)
    else:
        print(f"❌ Файл изображения не найден: {image_path}")
    
    # Тестируем PDF
    pdf_path = "example.pdf"
    if os.path.exists(pdf_path):
        test_pdf_processing(pdf_path)
    else:
        print(f"❌ PDF файл не найден: {pdf_path}")
    
    print("\n" + "=" * 60)
    print("🏁 Тестирование завершено")


if __name__ == "__main__":
    main()
