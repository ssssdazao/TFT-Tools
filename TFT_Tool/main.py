import streamlit as st
import pandas as pd
from analyzer import TFTAnalyzer
import time
from pathlib import Path

# Set page config
st.set_page_config(page_title="装备助手", page_icon="🛠️", layout="wide", initial_sidebar_state="expanded")

# --- 全局样式与背景设置 ---
def get_base64_of_bin_file(bin_file):
    import base64
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_and_style():
    import os
    
    # 尝试加载本地背景 bg.jpg
    bg_style = ""
    try:
        bg_path = Path(__file__).resolve().parent / "bg.jpg"
        if bg_path.exists():
            bg_base64 = get_base64_of_bin_file(str(bg_path))
            bg_style = f"""
            background-image: url("data:image/jpeg;base64,{bg_base64}");
            """
        else:
            # 默认在线图片
            bg_style = """
            background-image: url("https://images.wallpapersden.com/image/download/anime-school-classroom-sunset_bGdnaGuUmZqaraWkpJRmbmdlrWZlbWU.jpg");
            """
    except Exception as e:
        st.error(f"加载背景图失败: {e}")
        bg_style = """
        background-color: #2e3047;
        """

    st.markdown(f"""
    <style>
        /* 引入艺术字体 */
        @import url('https://fonts.googleapis.com/css2?family=Zcool+KuaiLe&family=Nunito:wght@400;700&display=swap');

        /* 增强全局字体清晰度 - 强制浅色 */
        body, p, li, span, div {{
            color: #ffffff;
        }}
        
        /* 针对 Streamlit Markdown 文本的增强 */
        .stMarkdown p, .stMarkdown li {{
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.8); /* 增加文字阴影，防止背景过亮看不清 */
            font-weight: 500;
        }}
        
        /* 输入框 Label 增强 */
        .stSelectbox label, .stNumberInput label, .stTextInput label, .stSlider label {{
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.9);
            font-weight: 600 !important;
            font-size: 1rem !important;
        }}

        /* 侧边栏文字增强 */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {{
            color: #ffffff !important;
        }}

        /* 1. 全局背景设置 */
        .stApp {{
            {bg_style}
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            font-family: 'Nunito', sans-serif;
        }}
        
        /* 2. 隐藏 Streamlit 默认元素 */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* 3. 侧边栏与导航 */
        section[data-testid="stSidebar"] {{
            visibility: visible !important;
            display: block !important;
            background: rgba(18, 18, 30, 0.52) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.10) !important;
        }}
        section[data-testid="stSidebar"] > div {{
            background: transparent !important;
        }}
        div[data-testid="stSidebarNav"] {{
            display: none !important;
        }}
        div[data-testid="stSidebarNav"] a {{
            border-radius: 12px !important;
        }}
        div[data-testid="stSidebarNav"] a:hover {{
            background: rgba(255, 255, 255, 0.08) !important;
        }}
        div[data-testid="stSidebarNav"] span {{
            font-weight: 700 !important;
        }}
        
        /* 4. 全局玻璃背景板 (Fixed Glass Overlay) */
        .main-glass {{
            position: fixed;
            top: 10vh;
            left: 2vw;
            width: 96vw;
            height: 80vh;
            background: rgba(20, 20, 35, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            z-index: 0; /* 确保在背景图之上，但在内容之下（配合内容z-index调整） */
            pointer-events: none; /* 让点击穿透，不影响操作 */
            animation: fadeIn 0.8s ease-in-out;
        }}
        
        /* 调整主内容区域，使其位于玻璃板之上 */
        [data-testid="block-container"] {{
            z-index: 1;
            position: relative;
            padding-top: 50px !important; /* 避免内容顶到玻璃板边缘 */
        }}

        /* 动画定义 */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* 5. 标题样式 - 强烈的个人风格 */
        .main-title {{
            font-family: 'Zcool KuaiLe', sans-serif; /* 快乐体，更有动漫感 */
            font-size: 3.5rem;
            background: linear-gradient(120deg, #ff9a9e 0%, #fecfef 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 4px 15px rgba(255, 100, 100, 0.3);
            text-align: center;
            margin-bottom: 0.2rem;
        }}
        .subtitle {{
            font-family: 'Nunito', sans-serif;
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.85);
            text-align: center;
            letter-spacing: 1px;
            margin-bottom: 30px;
        }}

        /* 5. 输入组件美化 */
        .stSelectbox > div > div {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            color: #fff !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 12px !important;
            height: 48px;
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
        }}
        .stSelectbox > div > div:hover {{
            border-color: #ff9a9e !important;
            background-color: rgba(255, 255, 255, 0.15) !important;
        }}
        /* 下拉菜单颜色 - 保持默认背景（通常是白色），仅修改字体 */
        ul[data-baseweb="menu"] {{
            border-radius: 12px !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
        }}
        /* 下拉菜单选项文字颜色 - 改为深色 */
        ul[data-baseweb="menu"] li {{
            color: #000000 !important;
            background-color: transparent !important;
            font-weight: 600 !important;
        }}
        ul[data-baseweb="menu"] li:hover {{
            background-color: rgba(0, 0, 0, 0.05) !important;
            color: #000000 !important;
        }}

        /* 6. 按钮美化 - 渐变夕阳色 */
        .stButton > button {{
            background: linear-gradient(45deg, #FF9A9E 0%, #FECFEF 99%, #FECFEF 100%);
            color: #555;
            border: none;
            border-radius: 12px;
            padding: 0.6rem 2rem;
            font-size: 1rem;
            font-weight: 700;
            box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
            transition: all 0.3s ease;
            height: 48px;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 25px rgba(255, 154, 158, 0.6);
            color: #333;
        }}

        /* 7. 结果卡片样式 */
        .item-container {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 15px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }}
        .item-container:hover {{
            background: rgba(255, 255, 255, 0.15);
            transform: translateX(5px);
            border-color: rgba(255, 255, 255, 0.3);
        }}
        .item-img {{
            width: 56px;
            height: 56px;
            border-radius: 10px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .item-names {{
            font-size: 1.05rem;
            color: #fff;
            font-weight: 500;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        .stats-info {{
            margin-left: auto;
            text-align: right;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.8);
        }}
        .stat-value {{
            font-weight: 700;
            color: #FF9A9E; /* 与主题色呼应 */
            font-size: 1.1rem;
        }}
    </style>
    """, unsafe_allow_html=True)

set_bg_and_style()
st.markdown('<div class="main-glass"></div>', unsafe_allow_html=True)

def _app_dir_name():
    p = Path(__file__).resolve()
    if p.parent.name.lower() == "pages":
        return p.parents[1].name
    return p.parent.name


def _nav_link(path: str, label: str, icon: str):
    app_dir = _app_dir_name()
    candidates = [path, f"{app_dir}/{path}"]
    for c in candidates:
        try:
            st.page_link(c, label=label, icon=icon)
            return
        except Exception:
            pass
    if st.button(f"{icon} {label}", use_container_width=True):
        for c in candidates:
            try:
                st.switch_page(c)
                return
            except Exception:
                pass


with st.sidebar:
    st.markdown("### 导航")
    _nav_link("main.py", label="装备助手", icon="🛠️")
    _nav_link("pages/1_Battle_Simulator.py", label="战斗模拟", icon="⚔️")

# 统一的大玻璃容器开始
# st.markdown('<div class="glass-container" style="padding: 40px;">', unsafe_allow_html=True)

# Title Area
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <div class="main-title">TFT 装备助手</div>
    <div class="subtitle">流淅</div>
</div>
""", unsafe_allow_html=True)

# Initialize Analyzer
@st.cache_resource
def get_analyzer():
    return TFTAnalyzer()

try:
    analyzer = get_analyzer()
    
    # 自动检测实例是否过期 (处理代码更新后的缓存问题)
    if not hasattr(analyzer.fetcher, '_item_map'):
        st.cache_resource.clear()
        analyzer = get_analyzer()
        
    st.sidebar.success(f"数据源连接成功! 已加载 {len(analyzer.champions)} 个英雄数据。")
    
    # Debug: Show Data Stats
    # 确保 _item_map 存在后再访问
    item_count = len(analyzer.fetcher._item_map) if hasattr(analyzer.fetcher, '_item_map') else 0
    st.sidebar.write(f"已加载装备: {item_count}")
    
    if st.sidebar.button("🧹 清除缓存并重载数据"):
        st.cache_resource.clear()
        st.rerun()
        
except Exception as e:
    st.sidebar.error(f"数据源连接失败: {e}")
    # 如果出错，提供一个强制重置按钮
    if st.sidebar.button("⚠️ 强制重置"):
        st.cache_resource.clear()
        st.rerun()
    st.stop()

# User Input
# 获取所有英雄名称用于下拉选择
all_champs = sorted([c.get('displayName') for c in analyzer.champions])

# 容器化输入区域，应用 Glassmorphism
# 使用 CSS 注入来覆盖 Streamlit 默认的 container 样式，或者直接在这里包裹一层 div
st.markdown("""
<div style="margin-bottom: 10px; font-weight: bold; color: #eee;">选择或搜索英雄：</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    # index=None 默认不选中
    selected_champ = st.selectbox(
        "选择或搜索英雄（隐藏标签）", # label_visibility="collapsed" 会隐藏这个标签
        all_champs, 
        index=None, 
        placeholder="例如：金克丝 (支持拼音/汉字搜索)",
        label_visibility="collapsed"
    )

with col2:
    # st.write("") # Spacer
    # st.write("") # Spacer
    analyze_btn = st.button("查询装备", use_container_width=True)

# 触发逻辑：按钮点击 或 选中了英雄
if analyze_btn or selected_champ:
    if not selected_champ:
        st.warning("请先选择或输入英雄名字！")
    else:
        # 直接使用选中的英雄名，无需再 NLP 提取
        question = selected_champ
        
        with st.spinner(f'正在分析 {question} 的出装数据...'):
            # Simulate scraping delay
            time.sleep(0.5) 
            result = analyzer.analyze(question)

        if result['status'] == 'success':
            # 结果区域也应用 Glassmorphism
            # st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            
            st.markdown(f"## {result['champion']} - {result['details'].get('title', '')}")
            
            # Show builds
            builds = result['details'].get('builds')
            if builds:
                st.markdown("### 🛠️ 推荐出装组合")
                
                for idx, build in enumerate(builds):
                    # 构建图片 HTML
                    imgs_html = ""
                    names = []
                    for item in build['items']:
                        if item['icon']:
                            imgs_html += f'<img src="{item["icon"]}" class="item-img" title="{item["name"]}">'
                        else:
                            imgs_html += f'<div class="item-img" style="display:flex;align-items:center;justify-content:center;font-size:10px;">{item["name"][:2]}</div>'
                        names.append(item['name'])
                    
                    # 统计数据
                    place = build.get('place', '-')
                    top4 = build.get('top4', '-')
                    
                    st.markdown(f"""
                    <div class="item-container">
                        <div style="display:flex; gap:10px;">
                            {imgs_html}
                        </div>
                        <div style="margin-left: 10px; flex-grow: 1;">
                            <div class="item-names">{", ".join(names)}</div>
                        </div>
                        <div class="stats-info">
                            <div>平均排名: <span class="stat-value">{place}</span></div>
                            <div>前四率: <span class="stat-value">{top4}%</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.caption("数据来源: Tactics.tools & CommunityDragon")
            else:
                st.info("暂无详细出装数据")
                
            # st.markdown('</div>', unsafe_allow_html=True) # End result glass-container

        else:
            st.error(result['message'])
            st.markdown("---")
            st.markdown("💡 **提示**: 尝试输入完整的英雄名字，例如 '蔚' 而不是 '皮城执法官'。")

# Footer (Inside glass container)
st.markdown("---")
st.caption("数据来源: 腾讯游戏 / Riot Games (非官方接口演示版)")

# 统一的大玻璃容器结束
# st.markdown('</div>', unsafe_allow_html=True)
