# Brother DCP-7180DN 打印程序依赖安装说明

## 简介
本程序需要额外的Python库来支持PDF转换功能。以下是安装所需依赖的步骤。

## 安装依赖

### 1. 安装weasyprint（用于HTML到PDF转换）
```bash
pip install weasyprint
```

### 2. 安装Pillow（用于图片到PDF转换）
```bash
pip install Pillow
```

## Windows系统特殊说明

### weasyprint安装困难的原因：
- weasyprint依赖GTK+图形库，Windows上安装复杂
- 需要安装GTK+运行时环境或使用预编译版本
- 常见错误：`OSError: cannot load library 'libgobject-2.0-0'`

### 推荐的Windows安装方法：

#### 方法1：使用预编译版本（推荐）
```bash
pip install weasyprint --only-binary=all
```

#### 方法2：使用conda（如果已安装Anaconda/Miniconda）
```bash
conda install -c conda-forge weasyprint
```

#### 方法3：使用Windows Subsystem for Linux (WSL)
在WSL中安装：
```bash
sudo apt-get update
sudo apt-get install libgobject-2.0-0
pip install weasyprint
```

## 安装说明

### Windows系统：
1. 打开命令提示符（CMD）或PowerShell
2. 运行以下命令安装依赖：
```bash
pip install weasyprint Pillow
```

### Linux/Mac系统：
1. 打开终端
2. 运行以下命令安装依赖：
```bash
pip install weasyprint Pillow
```

## 注意事项

1. **weasyprint依赖**：
   - weasyprint需要系统安装GTK+库
   - Windows用户可能需要安装GTK+运行时环境
   - 推荐使用Python 3.7+版本

2. **Pillow依赖**：
   - Pillow是纯Python库，通常容易安装
   - 如果遇到编译问题，可以尝试：
   ```bash
   pip install --upgrade pip
   pip install Pillow
   ```

3. **程序兼容性**：
   - 即使没有安装weasyprint，程序仍可正常工作
   - 没有weasyprint时，程序会直接打印原始文件
   - 对于Word文档(.docx)，程序会尝试直接发送，但可能需要打印机支持

## 验证安装

安装完成后，可以通过以下命令验证：
```bash
python -c "from weasyprint import HTML; print('weasyprint installed successfully')"
python -c "from PIL import Image; print('Pillow installed successfully')"
```

## 故障排除

如果安装过程中遇到问题：

1. **权限问题**：
   ```bash
   pip install --user weasyprint Pillow
   ```

2. **网络问题**：
   ```bash
   pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org weasyprint Pillow
   ```

3. **升级pip**：
   ```bash
   python -m pip install --upgrade pip
   ```

4. **使用国内镜像源**（如果网络慢）：
   ```bash
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple weasyprint Pillow
   ```

## 替代方案

如果无法安装weasyprint，程序仍然可以正常工作：
- 文本文件会直接打印
- PDF文件会直接打印
- 图片文件会直接打印
- 其他格式文件会尝试作为文本处理

安装完成后，重启程序即可正常使用PDF转换功能。
