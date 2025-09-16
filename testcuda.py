import torch
print("CUDA 可用:", torch.cuda.is_available())
print("当前设备:", torch.cuda.current_device())
print("显卡名称:", torch.cuda.get_device_name(0))
