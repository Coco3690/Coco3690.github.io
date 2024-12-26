import cv2
import os

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 定义输出图片的文件夹路径
output_folder = os.path.join(script_dir, "output/")

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
    frame_count += 1

# 释放影片对象
cap.release()
print(f"总共提取了 {frame_count} 帧图片，存储到 {output_folder} 文件夹中。")