import os
import subprocess

def run_sadtalker(
    source_image="examples/source_image/full_body_1.png",  # 输入图片
    driven_audio="examples/driven_audio/bus_chinese.wav",     # 输入音频
    result_dir="results/mx150_test",                      # 输出目录
    enhancer="gfpgan",                                    # 面部增强
    still_mode=True,                                      # 适合头像模式
    pose_style=0,                                         # 姿态风格（0 ~ 46）
    size=256,                                             # 分辨率（256 更快，512 更清晰）
    # device="cuda"
):
    """
    运行 SadTalker 推理
    """

    command = [
        "python", "inference.py",
        "--driven_audio", driven_audio,
        "--source_image", source_image,
        "--result_dir", result_dir,
        "--enhancer", enhancer,
        "--size", str(size),
        # "--device", device,
    ]

    if still_mode:
        command.append("--still")

    if pose_style is not None:
        command.extend(["--pose_style", str(pose_style)])

    print("运行命令：", " ".join(command))

    subprocess.run(command)

if __name__ == "__main__":
    run_sadtalker()
