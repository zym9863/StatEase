import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
# 导入中文字体配置
import font_config

def calculate_statistics(data):
    """计算描述性统计量并返回格式化的结果"""
    if len(data) == 0:
        return "数据为空"

    # 基本统计量计算
    count = len(data)
    mean = np.mean(data)
    median = np.median(data)
    std_dev = np.std(data)
    min_val = np.min(data)
    max_val = np.max(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    skewness = stats.skew(data)
    kurtosis = stats.kurtosis(data)

    # 检测异常值
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = [x for x in data if x < lower_bound or x > upper_bound]
    outlier_count = len(outliers)

    # 格式化结果为Markdown
    result = f"""### 描述性统计结果

| 统计量 | 值 |
|--------|----|
| 样本数 | {count} |
| 均值 | {mean:.4f} |
| 中位数 | {median:.4f} |
| 标准差 | {std_dev:.4f} |
| 最小值 | {min_val:.4f} |
| 最大值 | {max_val:.4f} |
| 第一四分位数 (Q1) | {q1:.4f} |
| 第三四分位数 (Q3) | {q3:.4f} |
| 四分位距 (IQR) | {iqr:.4f} |
| 偏度 | {skewness:.4f} |
| 峰度 | {kurtosis:.4f} |
| 异常值数量 | {outlier_count} |

### 数据解读

- **集中趋势**: 均值({mean:.2f})与中位数({median:.2f})的比较可反映数据分布的对称性
- **离散程度**: 标准差为{std_dev:.2f}，表示数据的波动/分散程度
- **分布形态**: """

    # 添加关于分布形态的解读
    if abs(skewness) < 0.5:
        result += "数据分布近似对称"
    elif skewness > 0.5:
        result += "数据呈现右偏（正偏）分布，有较长的右尾"
    else:  # skewness < -0.5
        result += "数据呈现左偏（负偏）分布，有较长的左尾"

    if kurtosis > 0.5:
        result += "，且峰度较高（尖峰分布）"
    elif kurtosis < -0.5:
        result += "，且峰度较低（平峰分布）"
    else:
        result += "，峰度接近正态分布"

    # 添加异常值信息
    if outlier_count > 0:
        result += f"\n- **异常值**: 检测到{outlier_count}个潜在异常值，可能需要进一步检查"
    else:
        result += "\n- **异常值**: 未检测到明显异常值"

    return result

def generate_histogram(data, title="数据分布"):
    """生成数据直方图"""
    fig, ax = plt.subplots(figsize=(8, 5))

    # 计算合适的bin数量 (Sturges规则)
    bins = int(np.ceil(np.log2(len(data)) + 1))

    # 绘制直方图和核密度估计
    ax.hist(data, bins=bins, density=True, alpha=0.7, color='#5B9BD5', label='频率分布')

    # 添加核密度估计曲线
    if len(data) > 2:  # 至少需要3个点才能计算KDE
        x = np.linspace(min(data), max(data), 100)
        kde = stats.gaussian_kde(data)
        ax.plot(x, kde(x), 'r-', linewidth=2, label='密度估计')

    # 添加均值和中位数线
    mean = np.mean(data)
    median = np.median(data)
    ax.axvline(mean, color='green', linestyle='dashed', linewidth=1.5, label=f'均值: {mean:.2f}')
    ax.axvline(median, color='red', linestyle='dashed', linewidth=1.5, label=f'中位数: {median:.2f}')

    # 设置图表标题和标签
    ax.set_title(f'{title}的直方图', fontsize=14)
    ax.set_xlabel('值', fontsize=12)
    ax.set_ylabel('频率密度', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def generate_boxplot(data, title="数据分布"):
    """生成箱线图"""
    fig, ax = plt.subplots(figsize=(8, 5))

    # 绘制箱线图
    boxplot = ax.boxplot(data, patch_artist=True, vert=False)

    # 设置箱线图颜色
    for patch in boxplot['boxes']:
        patch.set_facecolor('#5B9BD5')

    # 添加散点图展示数据分布
    y = np.random.normal(1, 0.04, size=len(data))
    ax.scatter(data, y, alpha=0.5, color='#333333')

    # 计算并标注统计量
    q1, median, q3 = np.percentile(data, [25, 50, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # 设置图表标题和标签
    ax.set_title(f'{title}的箱线图', fontsize=14)
    ax.set_xlabel('值', fontsize=12)
    ax.set_yticks([])

    # 添加统计量标注
    stats_text = f"中位数: {median:.2f}\nQ1: {q1:.2f}\nQ3: {q3:.2f}\nIQR: {iqr:.2f}"
    ax.text(0.02, 0.95, stats_text, transform=ax.transAxes,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    return fig