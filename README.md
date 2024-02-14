<div style="float: right; width: 200px; height: 200px;">
  <img src="images/logo.png" width="200" alt="tmp-logo">
</div>

# DocuMentor


[![Acknowledgement ITMO](https://raw.githubusercontent.com/aimclub/open-source-ops/master/badges/ITMO_badge.svg)](https://itmo.ru/)
[![Acknowledgement SAI](https://raw.githubusercontent.com/aimclub/open-source-ops/master/badges/SAI_badge.svg)](https://sai.itmo.ru/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Visitors](https://api.visitorbadge.io/api/combined?path=https%3A%2F%2Fgithub.com%2FIndustrial-AI-Research-Lab%2Fdocumentor&countColor=%23263759&style=plastic&labelStyle=lower)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FIndustrial-AI-Research-Lab%2Fdocumentor)
[![PythonVersion](https://img.shields.io/badge/python_3.10-passing-success)](https://img.shields.io/badge/python_3.10-passing-success)                                                                                                                                                                                  


## The purpose of the project

The DocuMentor library is designed to simplify and automate the parsing and semantic analysis of various types of 
documents, including word, excel and log files.

The library performs the following tasks:
1. Data extraction
2. Conversion of specialized terms
3. Hierarchical analysis of the document structure
4. Entity recognition in documents

## Core features

TBD

## Installation

Download the library from the repository and install it using the following command:
```shell
pip install -r requirements.txt

# for running examples jupyter notebooks:
pip install jupyter jupytext

# convert .md to .ipynb
jupytext --to notebook file_name.md
```

## Examples


All examples made in jupyter notebooks, so you should have jupyter installed to run them.
Jupyter notebooks are saved with the .md extension, to convert to .ipynb, you can manually copy the code or use the 
jupytext library (see installation section for details).

- usage of specialized terms search - [link](examples/semantic_example.md)
- usage of excel to csv parser  - [link](examples/table_parsing.md)
- usage of sheet fragment classification  - [link](examples/table_fragmentation.md)


## Project structure

- [documentor](documentor/README.md) - main library folder
- [deployment](deployment/README.md) - folder for storing scripts and dockerfiles for deploying the library or its components
- [examples](examples/README.md) - folder for storing examples of using the library
- [notebooks](notebooks/README.md) - folder for storing notebooks with researches and base experiments
- [tests](tests/README.md) - folder for storing tests for the library
- [experiments](experiments/README.md) - folder for storing experiments with the library
- [docs](docs/README.md) - folder for storing documentation for the library

## Documentation

TBD

## Getting started

TBD

## Development tasks

- Test implementation for developed functionality
- Documentation for the library
- Implementation of pipelines for the full process of semantic document parsing
- Improving the search for table boundaries using genetic selection of heuristics and convolutional neural networks
- Improvement of the algorithm for searching and replacing specialized terms
- Implementation of the hierarchy allocation algorithm in word documents, taking into account semantics
- Implementation of the algorithm for recognizing entities in documents

## License

[BSD 3-Clause License](LICENSE.md)

## Acknowledgements

By ITMO University, Saint Petersburg, Russia 

## Contacts

Questions and suggestions can be asked to Mikhail Kovalchuk by the following contacts:
- [Telegram](https://t.me/hungry_muskrat)
- [Email](mailto:mkovalchuk@itmo.ru) 
