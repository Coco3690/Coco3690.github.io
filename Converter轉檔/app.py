import gradio as gr
import shutil
import os
import subprocess


def copy_video(video_path):
    current_directory = os.getcwd()
    video_name = os.path.basename(video_path)
    file_name, file_extension = os.path.splitext(video_name)
    save_path = os.path.join(current_directory, "video" + file_extension)
    try:
        # 拷贝其他格式的影片
        shutil.copy(video_path, save_path)
        print(f"成功拷贝影片: {video_path} 到 {save_path}")
        return f"已成功上载影片: {video_path} 到 {save_path}。"
    except Exception as e:
        print(f"拷贝影片时发生错误: {e}")
        return f"拷贝影片时发生错误: {e}"


def convert_video(video_path):
    current_directory = os.getcwd()
    video_name = os.path.basename(video_path)
    file_name, file_extension = os.path.splitext(video_name)
    # 生成新的 mp3 和 wav 文件名
    mp3_name = "video.mp3"
    mp3_path = os.path.join(current_directory, mp3_name)
    wav_name = "video.wav"
    wav_path = os.path.join(current_directory, wav_name)
    try:
        # 检查是否是 webm 或 mkv 格式
        if file_extension.lower() == '.webm' or file_extension.lower() == '.mkv':
            mp4_name = "video.mp4"
            mp4_path = os.path.join(current_directory, mp4_name)
            # 将 webm 或 mkv 转换为 mp4，并自动覆盖
            command = ['ffmpeg', '-y', '-i', video_path, mp4_path]
            try:
                subprocess.run(command, check=True)
                video_path = mp4_path
            except subprocess.CalledProcessError as e:
                print(f"转换失败，命令: {' '.join(command)}")
                return f"转换失败，命令: {' '.join(command)}"
        # 使用 ffmpeg 转换 MP4 到 MP3，并自动覆盖
        subprocess.run(['ffmpeg', '-y', '-i', video_path, mp3_path], check=True)
        # 使用 ffmpeg 转换 MP4 到 WAV，并自动覆盖
        subprocess.run(['ffmpeg', '-y', '-i', video_path, wav_path], check=True)
        return f"影片 {video_name} 已成功转换为 {mp3_name} 和 {wav_name}。"
    except subprocess.CalledProcessError as e:
        return f"转换影片时发生错误: {e}"


def split_video(video_path):
    current_directory = os.getcwd()
    file_name, file_extension = os.path.splitext(video_path)
    split_video_name = "video" + file_extension
    split_video_path = os.path.join(current_directory, split_video_name)
    try:
        # 真正的分割操作可使用 ffmpeg 的分割功能，以下是一个示例，根据具体需求修改
        # 例如，将视频从第 0 秒开始，分割为 10 秒一段
        split_command = ['ffmpeg', '-i', video_path, '-ss', '0', '-t', '10', split_video_path]
        subprocess.run(split_command, check=True)
        return f"影片 {video_path} 已分割成 {split_video_path}。"
    except Exception as e:
        return f"分割影片时发生错误: {e}"


# 建立 Gradio 界面
with gr.Blocks() as app:  # 修正这里，确保有变量名
    gr.Markdown("# 影片上载与拷贝")
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(label="上载影片", height=600, width=600)
        with gr.Column():
            output_message = gr.Textbox(label="消息显示框", interactive=False)
            convert_button = gr.Button("Convert")
            split_button = gr.Button("Split")
    video_input.change(fn=copy_video, inputs=video_input, outputs=output_message)
    convert_button.click(fn=convert_video, inputs=video_input, outputs=output_message)
    split_button.click(fn=split_video, inputs=video_input, outputs=output_message)

# 启动 Gradio 应用
if __name__ == "__main__":
    app.launch()
