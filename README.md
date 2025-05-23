# StatEase - 简易统计分析工具

[English](README_EN.md) | 简体中文

StatEase是一个基于Python和Gradio的简易统计分析工具，专注于提供数据的描述性统计功能。该工具允许用户通过上传数据集、手动输入数据或选择示例数据来快速获取统计分析结果。

## 功能特点

- **多种数据输入方式**：
  - 上传CSV文件
  - 手动输入数据
  - 选择预设示例数据

- **全面的描述性统计**：
  - 基本统计量（均值、中位数、标准差等）
  - 分布特征（偏度、峰度）
  - 异常值检测

- **参数估计**：
  - 点估计（样本均值、样本比例）
  - 区间估计（均值的置信区间、比例的置信区间）
  - 可选择不同的置信水平（90%、95%、99%）

- **数据可视化**：
  - 直方图（带核密度估计）
  - 箱线图（带数据点分布）

## 安装与运行

### 本地运行

1. 克隆或下载本仓库

2. 创建并激活虚拟环境（推荐）
   ```bash
   # 创建虚拟环境
   python -m venv venv

   # 激活虚拟环境（Windows）
   venv\Scripts\activate

   # 激活虚拟环境（Linux/Mac）
   source venv/bin/activate
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 运行应用
   ```bash
   python app.py
   ```

5. 在浏览器中访问显示的URL（通常是 http://127.0.0.1:7860）

### Hugging Face Spaces部署

本项目可以直接部署到Hugging Face Spaces：

1. 在Hugging Face上创建一个新的Space
2. 选择Gradio作为SDK
3. 上传项目文件
4. Space会自动安装依赖并启动应用

## 使用指南

### 上传数据

1. 切换到"上传数据"选项卡
2. 点击上传按钮选择CSV文件
3. 点击"分析"按钮获取结果

### 手动输入数据

1. 切换到"手动输入"选项卡
2. 在文本框中输入数据，用逗号、空格或换行符分隔
3. 点击"分析"按钮获取结果

### 使用示例数据

1. 切换到"示例数据"选项卡
2. 从下拉菜单中选择一个示例数据集
3. 点击"分析"按钮获取结果

### 参数估计

1. 切换到"参数估计"选项卡
2. 在文本框中输入数据，用逗号、空格或换行符分隔
3. 选择估计类型（均值估计或比例估计）
4. 选择置信水平（90%、95%或99%）
5. 如果选择比例估计，还需要输入阈值（大于等于此值视为"成功"）
6. 点击"计算参数估计"按钮获取结果