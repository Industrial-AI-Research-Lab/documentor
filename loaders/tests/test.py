# Ниже приведены простые тестовые примеры для проверки функциональности RecursiveLoader.
# Тесты написаны с использованием Pytest.
# Если в вашем проекте не используется Pytest, адаптируйте код под используемый фреймворк.

from loaders.code.recursiveloader_gpt_v1 import RecursiveLoader

def test_recursive_loader_simple_file(tmp_path):
    """
    Проверяет базовую загрузку текстового файла в массив документов.
    """
    # Создаем тестовый файл
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello World\nThis is a test", encoding="utf-8")

    # Инициируем RecursiveLoader
    loader = RecursiveLoader(
        file_path=str(tmp_path),
        extension=["txt"],
        recursive=True,
        zip_loader=False
    )

    # Загружаем документы
    documents = list(loader.lazy_load())

    # Проверяем результаты
    assert len(documents) == 2, "Ожидается 2 строки из текстового файла"
    assert documents[0].page_content.strip() == "Hello World"
    assert documents[1].page_content.strip() == "This is a test"
    assert len(loader.logs["info"]) > 0, "Ожидается лог о загрузке файла"
    assert "Чтение файла:" in loader.logs["info"][0]


def test_recursive_loader_zip(tmp_path):
    """
    Проверяет загрузку контента из zip-архива.
    """
    import zipfile

    # Создаем тестовый zip-архив
    zip_path = tmp_path / "test_archive.zip"
    text_content = "Hello from zip\nAnother line"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("file_inside.txt", text_content)

    # Инициируем RecursiveLoader с поддержкой zip_loader
    loader = RecursiveLoader(
        file_path=str(tmp_path),
        extension=["zip"],
        recursive=True,
        zip_loader=True
    )

    # Загружаем документы
    documents = list(loader.lazy_load())

    # Проверяем результаты
    assert len(documents) == 2, "Ожидается 2 строки из файла внутри zip"
    assert documents[0].page_content.strip() == "Hello from zip"
    assert documents[1].page_content.strip() == "Another line"
    assert "Обработка ZIP архива:" in loader.logs["info"][0]


def test_recursive_loader_unsupported_extension(tmp_path):
    """
    Проверяет, что файлы с неподходящим расширением не грузятся.
    """
    # Создаем файлы с разными расширениями
    txt_file = tmp_path / "test_file.txt"
    txt_file.write_text("Sample text", encoding="utf-8")
    md_file = tmp_path / "readme.md"
    md_file.write_text("Markdown content", encoding="utf-8")

    # Загружаем только txt-файлы
    loader = RecursiveLoader(
        file_path=str(tmp_path),
        extension=["txt"],
        recursive=False,
        zip_loader=False
    )

    documents = list(loader.lazy_load())
    assert len(documents) == 1, "Ожидается загрузка только 1 файла c расширением txt"
    assert documents[0].page_content.strip() == "Sample text"
    log_info = loader.logs["info"]
    # Проверим, что в логах нет попытки чтения readme.md
    assert all("readme.md" not in message for message in log_info)

    def test_recursive_loader_empty_directory(tmp_path):
        """
        Проверяет, что при отсутствии файлов в директории не загружается ни одного документа.
        """
        # В tmp_path не создаём никаких файлов, оставляя директорию пустой
        loader = RecursiveLoader(
            file_path=str(tmp_path),
            extension=["txt", "md", "zip"],
            recursive=True,
            zip_loader=True
        )
        documents = list(loader.lazy_load())
        assert len(documents) == 0, "Ожидается отсутствие документов при пустой директории"
        assert not loader.logs["info"], "Ожидается отсутствие информационных записей в логах при пустой директории"

    def test_recursive_loader_multiple_files(tmp_path):
        """
        Проверяет работу загрузчика при наличии нескольких файлов разных типов.
        """
        # Создаём несколько файлов разных типов
        txt_file = tmp_path / "file1.txt"
        txt_file.write_text("Содержимое TXT-файла", encoding="utf-8")

        md_file = tmp_path / "file2.md"
        md_file.write_text("Содержимое MD-файла", encoding="utf-8")

        # Указываем, что нас интересуют файлы с расширением txt и md
        loader = RecursiveLoader(
            file_path=str(tmp_path),
            extension=["txt", "md"],
            recursive=False,
            zip_loader=False
        )
        documents = list(loader.lazy_load())

        # Проверяем, что оба файла были загружены
        assert len(documents) == 2, "Ожидается загрузка двух документов"
        assert any("Содержимое TXT-файла" in doc.page_content for doc in documents), "Не найден TXT-документ"
        assert any("Содержимое MD-файла" in doc.page_content for doc in documents), "Не найден MD-документ"

    def test_recursive_loader_subdirectories(tmp_path):
        """
        Проверяет работу загрузчика при необходимости рекурсивного обхода поддиректорий.
        """
        # Создаём поддиректорию и файл внутри неё
        sub_dir = tmp_path / "subfolder"
        sub_dir.mkdir()
        sub_file = sub_dir / "nested.txt"
        sub_file.write_text("Текст внутри поддиректории", encoding="utf-8")

        # Запускаем загрузчик с рекурсивным обходом
        loader = RecursiveLoader(
            file_path=str(tmp_path),
            extension=["txt"],
            recursive=True,
            zip_loader=False
        )
        documents = list(loader.lazy_load())
        assert len(documents) == 1, "Ожидается загрузка одного файла из вложенной директории"
        assert "Текст внутри поддиректории" in documents[0].page_content, "Файл из поддиректории не был загружен"

    def test_recursive_loader_several_zips(tmp_path):
        """
        Проверяет работу рекурсивного загрузчика, если в директории несколько ZIP-архивов.
        """
        import zipfile

        # Создаём первый архив
        zip_path_1 = tmp_path / "archive1.zip"
        with zipfile.ZipFile(zip_path_1, "w") as zf:
            zf.writestr("inside1.txt", "Содержимое первого архива\nВторая строка")

        # Создаём второй архив
        zip_path_2 = tmp_path / "archive2.zip"
        with zipfile.ZipFile(zip_path_2, "w") as zf:
            zf.writestr("inside2.txt", "Содержимое второго архива")

        loader = RecursiveLoader(
            file_path=str(tmp_path),
            extension=["zip"],
            recursive=True,
            zip_loader=True
        )
        documents = list(loader.lazy_load())
        # Первый архив содержит 2 строки, второй - 1 строку => всего 3 документа
        assert len(documents) == 3, "Ожидается загрузка трёх строк из двух разных zip-архивов"

        # Проверяем, что каждая строка присутствует
        contents = [doc.page_content.strip() for doc in documents]
        assert "Содержимое первого архива" in contents[0], "Не найдено содержимое первого архива"
        assert "Вторая строка" in contents[1], "Не найдена вторая строка из первого архива"
        assert "Содержимое второго архива" in contents[2], "Не найдено содержимое второго архива"

