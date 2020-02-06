from pvlv_img_builder.level_up import DrawLevelUpCard


example_level_up_card = {
    'background_color': (62, 62, 62),
    'level': '10',
    'level_color': (230, 230, 230),
    'title': 'Congratulations User',
    'title_color': (180, 180, 180),
    'text': 'You have gained a level',
    'text_color': (180, 180, 180),
}


def main():
    d = DrawLevelUpCard(example_level_up_card)
    d.draw_level_up()
    d.save_image('level_up_out.png')


if __name__ == '__main__':
    main()
