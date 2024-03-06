PARSER_WORK_PARAMETRIZER = [
    {'path': 'data/Global_Hot_List.xlsx',
     'sheet_name': 'Hotlist - Identified ',
     'first_cell': 'A5',
     'last_cell': 'U75'},
    {'path': 'data/Global_Hot_List.xlsx',
     'sheet_name': 'Hotlist - Identified ',
     'first_cell': None,
     'last_cell': None},
    {'path': 'data/Global_Hot_List.xlsx',
     'sheet_name': 'Hotlist - Identified ',
     'first_cell': 'A5',
     'last_cell': None},
    {'path': 'data/Global_Hot_List.xlsx',
     'sheet_name': 'Hotlist - Identified ',
     'first_cell': None,
     'last_cell': 'U75'},
]

PARSER_EXCEPTIONS_PARAMETRIZER = [
    (
        {'path': 'data/Global_Hot_List.xls',
         'sheet_name': 'Hotlist - Identified ',
         'first_cell': 'A5',
         'last_cell': 'U75'},
        "The {form} format is not suitable for processing."
    ),
    (
        {'path': 'data/Global_Hot_List.xlsx',
         'sheet_name': 'Hotlist - Identified ',
         'first_cell': 'A5',
         'last_cell': 'U75'},
        "The sheet with the name {sheet_name} is not in the file."
    ),
    (
        {'path': 'data/Global.xlsx',
         'sheet_name': 'Hotlist - Identified ',
         'first_cell': 'A5',
         'last_cell': 'U75'},
        "The specified file does not exist or is unavailable."
    ),
    (
        {'path': 'data/Global.xlsx',
         'sheet_name': 'Hotlist - Identified ',
         'first_cell': '???',
         'last_cell': 'U75'},
        "A cell with this address does not exist in the table."
    ),
    (
        {'path': 'data/Global.xlsx',
         'sheet_name': 'Hotlist - Identified ',
         'first_cell': 'A5',
         'last_cell': '???'},
        "A cell with this address does not exist in the table."
    )
]
