from documentor.structuries.fragment import Fragment

FRAGMENT_POST_INIT_PARAMETRIZER = [
    # Test when all params are None
    (
        {"value": "test"},
        {
            "value": "test",
            "ground_truth": None,
            "label": None, "vector": None,
            "tokens": None,
            "token_vectors": None
        },
    ),
    # Test when ground_truth is provided
    (
        {"value": "test", "ground_truth": 'label1'},
        {
            "value": "test",
            "ground_truth": 'label1',
            "label": None,
            "vector": None,
            "tokens": None,
            "token_vectors": None
        },
    ),
    # Test when label is provided
    (
        {"value": "test", "label": 'label1'},
        {
            "value": "test",
            "ground_truth": None,
            "label": 'label1',
            "vector": None,
            "tokens": None,
            "token_vectors": None
        },
    ),
    # Test when vector is provided
    (
        {"value": "test", "vector": [1.0, 2.0]},
        {
            "value": "test",
            "ground_truth": None,
            "label": None,
            "vector": [1.0, 2.0],
            "tokens": None,
            "token_vectors": None
        },
    ),
    # Test when tokens are provided
    (
        {"value": "test", "tokens": ['token1', 'token2']},
        {
            "value": "test",
            "ground_truth": None,
            "label": None,
            "vector": None,
            "tokens": ['token1', 'token2'],
            "token_vectors": None
        },
    ),
    # Test when token_vectors are provided
    (
        {"value": "test", "token_vectors": [[1.0, 2.0], [3.0, 4.0]]},
        {
            "value": "test",
            "ground_truth": None,
            "label": None,
            "vector": None,
            "tokens": None,
            "token_vectors": [[1.0, 2.0], [3.0, 4.0]]
        },
    ),
]

FRAGMENT_STR_PARAMETRIZER = [
    (Fragment(value="Hello World"), "Hello World"),
    (Fragment(value="12345"), "12345"),
    (Fragment(value=""), "")
]

FRAGMENT_VALUES_PARAMETRIZER = [
    {
        'value': 'test value',
        'ground_truth': 'true label',
        'label': 'test label',
        'vector': [1.0, 2.0],
        'tokens': ['test', 'value'],
        'token_vectors': [[1.0, 2.0], [3.0, 4.0]],
    },
    {
        'value': 'test value',
        'ground_truth': None,
        'label': None,
        'vector': None,
        'tokens': None,
        'token_vectors': None,
    },
]
