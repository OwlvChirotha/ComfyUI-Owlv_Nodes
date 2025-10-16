import os
import json
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import folder_paths


class SaveImageDir:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "optional": {
                "use_custom_path": ("BOOLEAN", {"default": False}),
                "custom_path": ("STRING", {"default": ""}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def save_images(self, images, filename_prefix="ComfyUI", use_custom_path=False, custom_path="", prompt=None, extra_pnginfo=None):
        # 确定保存目录
        if use_custom_path and custom_path.strip():
            # 使用自定义路径（绝对路径）
            full_output_folder = os.path.abspath(custom_path.strip())
            # 创建目录（如果不存在）
            try:
                os.makedirs(full_output_folder, exist_ok=True)
            except Exception as e:
                print(f"Error creating directory {full_output_folder}: {e}")
                # 如果创建失败，回退到默认路径
                full_output_folder = self.output_dir
        else:
            # 使用ComfyUI默认路径
            full_output_folder = self.output_dir

        filename_prefix = filename_prefix.replace("%width%", str(images[0].shape[1]))
        filename_prefix = filename_prefix.replace("%height%", str(images[0].shape[0]))
        filename_prefix = filename_prefix.replace("%date%", self.get_date_string())

        results = list()
        
        for (batch_number, image) in enumerate(images):
            # 转换图像格式
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            # 准备元数据
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            # 生成文件名
            filename_with_batch_num = filename_prefix.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{self.get_counter():05}_.png"
            
            # 完整文件路径
            file_path = os.path.join(full_output_folder, file)
            
            # 确保文件名唯一
            counter = 0
            while os.path.exists(file_path):
                counter += 1
                file = f"{filename_with_batch_num}_{self.get_counter():05}_{counter:02}.png"
                file_path = os.path.join(full_output_folder, file)
            
            # 保存图像
            img.save(file_path, pnginfo=metadata, compress_level=self.compress_level)
            
            results.append({
                "filename": file,
                "subfolder": "",
                "type": self.type
            })

        return { "ui": { "images": results } }

    def get_counter(self):
        # 获取计数器（避免文件名冲突）
        try:
            counter_file = os.path.join(self.output_dir, "counter.txt")
            if os.path.exists(counter_file):
                with open(counter_file, "r") as f:
                    counter = int(f.read().strip())
            else:
                counter = 0
            
            counter += 1
            
            with open(counter_file, "w") as f:
                f.write(str(counter))
            
            return counter
        except:
            # 如果计数器失败，使用时间戳
            import time
            return int(time.time() * 1000) % 100000

    def get_date_string(self):
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d")


# 简化版本 - 不依赖args
class args:
    disable_metadata = False


NODE_CLASS_MAPPINGS = {
    "SaveImageDir": SaveImageDir
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageDir": "Save Image (Dir) 🦉| OwlV"
}

