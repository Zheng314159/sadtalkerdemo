SadTalker 参数推荐表（适配 NVIDIA GeForce MX150）
1. ⚡快速出结果（测试/预览用）

分辨率：--size 256

batch_size：1

pose_style：0（只动嘴巴）

preprocess：crop

GFPGAN：关闭（不要 --enhancer）

音频：10 秒以内

👉 优点：生成速度最快，几十秒出结果；缺点：清晰度一般。

2. 🎥 高清效果（演示/出片用）

分辨率：--size 256（MX150 不建议 512，基本会爆显存）

batch_size：1

pose_style：5 ~ 10（自然一点的头部动作）

preprocess：extcrop（保留肩膀和部分背景，画面更自然）

GFPGAN：建议开启（--enhancer gfpgan），改善人脸模糊

音频：≤ 30 秒（太长会拖慢速度）

👉 优点：画面比较自然，嘴型清晰；缺点：生成会慢一些。

3. 🖼 稳定嘴型模式（类似电子相册“开口说话”）

分辨率：--size 256

batch_size：1

pose_style：0（保持头部基本静止）

preprocess：full 或 extfull（整张图保留）

Still Mode：开启 --still

GFPGAN：可选，清晰度不足时打开

👉 优点：嘴型同步好，头部不会乱动；缺点：表情僵硬。

python .\inference.py ^
  --driven_audio F:\SadTalker\examples\driven_audio\bus_chinese.wav ^
  --source_image F:\SadTalker\examples\source_image\art_6.png ^
  --result_dir results ^
  --pose_style 0 ^
  --batch_size 1 ^
  --size 256 ^
  --preprocess crop
提醒

避免长音频：MX150 跑 1 分钟音频可能要 5~10 分钟甚至更久。建议先用短音频测试。

确认 GPU 是否在跑：生成时开 nvidia-smi，看显存是否有占用（~1500MB 左右）。

GFPGAN 很耗时：建议只在出片时开，平时调试关掉。