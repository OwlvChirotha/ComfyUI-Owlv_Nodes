import os
import json
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import folder_paths


class SaveImageDir:
    # 临时文件夹名称
    TEMP_FOLDER_NAME = "save_image_dir_temp"
    
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
        # 确定保存目录和临时预览目录
        temp_folder_path = None
        subfolder = ""
        
        if use_custom_path and custom_path.strip():
            # 使用自定义路径（绝对路径）
            custom_output_folder = os.path.abspath(custom_path.strip())
            
            # 创建自定义目录
            try:
                os.makedirs(custom_output_folder, exist_ok=True)
            except Exception as e:
                print(f"[OwlV] Error creating directory {custom_output_folder}: {e}")
                # 如果创建失败，回退到默认路径
                custom_output_folder = None
                use_custom_path = False
            
            if custom_output_folder:
                # 准备临时预览文件夹
                temp_folder_path = os.path.join(self.output_dir, self.TEMP_FOLDER_NAME)
                self._prepare_temp_folder(temp_folder_path)
                subfolder = self.TEMP_FOLDER_NAME
                
                full_output_folder = custom_output_folder
                print(f"[OwlV] Saving images to custom path: {custom_output_folder}")
        else:
            # 使用ComfyUI默认路径
            full_output_folder = self.output_dir
            use_custom_path = False

        # 处理文件名模板
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
            
            # 保存主文件
            img.save(file_path, pnginfo=metadata, compress_level=self.compress_level)
            
            # 如果使用自定义路径，同时保存临时预览副本
            if use_custom_path and temp_folder_path:
                preview_file_path = os.path.join(temp_folder_path, file)
                img.save(preview_file_path, pnginfo=metadata, compress_level=self.compress_level)
            
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })

        return { "ui": { "images": results } }

    def _prepare_temp_folder(self, temp_path):
        """准备临时预览文件夹：创建、清理旧文件、生成说明文档"""
        # 创建临时文件夹
        os.makedirs(temp_path, exist_ok=True)
        
        # 清理旧的图像文件（保留README.txt）
        try:
            for filename in os.listdir(temp_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    file_path = os.path.join(temp_path, filename)
                    try:
                        os.remove(file_path)
                    except:
                        pass
        except Exception as e:
            print(f"[OwlV] Error cleaning temp folder: {e}")
        
        # 创建或更新README.txt说明文件
        readme_path = os.path.join(temp_path, "README.txt")
        readme_content = """[OwlV Temporary Preview Files]

这是 Save Image (Dir) 🦉| OwlV 节点的临时预览文件夹。

说明：
- 当启用自定义路径保存时，为了在节点面板显示预览，会在此文件夹保存临时副本
- 原始文件已保存到您指定的自定义路径中
- 此文件夹的文件会在每次运行时自动清理
- 最后一次运行的图像会保留在此文件夹中

管理建议：
- 可以不管它，隔段时间统一清理
- 也可以手动删除此文件夹（不影响自定义路径中的原始文件）
- 删除后节点会在下次运行时自动重新创建

--------------------
This is the temporary preview folder for Save Image (Dir) 🦉| OwlV node.

Note:
- When custom path is enabled, temporary copies are saved here for panel preview
- Original files are saved to your specified custom path
- Files in this folder are automatically cleaned on each run
- The last run's images will remain in this folder

Management Tips:
- You can ignore it and clean up periodically
- You can manually delete this folder (won't affect original files)
- The folder will be automatically recreated on next run
"""
        try:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)
        except:
            pass

    def get_counter(self):
        """获取计数器（避免文件名冲突）"""
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
        """获取日期字符串"""
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
