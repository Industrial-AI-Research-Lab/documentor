from documentor.types.excel.fragment import SheetFragment
from sklearn.cluster import k_means, DBSCAN

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
        "The xls format is not suitable for processing."
    ),
    (
        {'path': 'data/Global_Hot_List.xlsx',
         'sheet_name': 'Hot',
         'first_cell': 'A5',
         'last_cell': 'U75'},
        "The sheet with the name Hot is not in the file."
    ),
    (
        {'path': 'data/Global.xlsx',
         'sheet_name': 'Hotlist - Identified ',
         'first_cell': 'A5',
         'last_cell': 'U75'},
        "The specified file does not exist or is unavailable."
    ),
    (
        {'path': 'data/Global_Hot_List.xlsx',
         'sheet_name': 'Hotlist - Identified ',
         'first_cell': '???',
         'last_cell': 'U75'},
        "A cell with this address does not exist in the table."
    ),
    (
        {'path': 'data/Global_Hot_List.xlsx',
         'sheet_name': 'Hotlist - Identified ',
         'first_cell': 'A5',
         'last_cell': '???'},
        "A cell with this address does not exist in the table."
    )
]

FRAGMENT_VALUES_PARAMETRIZER = [
    {
        'value': 'Value',
        'start_content': 'Value',
        'relative_id': 25,
        'type': 'str',
        'row': 6,
        'column': 5,
        'length': 5,
        'vertically_merged': False,
        'horizontally_merged': False,
        'font_selection': True,
        'top_border': True,
        'bottom_border': False,
        'left_border': False,
        'right_border': False,
        'color': '00000000',
        'font_color': 0,
        'is_formula': False,
        'row_type': None,
        'ground_truth': None,
        'label': None
    },
    {
        'value': None,
        'start_content': None,
        'relative_id': 25,
        'type': 'str',
        'row': 6,
        'column': 5,
        'length': 5,
        'vertically_merged': False,
        'horizontally_merged': False,
        'font_selection': True,
        'top_border': True,
        'bottom_border': False,
        'left_border': False,
        'right_border': False,
        'color': '00000000',
        'font_color': 0,
        'is_formula': False,
        'row_type': None,
        'ground_truth': None,
        'label': None
    },
]

FRAGMENT_POST_INIT_PARAMETRIZER = [
    # Test when all params are None
    (
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'ground_truth': None,
            'label': None
        },
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'row_type': None,
            'ground_truth': None,
            'label': None
        },
    ),
    (
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'row_type': None,
            'label': None
        },
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'row_type': None,
            'ground_truth': None,
            'label': None
        },
    ),
    (
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'row_type': None,
            'ground_truth': None,
        },
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'row_type': None,
            'ground_truth': None,
            'label': None
        },
    ),
    (
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
        },
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'row_type': None,
            'ground_truth': None,
            'label': None
        },
    ),
    (
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'label': None
        },
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'row_type': None,
        },
    ),
    (
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'ground_truth': None,
        },
        {
            'value': 'Value',
            'start_content': 'Value',
            'relative_id': 25,
            'type': 'str',
            'row': 6,
            'column': 5,
            'length': 5,
            'vertically_merged': False,
            'horizontally_merged': False,
            'font_selection': True,
            'top_border': True,
            'bottom_border': False,
            'left_border': False,
            'right_border': False,
            'color': '00000000',
            'font_color': 0,
            'is_formula': False,
            'row_type': None,
            'ground_truth': None,
            'label': None
        },
    ),
]

DOCUMENT_PATH_PARAMETRIZER = [
    ('data/Global Hot List.csv', ['value', 'start_content', 'relative_id', 'type', 'row', 'column',
                                  'length', 'vertically_merged', 'horizontally_merged',
                                  'font_selection', 'top_border',
                                  'bottom_border', 'left_border', 'right_border', 'color',
                                  'font_color', 'is_formula']),
    ('data/hot_list_parsed.csv', ['value', 'start_content', 'relative_id', 'type', 'row', 'column',
                                  'length', 'vertically_merged', 'horizontally_merged',
                                  'font_selection', 'top_border',
                                  'bottom_border', 'left_border', 'right_border', 'color',
                                  'font_color', 'is_formula', 'ground_truth'])
]

FRAGMENT_STR_PARAMETRIZER = [
    (SheetFragment(value="Hello World",
                   start_content='Hello World',
                   relative_id=25,
                   type='str',
                   row=6,
                   column=5,
                   length=5,
                   vertically_merged=False,
                   horizontally_merged=False,
                   font_selection=True,
                   top_border=True,
                   bottom_border=False,
                   left_border=False,
                   right_border=False,
                   color='00000000',
                   font_color=0,
                   is_formula=False,
                   ),
     "Hello World"),
    (SheetFragment(value="12345",
                   start_content='12345',
                   relative_id=25,
                   type='str',
                   row=6,
                   column=5,
                   length=5,
                   vertically_merged=False,
                   horizontally_merged=False,
                   font_selection=True,
                   top_border=True,
                   bottom_border=False,
                   left_border=False,
                   right_border=False,
                   color='00000000',
                   font_color=0,
                   is_formula=False,
                   ),
     "12345"),
    (SheetFragment(value="",
                   start_content='',
                   relative_id=25,
                   type='str',
                   row=6,
                   column=5,
                   length=5,
                   vertically_merged=False,
                   horizontally_merged=False,
                   font_selection=True,
                   top_border=True,
                   bottom_border=False,
                   left_border=False,
                   right_border=False,
                   color='00000000',
                   font_color=0,
                   is_formula=False,
                   ),
     "")
]


CLASSIFIER_INIT_PARAMS = [
    {'algo': None, 'params': None},
    {'algo': DBSCAN, 'params': None},
    {'algo': None, 'params': {'eps': 0.1, 'min_samples': 3}},
    {'algo': DBSCAN, 'params': {'eps': 0.1, 'min_samples': 3}},
]
