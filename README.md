# ComfyUI-Owlv_Nodes 🦉

[English](#english) | [简体中文](#简体中文)

---

## English

### Overview
A collection of custom utility nodes for ComfyUI, providing practical mini-tools with multiple functions.

### Node List

#### Save Image (Dir) 🦉| OwlV
An enhanced version of ComfyUI's official save_image node with custom export path support.

**Features:**
- ✅ Retains all functionality of the official save_image node
- ✅ Supports custom folder path (absolute path)
- ✅ Optional enable/disable switch for custom path
- ✅ Falls back to ComfyUI default behavior when disabled
- ✅ Supports PNG metadata (prompt, workflow info)
- ✅ Automatically creates directories if they don't exist
- ✅ Automatic file name conflict resolution
- ✅ Panel preview support with temporary copy mechanism
- ✅ Auto-cleanup of temporary preview files

**Input Parameters:**
- `images`: Images to save (required)
- `filename_prefix`: Filename prefix (default: "ComfyUI")
- `use_custom_path`: Enable custom path (boolean, default: False)
- `custom_path`: Custom folder path (string, supports absolute path)

**Usage:**
1. Add the node to your workflow
2. Connect the image input
3. To use a custom path:
   - Check `use_custom_path`
   - Enter an absolute path in `custom_path` (e.g., `D:\MyImages\Output`)
4. If `use_custom_path` is not checked, images will be saved to ComfyUI's default output folder

**About Temporary Preview Files:**
- When custom path is enabled, a temporary copy is created in `output/save_image_dir_temp/` for panel preview
- Original files are always saved to your specified custom path
- Temporary files are automatically cleaned on each run
- The last run's images will remain - you can clean them up manually or leave them be
- A `README.txt` file in the temp folder explains its purpose

### Installation

#### Method 1: Via ComfyUI Manager (Recommended)
1. Open ComfyUI Manager
2. Search for "ComfyUI-Owlv_Nodes" or "OwlV"
3. Click Install
4. Restart ComfyUI

#### Method 2: Manual Installation
1. Navigate to your ComfyUI's `custom_nodes` directory:
```bash
cd ComfyUI/custom_nodes
```

2. Clone this repository:
```bash
git clone https://github.com/OwlvChirotha/ComfyUI-Owlv_Nodes.git
```

3. Restart ComfyUI

4. Find the `Save Image (Dir) 🦉| OwlV` node in the `image` category

### Requirements
- ComfyUI base installation
- No additional dependencies required

### License
Please see the [LICENSE](LICENSE) file for details.

### Author
**OwlV** - [GitHub](https://github.com/OwlvChirotha)

### Support
If you encounter any issues or have suggestions, please open an issue on [GitHub Issues](https://github.com/OwlvChirotha/ComfyUI-Owlv_Nodes/issues).

---

## 简体中文

### 概述
ComfyUI自定义实用节点集合，提供多种实用的小工具和多功能节点。

### 节点列表

#### Save Image (Dir) 🦉| OwlV
在ComfyUI官方save_image节点的基础上，增加了自定义导出路径功能。

**功能特点：**
- ✅ 保留官方save_image的所有功能
- ✅ 支持自定义文件夹路径（绝对路径）
- ✅ 可选的启用/禁用开关
- ✅ 禁用时完全使用ComfyUI默认行为
- ✅ 支持PNG元数据（prompt、workflow信息）
- ✅ 自动创建不存在的目录
- ✅ 自动处理文件名冲突
- ✅ 支持节点面板预览（临时副本机制）
- ✅ 自动清理临时预览文件

**输入参数：**
- `images`: 要保存的图像（必需）
- `filename_prefix`: 文件名前缀（默认："ComfyUI"）
- `use_custom_path`: 是否启用自定义路径（布尔值，默认：False）
- `custom_path`: 自定义文件夹路径（字符串，支持绝对路径）

**使用说明：**
1. 将节点添加到工作流中
2. 连接图像输入
3. 如果需要使用自定义路径：
   - 勾选 `use_custom_path`
   - 在 `custom_path` 中输入绝对路径（例如：`D:\MyImages\Output`）
4. 如果不勾选 `use_custom_path`，将使用ComfyUI默认的output文件夹

**关于临时预览文件：**
- 启用自定义路径时，会在 `output/save_image_dir_temp/` 创建临时副本用于节点面板预览
- 原始文件始终保存在您指定的自定义路径中
- 临时文件会在每次运行时自动清理
- 最后一次运行的图像会保留 - 您可以手动清理或不管它
- 临时文件夹内有 `README.txt` 文件说明其用途

### 安装方法

#### 方法1：通过ComfyUI Manager安装（推荐）
1. 打开ComfyUI Manager
2. 搜索"ComfyUI-Owlv_Nodes"或"OwlV"
3. 点击安装
4. 重启ComfyUI

#### 方法2：手动安装
1. 进入ComfyUI的 `custom_nodes` 目录：
```bash
cd ComfyUI/custom_nodes
```

2. 克隆本仓库：
```bash
git clone https://github.com/OwlvChirotha/ComfyUI-Owlv_Nodes.git
```

3. 重启ComfyUI

4. 在节点菜单的 `image` 分类下找到 `Save Image (Dir) 🦉| OwlV` 节点

### 依赖要求
- ComfyUI基础安装
- 无需额外依赖

### 许可证
请查看 [LICENSE](LICENSE) 文件了解详情。

### 作者
**OwlV** - [GitHub](https://github.com/OwlvChirotha)

### 支持
如果您遇到任何问题或有建议，请在 [GitHub Issues](https://github.com/OwlvChirotha/ComfyUI-Owlv_Nodes/issues) 提交问题。
