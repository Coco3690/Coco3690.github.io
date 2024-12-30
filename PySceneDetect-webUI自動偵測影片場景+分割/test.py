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


if __name__ == "__main__":
    # 调用函数，将 'your_video.mp4' 替换为你要处理的视频文件的实际路径
    split_video_into_scenes('video.mp4')