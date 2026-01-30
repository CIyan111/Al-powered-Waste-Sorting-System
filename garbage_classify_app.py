import streamlit as st

# -------------------------- 全局配置与自定义CSS --------------------------
st.set_page_config(
    page_title="♻️ 智能垃圾分类识别系统",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 高级自定义CSS
custom_css = """
<style>
/* 全局背景：柔和的渐变 */
.stApp {
    background: linear-gradient(135deg, #f0f9f5 0%, #e6f7ef 100%);
    background-attachment: fixed;
}

/* 主标题：自定义字体和颜色 */
.main-title {
    font-size: 32px !important;
    font-weight: 700 !important;
    color: #2f5d62 !important;
    margin-bottom: 8px !important;
    text-align: center;
}

/* 副标题：柔和的灰色 */
.sub-title {
    color: #6b7280 !important;
    text-align: center;
    margin-bottom: 32px !important;
    font-size: 16px;
}

/* 自定义卡片：悬浮效果+精致阴影 */
.custom-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 8px 30px rgba(78, 143, 118, 0.08);
    border: 1px solid #f0f8f5;
    transition: all 0.3s ease;
    margin-bottom: 24px;
}
.custom-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(78, 143, 118, 0.12);
}

/* 按钮美化：环保绿主色+圆角+悬浮动效 */
.stButton > button {
    background: linear-gradient(135deg, #4a7366 0%, #2f5d62 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    font-size: 15px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(74, 115, 102, 0.2);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(74, 115, 102, 0.3);
}
.stButton > button:disabled {
    background: #94a3b8 !important;
    transform: none;
    box-shadow: none;
}

/* 上传组件美化：虚线边框+圆角+悬浮变色 */
.stFileUploader > div > div {
    border: 2px dashed #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    transition: all 0.3s ease;
    background: #fafbfc;
}
.stFileUploader > div > div:hover {
    border-color: #4a7366;
    background: #f0f9f5;
}

/* 提示框美化：圆角+左侧色块 */
.stSuccess, .stInfo, .stWarning {
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    border-left: 4px solid #4a7366;
    padding: 12px 16px;
}

/* 侧边栏美化 */
[data-testid="stSidebar"] {
    background: #f8fafc;
    border-right: 1px solid #e2e8f0;
}
[data-testid="stSidebar"] h3 {
    color: #2f5d62;
    font-weight: 600;
}

/* 图片预览：圆角+阴影 */
.stImage img {
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

/* 底部文字：居中+灰色 */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    margin-top: 40px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------- 侧边栏：垃圾分类小知识 --------------------------
with st.sidebar:
    st.markdown("### 📚 垃圾分类小知识")
    st.divider()

    st.markdown("""
    <div style="padding: 8px; background: #f0f9f5; border-radius: 8px; margin-bottom: 12px;">
    <span style="color: #4a7366; font-weight: 600;">♻️ 可回收物</span><br>
    <span style="font-size: 13px; color: #6b7280;">纸类、塑料、玻璃、金属、织物等</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 8px; background: #fff1e6; border-radius: 8px; margin-bottom: 12px;">
    <span style="color: #e27d60; font-weight: 600;">🍚 厨余垃圾</span><br>
    <span style="font-size: 13px; color: #6b7280;">剩菜剩饭、果皮、蔬菜、肉类内脏等</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 8px; background: #ffe5e5; border-radius: 8px; margin-bottom: 12px;">
    <span style="color: #e74c3c; font-weight: 600;">⚠️ 有害垃圾</span><br>
    <span style="font-size: 13px; color: #6b7280;">电池、灯管、过期药品、油漆桶等</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 8px; background: #f1f5f9; border-radius: 8px;">
    <span style="color: #64748b; font-weight: 600;">🗑️ 其他垃圾</span><br>
    <span style="font-size: 13px; color: #6b7280;">餐巾纸、塑料袋、一次性餐具等</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="font-size: 12px; color: #94a3b8; text-align: center;">
    本系统基于AI图像识别技术<br>快速实现垃圾智能分类
    </div>
    """, unsafe_allow_html=True)

# -------------------------- 主页面 --------------------------
st.markdown('<h1 class="main-title">♻️ 智能垃圾分类识别系统</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">上传垃圾图片，AI自动识别分类类型 | 支持单张图片上传（JPG/PNG/JPEG）</p>',
            unsafe_allow_html=True)
st.divider()

# 核心功能卡片
st.markdown('<div class="custom-card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    label="请选择要识别的垃圾图片",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=False,
    help="推荐上传清晰的垃圾正面图片，识别准确率更高（如塑料瓶、果皮、电池等）",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    st.success(f"✅ 图片上传成功！文件名：{uploaded_file.name}")
    st.image(
        uploaded_file,
        caption="📷 上传的垃圾图片（预览）",
        use_column_width=False,
        width=420,
        output_format="PNG"
    )
    st.button("🚀 点击开始AI识别分类", help="点击后调用AI模型，返回分类结果")
    st.markdown("---")
    st.info("📌 识别结果将展示于此 | 包含分类类型+分类建议+处理方式")
else:
    st.info("ℹ️ 请点击上方上传框，选择一张垃圾图片（如塑料瓶、果皮、电池、废纸等）")

st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown("""
<div class="footer">
中国大学生计算机设计大赛参赛项目 | 前端基于Streamlit开发 | 后续将对接AI图像识别模型
</div>
""", unsafe_allow_html=True)