def common_params() -> tuple[list[str], list[tuple[str, dict, str, dict, dict]]]:
    _data = [
        {
            'description': 'flat_dict1',
            'data': {'foo': 'a', 'bar': 'b', 'baz': 'c', 'qux': 'd'},
            'file_name': 'flat_dict1',
            'expected': {},
            'options': {},
        },
        {
            'description': 'flat_dict2',
            'data': {'foo': 1, 'bar': 2, 'baz': 'three', 'qux': True},
            'file_name': 'flat_dict2',
            'expected': {},
            'options': {},
        },
        {
            'description': 'section_dict1',
            'data': {
                'section1': {'foo': 'one', 'bar': 2, 'baz': 'three', 'qux': True},
                'section2': {'foo': 1, 'bar': 'two', 'baz': 3.5, 'qux': False},
            },
            'file_name': 'section_dict1',
            'expected': {},
            'options': {},
        },
        {
            'description': 'section_dict2',
            'data': {
                'section1': {'foo': {'qux': 4}, 'bar': 'two', 'baz': 'three'},
                'section2': {
                    'foo': 'one',
                    'bar': [1, 2, 3],
                    'baz': {'qux': 130, 'quux': 256},
                },
            },
            'file_name': 'section_dict2',
            'expected': {},
            'options': {},
        },
        {
            'description': 'section_dict3',
            'data': {
                'section1': {'foo': {'qux': 4}, 'bar': 'two', 'baz': 'three'},
                'section2': {
                    'foo': 'one',
                    'bar': [1, 2, 3],
                    'baz': {'qux': 130, 'quux': 256},
                },
            },
            'file_name': 'section_dict3',
            'expected': {},
            'options': {},
        },
        {
            'description': 'empty_dict',
            'data': {},
            'file_name': 'empty_dict',
            'expected': {},
            'options': {},
        },
    ]

    return list(_data[0].keys()), [
        (
            d['description'],
            d['data'],
            d['file_name'],
            d['expected'],
            d['options'],
        )
        for d in _data
    ]
