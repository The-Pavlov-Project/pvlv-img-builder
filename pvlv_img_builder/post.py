from pvlv_img_builder.modules.post.paginator import Paginator
from pvlv_img_builder.modules.post.configs import Configs

    
if __name__ == '__main__':
    configs = Configs({
        "pavlov": {
            "logo": "img/icons/pavlov.png",
            "images": {
                "meme": {
                    "image_scale": [1, 1],
                    "colorize_logo": False,
                    "logo_position": "auto"
                }
            },
            "text": {
                "spot": {
                    "top_image": "quotation-marks",
                    "text_align": "center",
                    "line_position": None,
                    "colorize_logo": True,
                    "logo_position": "center",
                    "rectangle": False
                }
            }
        }
    })

    colors = configs.get_colors_setup('text', 'spot')
    
    paginator = Paginator("img/icons/pavlov.png", configs.resolution, colors=colors, name_tag="name_tag")
    kwargs = configs.build_kwargs('text', 'spot')
    paginator.paginate_text("ciao", **kwargs)
    paginator.save_image("image.jpeg")
