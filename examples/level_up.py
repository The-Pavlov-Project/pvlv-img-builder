from pvlv_img_builder.level_up_card import DrawLevelUpCard
from time import time

example_level_up_card = {
    'background_color': (62, 62, 62),
    'level': '20',
    'level_color': (230, 230, 230),
    'bold_text': 'Congratulations User',
    'bold_text_color': (180, 180, 180),
    'text': 'You have gained a level\nYou have gained a level',
    'text_color': (180, 180, 180),
}


def main():
    t1 = time()

    d = DrawLevelUpCard(example_level_up_card)
    d.draw_level_up()
    d.save_image('level_up_out.png')

    t2 = time()
    t = (t2-t1) * 1000
    print('{} ms'.format(int(t)))


if __name__ == '__main__':
    main()
