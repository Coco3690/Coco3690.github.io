import gradio as gr
import shutil
import os
from scenedetect import open_video, SceneManager, split_video_ffmpeg
from scenedetect.detectors import ContentDetector


def split_video_into_scenes(video_path, threshold=27.0):
    # 打开视频文件
    video = open_video(video_path)
    # 创建场景管理器
    scene_manager = SceneManager()
    # 向场景管理器添加内容检测器，并设置阈值
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    # 开始对视频进行场景检测，并显示进度
    scene_manager.detect_scenes(video, show_progress=True)
    # 获取检测到的场景列表
    scene_list = scene_manager.get_scene_list()
    # 使用 ffmpeg 分割视频，根据检测到的场景列表，并显示分割进度
    split_video_ffmpeg(video_path, scene_list, show_progress=True)


def process_video(video_path):
    # 获取当前目录
    current_directory = os.getcwd()
    print(f"当前目录: {current_directory}")  # 打印当前目录以便调试
    
    # 提取影片名称
    video_name = os.path.basename(video_path)  # 获取文件名称
    save_path = os.path.join(current_directory, video_name)
    print(f"保存路径: {save_path}")  # 打印保存路径以便调试
    
    try:
        # 使用 shutil 库将上传的影片复制到指定目录
        shutil.copy(video_path, save_path)
        print(f"成功拷贝影片: {video_name} 到 {save_path}")  # 成功消息
        split_video_into_scenes(save_path)  # 调用视频分割函数
        return f"已成功上传影片: {video_name} 到 {save_path} 并进行场景分割。"
    except Exception as e:
        print(f"拷贝影片时发生错误: {e}")  # 错误消息
        return f"拷贝影片时发生错误: {e}"


# 建立 Gradio 界面
with gr.Blocks() as app:
    gr.Markdown("# 影片上传与处理")
    
    with gr.Row():
        with gr.Column():
            # 设定影片显示的高度和宽度
            video_input = gr.Video(label="上传影片", height=600, width=600)  # 可以根据需要调整尺寸
        
        with gr.Column():
            output_message = gr.Textbox(label="消息显示框", interactive=False)
    
    submit_button = gr.Button("Submit")  # 添加 Submit 按钮

    # 当点击 submit 按钮时，调用 process_video 函数
    submit_button.click(fn=process_video, inputs=video_input, outputs=output_message)

# 启动 Gradio 应用
if __name__ == "__main__":
    app.launch()