from pvlv_img_builder.level import DrawLevelCard


example_level_card = {
    'background_color': (62, 62, 62),
    'username': 'Congratulations User',
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
        'value': '2341',
        'max': '8000',
        'bar_color': (230, 230, 230),
        'bar_background_color': (230, 230, 230),
        'inside_xp_dark_color': (230, 230, 230),
        'inside_xp_light_color': (230, 230, 230),
    },
    'text': 'Cool keep going like that',
    'text_color': (180, 180, 180),
}


def main():
    d = DrawLevelCard(example_level_card)
    d.save_image('level.png')


if __name__ == '__main__':
    main()
