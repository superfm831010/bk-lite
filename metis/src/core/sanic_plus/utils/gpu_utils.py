class GpuUtils:
    @staticmethod
    def choose_model_device():
        import torch
        num_gpus = torch.cuda.device_count()
        device = "cuda" if num_gpus > 0 else "cpu"
        return device
