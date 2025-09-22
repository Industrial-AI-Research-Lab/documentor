import os
import shutil

# Директория, в которую копируем файлы
destination_dir = 'listening'

# Игнорируемая директория и файл
ignore_dirs = ['.idea']
ignore_files = ['test.py']

# Расширения файлов, которые нужно копировать
allowed_extensions = ['.md', '.py']

# Если директория 'listening' существует, очищаем ее
if os.path.exists(destination_dir):
    shutil.rmtree(destination_dir)
os.makedirs(destination_dir)

# Функция для копирования файлов с учетом иерархии в именах
def copy_files_with_hierarchy(src_dir):
    for root, dirs, files in os.walk(src_dir):
        # Игнорируем указанные директории
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            # Игнорируем указанные файлы и копируем только файлы с нужным расширением
            if file in ignore_files:
                continue

            file_extension = os.path.splitext(file)[1]
            if file_extension in allowed_extensions:
                # Формируем новое имя файла с учетом исходной иерархии
                relative_path = os.path.relpath(root, src_dir)
                new_file_name = os.path.join(destination_dir, relative_path.replace(os.sep, '_') + '_' + file)
                new_file_name = os.path.normpath(new_file_name)

                # Копируем файл
                src_file_path = os.path.join(root, file)
                shutil.copy2(src_file_path, new_file_name)
                print(f"Скопирован файл: {new_file_name}")

# Запуск копирования из текущей директории
current_directory = os.path.dirname(os.path.abspath(__file__))
copy_files_with_hierarchy(current_directory)
