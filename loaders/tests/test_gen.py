def test_recursive_loader_mixed_content(tmp_path):
    """
    Проверяет работу RecursiveLoader при наличии в директории:
      - Нескольких обычных файлов (.txt, .md)
      - Поддиректорий с другими файлами
      - Zip-архивов, содержащих файлы
    """
    import zipfile

    # Создаём в корневой директории файлы TXT и MD
    txt_file_1 = tmp_path / "sample1.txt"
    txt_file_1.write_text("Содержимое первого TXT-файла\nВторая строка", encoding="utf-8")

    md_file_1 = tmp_path / "sample1.md"
    md_file_1.write_text("Содержимое первого MD-файла", encoding="utf-8")

    # Создаём поддиректорию и помещаем туда ещё один TXT-файл
    sub_dir = tmp_path / "nested_folder"
    sub_dir.mkdir()
    txt_file_2 = sub_dir / "sample2.txt"
    txt_file_2.write_text("Содержимое второго TXT-файла\nЕщё одна строка", encoding="utf-8")

    # Создаём вложенный zip-архив с несколькими текстовыми файлами внутри
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("inside_zip_1.txt", "Данные из первого файла в архиве\nВторая строка внутри архива")
        zf.writestr("inside_zip_2.md", "Данные из MD-файла в архиве")

    # Импортируем RecursiveLoader (допускается локальный импорт для теста)
    from loaders.code.recursiveloader_gpt_v1 import RecursiveLoader

    # Инициализируем RecursiveLoader для всех интересующих расширений, включая zip, и рекурсивный обход
    loader = RecursiveLoader(
        file_path=str(tmp_path),
        extension=["txt", "md", "zip"],
        recursive=True,
        zip_loader=True
    )

    # Загружаем документы и проверяем результаты
    documents = list(loader.lazy_load())

    # Ожидаем: 
    # 2 строки из sample1.txt
    # 1 строку из sample1.md
    # 2 строки из sample2.txt
    # 2 строки из inside_zip_1.txt
    # 1 строку из inside_zip_2.md
    # Итого: 2 + 1 + 2 + 2 + 1 = 8 документов
    assert len(documents) == 8, f"Ожидается 8 документов, получено {len(documents)}."

    # Проверяем наличие ожидаемых строк
    page_contents = [doc.page_content.strip() for doc in documents]
    assert any("Содержимое первого TXT-файла" in content for content in page_contents), \
        "Не найдены данные из первого TXT-файла."
    assert any("Содержимое второго TXT-файла" in content for content in page_contents), \
        "Не найдены данные из второго TXT-файла."
    assert any("Содержимое первого MD-файла" in content for content in page_contents), \
        "Не найдены данные из MD-файла в корне."
    assert any("Вторая строка внутри архива" in content for content in page_contents), \
        "Не найдена вторая строка из inside_zip_1.txt."
    assert any("Данные из MD-файла в архиве" in content for content in page_contents), \
        "Не найден MD-файл внутри архива."

    # Проверяем логи
    logs_info = loader.logs["info"]
    assert any("Чтение файла:" in msg for msg in logs_info), "Ожидается лог о чтении файлов."
    assert any("Обработка ZIP архива:" in msg for msg in logs_info), "Ожидается лог об обработке ZIP-архива."
