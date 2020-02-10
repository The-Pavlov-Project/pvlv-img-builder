from time import time
from pvlv_img_builder.ranking_card import DrawRankingCard


example_level_ranking_card = {
    'background_color': (62, 62, 62),
    'title': 'Ranking of most Active Users',
    'rank': {
        '1': {
            'username': 'Username 1',
            'highlight': True,
            'data': {
                'rank': 1,
                'level': 100,
            },
            'bar': {
                'value': 2341,
                'max': 8000,
            },
        },
        '2': {
            'username': 'Username 2',
            'username_color': (180, 180, 180),
            'highlight': False,
            'data': {
                'rank': 200,
                'rank_label': 'RANK',
                'rank_color': (230, 230, 230),
                'level': 9,
                'level_label': 'LEVEL',
                'level_color': (230, 230, 230),
            },
            'bar': {
                'value': 1926,
                'max': 8000,
                'bar_color_a': (230, 230, 230),
                'bar_color_b': (105, 105, 105),
                'bar_inside_text_a_color': (105, 105, 105),
                'bar_inside_text_b_color': (230, 230, 230),
            },
        },
        '3': {
            'username': 'Username 3',
            'username_color': (180, 180, 180),
            'highlight': True,
            'data': {
                'rank': 300,
                'rank_label': 'RANK',
                'rank_color': (230, 230, 230),
                'level': 3,
                'level_label': 'LEVEL',
                'level_color': (230, 230, 230),
            },
            'bar': {
                'value': 2341,
                'max': 8000,
                'bar_color_a': (230, 230, 230),
                'bar_color_b': (105, 105, 105),
                'bar_inside_text_a_color': (105, 105, 105),
                'bar_inside_text_b_color': (230, 230, 230),
            },
        },
    },
    'text': 'Ranking Data of the most active users\nBeta Command',
    'text_color': (180, 180, 180),
}


def main():
    t1 = time()

    d = DrawRankingCard(example_level_ranking_card)
    d.draw_ranking()
    d.save_image('out/ranking_out.png')

    t2 = time()
    t = (t2-t1) * 1000
    print('{} ms'.format(int(t)))


if __name__ == '__main__':
    main()
