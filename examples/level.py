from time import time
from pvlv_img_builder.level_card import DrawLevelCard


example_level_card = {
    'background_color': (62, 62, 62),
    'username': 'Revolver chicken',
    'username_color': (180, 180, 180),
    'data': {
        'rank': 'N/D',
        'rank_label': 'RANK',
        'rank_color': (230, 230, 230),
        'level': '10',
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
    'text': 'Cool keep going like that\nI\'m proud of you',
    'text_color': (180, 180, 180),
}


def main():
    t1 = time()

    d = DrawLevelCard(example_level_card)
    d.draw_level_card()
    d.save_image('out/level_out.png')

    t2 = time()
    t = (t2 - t1) * 1000
    print('{} ms'.format(int(t)))


if __name__ == '__main__':
    main()
