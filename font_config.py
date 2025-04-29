import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import os
import sys
import urllib.request
from matplotlib.font_manager import FontProperties, findfont, FontManager, get_font_names
import shutil

def download_chinese_font():
    """
    下载中文字体并安装到matplotlib字体目录
    """
    # 创建字体目录
    font_dir = os.path.join(os.path.expanduser('~'), '.matplotlib', 'fonts', 'ttf')
    os.makedirs(font_dir, exist_ok=True)

    # 下载字体的URL (使用开源中文字体)
    font_url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansSC-Regular.otf"
    font_path = os.path.join(font_dir, "NotoSansSC-Regular.otf")

    # 如果字体已存在，则不下载
    if os.path.exists(font_path):
        print(f"中文字体已存在: {font_path}")
        return font_path

    try:
        print(f"正在下载中文字体...")
        urllib.request.urlretrieve(font_url, font_path)
        print(f"字体下载成功: {font_path}")

        # 清除matplotlib字体缓存
        cache_dir = mpl.get_cachedir()
        cache_file = os.path.join(cache_dir, 'fontlist-v330.json')
        if os.path.exists(cache_file):
            os.remove(cache_file)

        # 重新加载字体管理器
        font_manager = FontManager()
        font_manager.findfont('sans-serif')

        return font_path
    except Exception as e:
        print(f"字体下载失败: {e}")
        return None

def check_chinese_font_availability():
    """
    检查系统是否有可用的中文字体
    """
    # 测试字符串
    test_str = "测试中文字体"

    # 获取当前默认字体
    default_font = findfont(FontProperties(family=['sans-serif']))

    # 检查是否为后备字体
    is_fallback = 'DejaVuSans.ttf' in default_font

    if is_fallback:
        print("系统没有检测到合适的中文字体，将尝试使用备选方案")
        return False
    else:
        print(f"检测到可用的中文字体: {os.path.basename(default_font)}")
        return True

def configure_chinese_font():
    """
    配置matplotlib以正确显示中文字符
    根据不同操作系统自动选择合适的中文字体
    """
    system = platform.system()

    if system == 'Windows':
        # Windows系统常见中文字体
        font_list = ['Microsoft YaHei', 'SimHei', 'SimSun', 'NSimSun', 'FangSong', 'KaiTi']
    elif system == 'Darwin':  # macOS
        # macOS系统常见中文字体
        font_list = ['PingFang SC', 'Heiti SC', 'STHeiti', 'STSong', 'STFangsong']
    else:  # Linux和其他系统
        # Linux系统常见中文字体
        font_list = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'Noto Sans CJK TC', 'Droid Sans Fallback']

    # 尝试设置字体
    font_found = False
    for font in font_list:
        try:
            # 尝试创建字体属性对象，如果成功则表示字体存在
            font_prop = FontProperties(family=font)
            font_path = findfont(font_prop)

            # 如果找到了字体（不是后备字体）
            if not ('DejaVuSans.ttf' in font_path):
                # 设置matplotlib的字体
                plt.rcParams['font.family'] = 'sans-serif'
                plt.rcParams['font.sans-serif'] = [font] + plt.rcParams['font.sans-serif']
                print(f"成功设置中文字体: {font}")
                font_found = True
                break
        except:
            continue

    # 如果没有找到合适的字体，尝试下载并安装中文字体
    if not font_found:
        try:
            # 设置sans-serif字体族
            plt.rcParams['font.family'] = 'sans-serif'

            # 在sans-serif字体族中添加一些可能支持中文的字体
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans', 'Bitstream Vera Sans', 'Lucida Sans Unicode'] + font_list

            # 尝试下载中文字体
            font_path = download_chinese_font()
            if font_path and os.path.exists(font_path):
                # 添加下载的字体到sans-serif列表的最前面
                plt.rcParams['font.sans-serif'].insert(0, 'Noto Sans SC')
                font_found = True
            else:
                print("使用sans-serif字体族，但可能无法正确显示中文")
        except Exception as e:
            print(f"设置字体时出错: {e}")
            print("警告: 无法设置合适的中文字体，可能导致中文显示为方块")

    # 修复负号显示问题
    plt.rcParams['axes.unicode_minus'] = False

    # 设置全局字体大小
    plt.rcParams['font.size'] = 12

    return font_found

# 在导入模块时自动配置字体
configure_chinese_font()
