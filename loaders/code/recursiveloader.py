from typing import Union, Iterator
from overrides import overrides
from langchain_core.documents import Document
from loaders.code.base import BaseLoader
from pathlib import Path
import zipfile

class RecursiveLoader(BaseLoader):
    """
    Loader for recursive directory
    """
    def __init__(self, file_path: Union[str, Path] , 
                extension: list[str] = [], # Расширения файлов, которые будут загружены 
                recursive: bool = True, 
                zip_loader: bool = False, # Флаг для загрузки zip-файлов
                **kwargs):
        """
        Initialize the RecursiveLoader
        """
        self.file_path = Path(file_path)
        self.extension = extension if extension else ['*']
        self.recursive = recursive
        self.zip_loader = zip_loader
        self._logs = {'info': [], 'warning': [], 'error': []}

    @overrides
    def lazy_load(self) -> Iterator[Document]:
        """
        Lazy loading of documents line by line
        """
        # Определяем паттерн поиска файлов
        pattern = '**/*' if self.recursive else '*'
        
        for path in self.file_path.glob(pattern): # Итерируем по всем файлам в директории
            if path.is_file(): # Проверяем, что это файл
                # Проверяем расширение файла
                if self.extension == ['*'] or path.suffix.lower().lstrip('.') in [ext.lower() for ext in self.extension]:# Если расширение не указано или совпадает с указанным, то загружаем файл  
                    if self.zip_loader and path.suffix.lower() == '.zip':# Если включен zip_loader и файл является zip-архивом, то обрабатываем его
                        self._logs['info'].append(f'Обработка ZIP архива: {path}')
                        try:
                            with zipfile.ZipFile(path, 'r') as zip_ref: # Открываем zip-архив
                                for name in zip_ref.namelist(): # Итерируем по всем файлам в архиве
                                    with zip_ref.open(name) as f: # Открываем файл внутри архива
                                        line_number = 0
                                        for line in f.readlines(): # Читаем файл построчно
                                            try:
                                                content = line.decode('utf-8') # Декодируем строку в utf-8  
                                                yield Document(
                                                    page_content=content,# Создаем документ с содержимым строки 
                                                    metadata={# Метаданные документа    
                                                        "line_number": line_number,# Номер строки
                                                        "file_name": name,# Имя файла внутри архива
                                                        "source": f"{path}!{name}",# Источник данных
                                                        "file_type": "zip-content"# Тип файла
                                                    }
                                                )
                                                line_number += 1# Увеличиваем номер строки  
                                            except UnicodeDecodeError:# Если не удается декодировать строку, то добавляем в лог предупреждение
                                                self._logs['warning'].append(
                                                    f'Невозможно декодировать строку в файле {name} внутри {path}'
                                                )
                        except Exception as e:# Если возникает ошибка при чтении архива, то добавляем в лог ошибку
                            self._logs['error'].append(f'Ошибка при чтении ZIP-файла {path}: {str(e)}')
                    else:
                        self._logs['info'].append(f'Чтение файла: {path}')# Если zip_loader не включен, то читаем файл
                        try:
                            with open(path, 'r', encoding='utf-8') as f:# Открываем файл для чтения
                                line_number = 0
                                for line in f:
                                    yield Document(
                                        page_content=line,# Создаем документ с содержимым строки 
                                        metadata={# Метаданные документа    
                                            "line_number": line_number,# Номер строки
                                            "file_name": path.name,# Имя файла
                                            "source": str(path),# Источник данных
                                            "file_type": path.suffix# Тип файла
                                        }
                                    )
                                    line_number += 1# Увеличиваем номер строки  
                        except UnicodeDecodeError:# Если не удается декодировать строку, то добавляем в лог предупреждение
                            self._logs['warning'].append(f'Невозможно декодировать файл {path} как текст')
                        except Exception as e:# Если возникает ошибка при чтении файла, то добавляем в лог ошибку
                            self._logs['error'].append(f'Ошибка при чтении файла {path}: {str(e)}')

    @property
    @overrides
    def logs(self) -> dict[str, list[str]]:
        """
        Logs of the RecursiveLoader
        """
        return self._logs

