from rembg import remove
from PIL import Image
import cv2
import os

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 定义输出图片的文件夹路径（用于存放拆分的帧图片）
output_folder = os.path.join(script_dir, "output/")
# 若输出文件夹不存在，则创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 打开影片文件
video_path = "input.mp4"
cap = cv2.VideoCapture(video_path)

# 初始化帧计数器
frame_count = 0

while True:
    # 读取影片的每一帧
    ret, frame = cap.read()
    if not ret:
        break
    # 构建每帧的输出图片文件名
    output_file_name = os.path.join(output_folder, f"frame_{frame_count}.jpg")
    # 将当前帧存储为图片文件
    cv2.imwrite(output_file_name, frame)

    # 对刚保存的这一帧图片进行去背操作
    try:
        # 使用Pillow库打开图片，以便rembg库能处理
        input_image = Image.open(output_file_name)
        output_image = remove(input_image)
        # 将图片转换为RGB模式（如果是RGBA模式）
        if output_image.mode in ["RGBA", "P"]:
            output_image = output_image.convert("RGB")
        # 保存去背之后的图片覆盖原来的图片（也可以自行指定其他格式和文件名，此处选择覆盖原图片保持文件名一致）
        output_image.save(output_file_name)
    except Exception as e:
        print(f"处理图片 {output_file_name} 去背时出错: {e}")

    frame_count += 1

# 释放影片对象
cap.release()
print(f"总共提取了 {frame_count} 帧图片，并进行去背处理，存储到 {output_folder} 文件夹中。")