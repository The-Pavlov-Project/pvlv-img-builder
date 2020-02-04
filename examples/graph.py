example_graph = {
    'background_color': (62, 62, 62),
    'top_title': 'Main sheet title',
    'top_title_color': (230, 230, 230),
    'text_color': (180, 180, 180),
    'title_color': (180, 180, 180),
    'section_1': {
        'section_title': 'graph title',
        'section_title_color': (230, 230, 230),
        'graph_1': {
            'subtitle': 'subtitle of the graph',
            'subtitle_color': (180, 180, 180),
            'x_names': [1, 2, 3, 4, 5, 6],
            'y_names': [50, 100, 150],
            'tower_1': {
                'data': [12, 23, 43, 21, 21, 23],
                'value_printed': [12, 23, 43, 21, 21, 23],
                'printed_position': 'on_top',
                'tower_dim': 1,
                'color': (0, 0, 255)
            },
            'tower_2': {
                'data': [122, 123, 143, 221, 211, 213],
                'value_printed': ['2 min', '3 min', '2 min', '2 min', '1 min', '5 min'],
                'printed_position': 'inside',
                'tower_dim': 0.5,
                'color': (0, 255, 0)
            },

        },
        'description': "multi line text here, to describe the graph"
    },
    'section_2': {
        'section_title': 'graph title',
        'section_title_color': (230, 230, 230),
        'graph_1': {
            'subtitle': 'subtitle of the graph',
            'subtitle_color': (180, 180, 180),
            'x_names': [1, 2, 3, 4, 5, 6],
            'y_names': [50, 100, 150],
            'tower_1': {
                'data': [12, 23, 43, 21, 21, 23],
                'value_printed': [12, 23, 43, 21, 21, 23],
                'color': (0, 0, 255)
            }
        },
        'graph_2': {
            'subtitle': 'subtitle of the graph',
            'subtitle_color': (180, 180, 180),
            'x_names': [1, 2, 3, 4, 5, 6],
            'y_names': [50, 100, 150],
            'tower_1': {
                'data': [12, 23, 43, 21, 21, 23],
                'value_printed': [12, 23, 43, 21, 21, 23],
                'color': (0, 0, 255)
            },
            'tower_2': {
                'data': [122, 123, 143, 221, 211, 213],
                'value_printed': ['2 min', '3 min', '2 min', '2 min', '1 min', '5 min'],
                'color': (0, 255, 0)
            },
        },
        'description': "multi line text here, to describe the graph"
    },
    'footer': "this is the end of all"
}
