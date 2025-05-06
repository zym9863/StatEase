import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import math
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

def calculate_mean_confidence_interval(data, confidence_level=0.95):
    """
    计算样本均值的置信区间

    参数:
    - data: 数据数组
    - confidence_level: 置信水平，默认为0.95 (95%)

    返回:
    - 均值点估计和置信区间的Markdown格式结果
    """
    if len(data) < 2:
        return "样本量不足，无法计算置信区间（至少需要2个观测值）"

    # 计算样本均值（点估计）
    mean = np.mean(data)

    # 计算样本标准差
    std_dev = np.std(data, ddof=1)  # 使用无偏估计 (n-1)

    # 样本量
    n = len(data)

    # 计算标准误
    std_error = std_dev / math.sqrt(n)

    # 计算t临界值
    alpha = 1 - confidence_level
    t_critical = stats.t.ppf(1 - alpha/2, df=n-1)

    # 计算置信区间
    margin_of_error = t_critical * std_error
    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error

    # 格式化结果为Markdown
    result = f"""### 均值的参数估计 (置信水平: {confidence_level*100:.0f}%)

| 估计类型 | 值 |
|--------|----|
| 样本均值 (点估计) | {mean:.4f} |
| 标准误 | {std_error:.4f} |
| 置信区间下限 | {lower_bound:.4f} |
| 置信区间上限 | {upper_bound:.4f} |
| 误差幅度 | ±{margin_of_error:.4f} |

### 解读

- **点估计**: 样本均值 {mean:.4f} 是总体均值的最佳单点估计
- **置信区间**: 以 {confidence_level*100:.0f}% 的置信水平，总体均值落在区间 [{lower_bound:.4f}, {upper_bound:.4f}] 内
- **精确度**: 误差幅度为 ±{margin_of_error:.4f}，样本量越大，区间越窄，估计越精确
"""

    return result

def calculate_proportion_confidence_interval(data, threshold, confidence_level=0.95):
    """
    计算样本比例的置信区间

    参数:
    - data: 数据数组
    - threshold: 阈值，用于确定成功/失败（大于等于阈值为成功）
    - confidence_level: 置信水平，默认为0.95 (95%)

    返回:
    - 比例点估计和置信区间的Markdown格式结果
    """
    if len(data) < 30:
        return "样本量不足，建议使用至少30个观测值来估计比例的置信区间"

    # 计算样本比例（点估计）
    successes = sum(1 for x in data if x >= threshold)
    n = len(data)
    p_hat = successes / n

    # 计算标准误
    std_error = math.sqrt((p_hat * (1 - p_hat)) / n)

    # 计算z临界值
    alpha = 1 - confidence_level
    z_critical = stats.norm.ppf(1 - alpha/2)

    # 计算置信区间
    margin_of_error = z_critical * std_error
    lower_bound = max(0, p_hat - margin_of_error)  # 确保下限不小于0
    upper_bound = min(1, p_hat + margin_of_error)  # 确保上限不大于1

    # 格式化结果为Markdown
    result = f"""### 比例的参数估计 (置信水平: {confidence_level*100:.0f}%)

| 估计类型 | 值 |
|--------|----|
| 阈值 | {threshold:.4f} |
| 样本比例 (点估计) | {p_hat:.4f} ({successes}/{n}) |
| 标准误 | {std_error:.4f} |
| 置信区间下限 | {lower_bound:.4f} |
| 置信区间上限 | {upper_bound:.4f} |
| 误差幅度 | ±{margin_of_error:.4f} |

### 解读

- **点估计**: 样本中 {p_hat*100:.1f}% 的观测值大于等于阈值 {threshold:.4f}
- **置信区间**: 以 {confidence_level*100:.0f}% 的置信水平，总体比例落在区间 [{lower_bound:.4f}, {upper_bound:.4f}] 内
- **精确度**: 误差幅度为 ±{margin_of_error:.4f}，样本量越大，区间越窄，估计越精确
"""

    return result

def calculate_parameter_estimates(data, estimate_type, confidence_level=0.95, threshold=None):
    """
    计算参数估计（点估计和区间估计）

    参数:
    - data: 数据数组
    - estimate_type: 估计类型 ('mean' 或 'proportion')
    - confidence_level: 置信水平，默认为0.95 (95%)
    - threshold: 用于比例估计的阈值，仅当estimate_type='proportion'时使用

    返回:
    - 参数估计的Markdown格式结果
    """
    if len(data) == 0:
        return "数据为空，无法进行参数估计"

    if estimate_type == 'mean':
        return calculate_mean_confidence_interval(data, confidence_level)
    elif estimate_type == 'proportion':
        if threshold is None:
            # 如果未提供阈值，使用数据的中位数作为默认阈值
            threshold = np.median(data)
        return calculate_proportion_confidence_interval(data, threshold, confidence_level)
    else:
        return f"不支持的估计类型: {estimate_type}。请选择 'mean' 或 'proportion'。"