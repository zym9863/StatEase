import gradio as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import os
# 导入中文字体配置
import font_config
from data_processor import (
    calculate_statistics, generate_histogram, generate_boxplot,
    calculate_parameter_estimates, calculate_correlation
)


# 确保本地请求不经过代理，避免 Gradio 自检时触发 502
def ensure_local_no_proxy():
    """确保本地回环地址不走 HTTP/HTTPS 代理，避免 Gradio 启动自检 502。"""
    no_proxy_hosts = {"127.0.0.1", "localhost"}
    for key in ("NO_PROXY", "no_proxy"):
        existing = os.environ.get(key, "")
        hosts = {h.strip() for h in existing.split(',') if h.strip()}
        merged = ','.join(sorted(hosts.union(no_proxy_hosts)))
        os.environ[key] = merged


# 相关性示例数据文件路径
CORRELATION_EXAMPLE_FILE = 'example_data/correlation_example.csv'

# 创建示例数据
def create_example_data():
    # 确保示例数据目录存在
    os.makedirs('example_data', exist_ok=True)

    # 创建正态分布示例数据
    np.random.seed(42)
    normal_data = np.random.normal(loc=50, scale=10, size=100)
    pd.DataFrame(normal_data, columns=['value']).to_csv('example_data/normal_distribution.csv', index=False)

    # 创建偏态分布示例数据
    skewed_data = np.random.exponential(scale=10, size=100)
    pd.DataFrame(skewed_data, columns=['value']).to_csv('example_data/skewed_distribution.csv', index=False)

    # 创建双峰分布示例数据
    bimodal_data = np.concatenate([np.random.normal(loc=30, scale=5, size=50),
                                 np.random.normal(loc=70, scale=5, size=50)])
    pd.DataFrame(bimodal_data, columns=['value']).to_csv('example_data/bimodal_distribution.csv', index=False)

    # 创建相关性分析示例数据（正相关 + 轻微噪声）
    x = np.linspace(20, 80, 150)
    y = 2.5 * x + np.random.normal(scale=30, size=len(x))
    z = y + np.random.normal(scale=25, size=len(y))
    corr_df = pd.DataFrame({
        'study_hours': x,
        'exam_score': y,
        'practice_hours': z
    })
    corr_df.to_csv(CORRELATION_EXAMPLE_FILE, index=False)

    return ['example_data/normal_distribution.csv',
            'example_data/skewed_distribution.csv',
            'example_data/bimodal_distribution.csv']

# 确保示例数据存在
example_files = create_example_data()


def process_correlation_file(file):
    """从上传的CSV加载相关性分析数据"""
    if file is None:
        return "请先上传CSV文件", gr.update(choices=[], value=None), gr.update(choices=[], value=None), None

    df = pd.read_csv(file.name)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        return "需要至少两列数值列用于相关性分析", gr.update(choices=[], value=None), gr.update(choices=[], value=None), None

    default_x = numeric_cols[0]
    default_y = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
    return (
        f"已加载 {os.path.basename(file.name)}，请选择两列进行分析。",
        gr.update(choices=numeric_cols, value=default_x),
        gr.update(choices=numeric_cols, value=default_y),
        df
    )


def process_correlation_example():
    """加载预设的相关性示例数据"""
    df = pd.read_csv(CORRELATION_EXAMPLE_FILE)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    default_x = numeric_cols[0]
    default_y = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
    return (
        "已加载示例数据（study_hours, exam_score, practice_hours）",
        gr.update(choices=numeric_cols, value=default_x),
        gr.update(choices=numeric_cols, value=default_y),
        df
    )


def run_correlation_analysis(df, col_x, col_y, method):
    """执行相关性计算并返回结果"""
    if df is None:
        return "请先加载数据集", None
    if not col_x or not col_y:
        return "请选择要分析的两列", None
    if col_x == col_y:
        return "请选择不同的列进行相关性分析", None

    result, fig = calculate_correlation(df, col_x, col_y, method.lower())
    return result, fig

# 处理上传的CSV文件
def process_file(file):
    if file is None:
        return None, None, None

    df = pd.read_csv(file.name)
    # 只处理数值列
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        return "没有找到数值列", None, None

    # 默认选择第一个数值列
    selected_col = numeric_cols[0]
    data = df[selected_col].dropna().values

    stats = calculate_statistics(data)
    hist_fig = generate_histogram(data, selected_col)
    box_fig = generate_boxplot(data, selected_col)

    return stats, hist_fig, box_fig

# 处理手动输入的数据
def process_manual_input(text_input):
    if not text_input.strip():
        return "请输入数据", None, None

    try:
        # 尝试解析用户输入的数据（逗号、空格或换行符分隔）
        data = [float(x) for x in text_input.replace(',', ' ').split() if x.strip()]
        if not data:
            return "无法解析数据", None, None

        stats = calculate_statistics(np.array(data))
        hist_fig = generate_histogram(np.array(data), "输入数据")
        box_fig = generate_boxplot(np.array(data), "输入数据")

        return stats, hist_fig, box_fig
    except ValueError:
        return "数据格式错误，请确保输入的是数字，并用逗号、空格或换行符分隔", None, None

# 处理示例数据
def process_example(example_choice):
    if example_choice == "选择示例数据":
        return "请选择一个示例数据集", None, None

    file_path = example_choice
    df = pd.read_csv(file_path)
    data = df['value'].values

    stats = calculate_statistics(data)
    hist_fig = generate_histogram(data, os.path.basename(file_path).replace('.csv', ''))
    box_fig = generate_boxplot(data, os.path.basename(file_path).replace('.csv', ''))

    return stats, hist_fig, box_fig

# 处理参数估计
def process_parameter_estimation(text_input, estimate_type, confidence_level, threshold=None):
    if not text_input.strip():
        return "请输入数据"

    try:
        # 尝试解析用户输入的数据（逗号、空格或换行符分隔）
        data = [float(x) for x in text_input.replace(',', ' ').split() if x.strip()]
        if not data:
            return "无法解析数据"

        # 转换置信水平为小数
        confidence_level_value = float(confidence_level.strip('%')) / 100

        # 处理均值估计
        if estimate_type == "均值估计":
            result = calculate_parameter_estimates(
                np.array(data),
                'mean',
                confidence_level_value
            )
        # 处理比例估计
        else:  # estimate_type == "比例估计"
            # 如果提供了阈值
            if threshold is not None and threshold.strip():
                try:
                    threshold_value = float(threshold)
                    result = calculate_parameter_estimates(
                        np.array(data),
                        'proportion',
                        confidence_level_value,
                        threshold_value
                    )
                except ValueError:
                    return "阈值格式错误，请输入有效的数字"
            # 如果没有提供阈值，使用数据的中位数作为默认阈值
            else:
                result = calculate_parameter_estimates(
                    np.array(data),
                    'proportion',
                    confidence_level_value
                )
                return f"注意：未提供阈值，系统自动使用数据的中位数作为阈值。\n\n{result}"

        return result
    except ValueError:
        return "数据格式错误，请确保输入的是数字，并用逗号、空格或换行符分隔"

# 创建Gradio界面
with gr.Blocks(title="StatEase - 简易统计分析工具") as app:
    gr.Markdown("# StatEase - 简易统计分析工具")
    gr.Markdown("上传数据集、手动输入数据或选择示例数据，快速获取描述性统计结果。")

    with gr.Tabs():
        with gr.TabItem("上传数据"):
            file_input = gr.File(label="上传CSV文件")
            upload_button = gr.Button("分析")
            upload_output = gr.Markdown(label="统计结果")
            with gr.Row():
                hist_output1 = gr.Plot(label="直方图")
                box_output1 = gr.Plot(label="箱线图")

            upload_button.click(
                fn=process_file,
                inputs=[file_input],
                outputs=[upload_output, hist_output1, box_output1]
            )

        with gr.TabItem("手动输入"):
            text_input = gr.Textbox(
                label="输入数据（用逗号、空格或换行符分隔）",
                placeholder="例如: 1, 2, 3, 4, 5",
                lines=5
            )
            manual_button = gr.Button("分析")
            manual_output = gr.Markdown(label="统计结果")
            with gr.Row():
                hist_output2 = gr.Plot(label="直方图")
                box_output2 = gr.Plot(label="箱线图")

            manual_button.click(
                fn=process_manual_input,
                inputs=[text_input],
                outputs=[manual_output, hist_output2, box_output2]
            )

        with gr.TabItem("示例数据"):
            example_dropdown = gr.Dropdown(
                ["选择示例数据"] + [os.path.basename(f) for f in example_files],
                label="选择示例数据集",
                value="选择示例数据"
            )
            example_button = gr.Button("分析")
            example_output = gr.Markdown(label="统计结果")
            with gr.Row():
                hist_output3 = gr.Plot(label="直方图")
                box_output3 = gr.Plot(label="箱线图")

            # 映射下拉菜单选项到文件路径
            def map_example_choice(choice):
                if choice == "选择示例数据":
                    return choice
                for f in example_files:
                    if os.path.basename(f) == choice:
                        return f
                return choice

            example_button.click(
                fn=lambda x: process_example(map_example_choice(x)),
                inputs=[example_dropdown],
                outputs=[example_output, hist_output3, box_output3]
            )

        with gr.TabItem("相关性分析"):
            corr_state = gr.State()
            gr.Markdown("选择两列数值数据，计算 Pearson 或 Spearman 相关系数，并查看散点图与拟合线。")

            with gr.Row():
                corr_file = gr.File(label="上传CSV文件（至少包含两列数值列）")
                load_corr_btn = gr.Button("从上传文件加载")
                load_corr_example_btn = gr.Button("使用示例数据")

            corr_status = gr.Markdown("等待加载数据…")

            with gr.Row():
                corr_col_x = gr.Dropdown(label="X轴列", choices=[], interactive=True)
                corr_col_y = gr.Dropdown(label="Y轴列", choices=[], interactive=True)

            corr_method = gr.Radio(
                ["Pearson", "Spearman"],
                label="相关性方法",
                value="Pearson"
            )

            calc_corr_btn = gr.Button("计算相关性")
            corr_output = gr.Markdown(label="相关性结果")
            corr_plot = gr.Plot(label="散点图与回归线")

            load_corr_btn.click(
                fn=process_correlation_file,
                inputs=[corr_file],
                outputs=[corr_status, corr_col_x, corr_col_y, corr_state]
            )

            load_corr_example_btn.click(
                fn=process_correlation_example,
                inputs=[],
                outputs=[corr_status, corr_col_x, corr_col_y, corr_state]
            )

            calc_corr_btn.click(
                fn=run_correlation_analysis,
                inputs=[corr_state, corr_col_x, corr_col_y, corr_method],
                outputs=[corr_output, corr_plot]
            )

        with gr.TabItem("参数估计"):
            param_text_input = gr.Textbox(
                label="输入数据（用逗号、空格或换行符分隔）",
                placeholder="例如: 1, 2, 3, 4, 5",
                lines=5
            )
            with gr.Row():
                estimate_type = gr.Radio(
                    ["均值估计", "比例估计"],
                    label="估计类型",
                    value="均值估计"
                )
                confidence_level = gr.Dropdown(
                    ["90%", "95%", "99%"],
                    label="置信水平",
                    value="95%"
                )

            # 阈值输入框（初始状态下隐藏）
            threshold_input = gr.Textbox(
                label="阈值（仅用于比例估计，大于等于此值视为'成功'）",
                placeholder="例如: 50",
                visible=False,
                interactive=True
            )

            # 当估计类型改变时，控制阈值输入框的显示/隐藏
            def update_threshold_visibility(estimate_type_value):
                return gr.update(visible=(estimate_type_value == "比例估计"))

            estimate_type.change(
                fn=update_threshold_visibility,
                inputs=[estimate_type],
                outputs=[threshold_input]
            )

            param_button = gr.Button("计算参数估计")
            param_output = gr.Markdown(label="参数估计结果")

            param_button.click(
                fn=process_parameter_estimation,
                inputs=[param_text_input, estimate_type, confidence_level, threshold_input],
                outputs=[param_output]
            )

    gr.Markdown("""
    ## 使用说明
    1. **上传数据**: 上传CSV格式的数据文件进行分析
    2. **手动输入**: 直接输入数据值，用逗号、空格或换行符分隔
    3. **示例数据**: 选择预设的示例数据集进行分析
    4. **参数估计**: 计算样本均值和比例的点估计与区间估计
       - 均值估计: 计算样本均值及其置信区间
       - 比例估计: 计算样本比例及其置信区间（需设置阈值）
       - 可选择不同的置信水平（90%、95%、99%）

    分析结果包括基本统计量（均值、中位数、标准差等）、数据可视化和参数估计。
    """)

# 启动应用
if __name__ == "__main__":
    ensure_local_no_proxy()
    default_port = int(os.getenv("PORT", "7860"))

    # 检查是否在Hugging Face Spaces环境中运行
    if os.getenv("SPACE_ID"):
        # 如果在Hugging Face Spaces环境中运行，使用特定配置
        app.launch(
            share=False,
            server_name="0.0.0.0",
            server_port=default_port,
            show_error=True,
            inbrowser=False
        )
    else:
        # 本地运行配置
        app.launch(
            share=False,
            server_name=os.getenv("SERVER_NAME", "127.0.0.1"),
            server_port=default_port,
            show_error=True
        )