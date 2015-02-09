import subprocess
from PIL import Image

if __name__ == "__main__":

    width = 400
    height = 300
    result = Image.new('RGBA', (width, height))

    img_list = subprocess.check_output(["ls", "./"]).split(b'\n')
    i = 0
    for img in img_list:
        if img[-4:] != b'.png':
            continue
        image = Image.open(img.decode('utf-8'))
        rgb_im = image.convert('RGB')
        for x in range(image.size[0]):
            for y in range(3):
                r, g, b = rgb_im.getpixel((x, image.size[1] - 1))
                result.putpixel((x, i + y),(r, g, b, 255))
        i += 3

    result.save("result.png")
