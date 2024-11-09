from typing import List
from pathlib import Path
from pil_utils import BuildImage
from meme_generator.utils import save_gif
from meme_generator import add_meme
from PIL import Image, ImageSequence  # 导入 ImageSequence

img_dir = Path(__file__).parent / "images"


def pineapple(images: List[BuildImage], texts, args):
    """生成带动画的 Pineapple 表情"""

    frames = []
    base = BuildImage.open(img_dir / "0.png").convert("RGBA")
    avatar_size = (150, 150)  # 头像大小
    avatar_position = (75, 120)  # 头像位置

    # 将第一张图片转换为 PIL 图像以处理 GIF 动图帧
    pil_image = images[0].image  # 获取 PIL.Image 实例
    if pil_image.format == "GIF" and getattr(pil_image, "is_animated", False):
        # 遍历 GIF 动图的每一帧
        for frame in ImageSequence.Iterator(pil_image):
            frame = frame.convert("RGBA").resize(avatar_size)  # 调整大小
            frame_image = BuildImage.new("RGBA", base.size, (255, 255, 255, 0))
            frame_image.paste(frame, avatar_position, alpha=True)  # 将头像帧粘贴到透明位置
            frame_image.paste(base, (0, 0), alpha=True)  # 粘贴菠萝模板
            frames.append(frame_image.image)
    else:
        # 如果传入的图片不是动图，处理静态图片
        img = images[0].convert("RGBA").resize(avatar_size)
        frame_image = BuildImage.new("RGBA", base.size, (255, 255, 255, 0))
        frame_image.paste(img, avatar_position, alpha=True)
        frame_image.paste(base, (0, 0), alpha=True)
        frames.append(frame_image.image)

    # 保存 GIF
    return save_gif(frames, 0.06)


# 注册表情
add_meme(
    "pineapple",
    pineapple,
    min_images=1,
    max_images=1,
    keywords=["菠萝", "pineapple"]
)
