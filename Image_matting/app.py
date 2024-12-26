from rembg import remove
from PIL import Image

# 打开要处理的图片，这里假设图片和代码在同一目录下，名为 input.jpg，可以根据实际情况修改
input_image = Image.open("input.jpg")

# 执行去背操作
output_image = remove(input_image)

# 保存去背之后的图片为 output.png，也可以自行指定其他格式和文件名
output_image.save("output.png")