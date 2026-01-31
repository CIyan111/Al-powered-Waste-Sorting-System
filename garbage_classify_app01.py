import streamlit as st
import requests
from PIL import Image
import io

# -------------------------- 全局配置与自定义CSS --------------------------
st.set_page_config(
    page_title="♻♻️ 智能垃圾分类识别系统",
    page_icon="♻♻️",
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

/* 结果展示区域美化 */
.result-card {
    background: linear-gradient(135deg, #f8fff9 0%, #f0f9f5 100%);
    border-radius: 12px;
    padding: 20px;
    border-left: 5px solid #4a7366;
    margin: 20px 0;
}
.result-title {
    color: #2f5d62;
    font-weight: 600;
    font-size: 18px;
    margin-bottom: 10px;
}
.result-content {
    color: #4a7366;
    font-size: 16px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------- 垃圾分类映射和说明 --------------------------
# 根据后端返回的类别映射到中文分类和说明
category_mapping = {
    "电池": {
        "type": "有害垃圾",
        "description": "废旧电池含有重金属和有害化学物质",
        "handling": "应投放到有害垃圾收集容器，由专业机构处理"
    },
    "生物垃圾": {
        "type": "厨余垃圾",
        "description": "易腐烂的有机废弃物",
        "handling": "应投放到厨余垃圾收集容器，可用于堆肥"
    },
    "棕色玻璃": {
        "type": "可回收物",
        "description": "棕色玻璃瓶、玻璃制品",
        "handling": "应清洁后投放到可回收物收集容器"
    },
    "纸板": {
        "type": "可回收物",
        "description": "纸板箱、包装纸板等",
        "handling": "应压扁后投放到可回收物收集容器"
    },
    "衣物": {
        "type": "可回收物",
        "description": "废旧纺织品、衣物",
        "handling": "应清洁干燥后投放到可回收物或专门回收箱"
    },
    "绿色玻璃": {
        "type": "可回收物",
        "description": "绿色玻璃瓶、玻璃制品",
        "handling": "应清洁后投放到可回收物收集容器"
    },
    "金属": {
        "type": "可回收物",
        "description": "金属罐、金属制品等",
        "handling": "应清洁后投放到可回收物收集容器"
    },
    "纸张": {
        "type": "可回收物",
        "description": "报纸、书本、办公用纸等",
        "handling": "应整齐捆扎后投放到可回收物收集容器"
    },
    "塑料": {
        "type": "可回收物",
        "description": "塑料瓶、塑料容器、塑料包装等",
        "handling": "应清洁后压扁投放到可回收物收集容器"
    },
    "鞋子": {
        "type": "可回收物",
        "description": "废旧鞋类",
        "handling": "可投放到可回收物或专门回收箱"
    },
    "一般垃圾": {
        "type": "其他垃圾",
        "description": "难以回收利用的废弃物",
        "handling": "应投放到其他垃圾收集容器"
    },
    "白色玻璃": {
        "type": "可回收物",
        "description": "透明玻璃瓶、玻璃制品",
        "handling": "应清洁后投放到可回收物收集容器"
    }
}


# -------------------------- API调用函数 --------------------------
def predict_image(image_file):
    """调用后端API进行图像分类预测"""
    try:
        # 准备文件数据
        files = {'file': (image_file.name, image_file.getvalue(), image_file.type)}

        # 发送POST请求到后端API
        response = requests.post('http://localhost:8080/predict', files=files)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API请求失败，状态码：{response.status_code}'}
    except requests.exceptions.ConnectionError:
        return {'error': '无法连接到后端服务，请确保后端服务正在运行'}
    except Exception as e:
        return {'error': f'预测过程中出现错误：{str(e)}'}


# -------------------------- 侧边栏：垃圾分类小知识 --------------------------
with st.sidebar:
    st.markdown("### 📚📚 垃圾分类小知识")
    st.divider()

    st.markdown("""
    <div style="padding: 8px; background: #f0f9f5; border-radius: 8px; margin-bottom: 12px;">
    <span style="color: #4a7366; font-weight: 600;">♻♻️ 可回收物</span><br>
    <span style="font-size: 13px; color: #6b7280;">纸类、塑料、玻璃、金属、织物等</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 8px; background: #fff1e6; border-radius: 8px; margin-bottom: 12px;">
    <span style="color: #e27d60; font-weight: 600;">🍚🍚 厨余垃圾</span><br>
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
    <span style="color: #64748b; font-weight: 600;">🗑🗑️ 其他垃圾</span><br>
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
st.markdown('<h1 class="main-title">♻♻️ 智能垃圾分类识别系统</h1>', unsafe_allow_html=True)
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

    # 显示预览图片
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            uploaded_file,
            caption="📷📷 上传的垃圾图片（预览）",
            use_container_width=True,
            output_format="PNG"
        )

    with col2:
        st.info("💡 图片识别提示")
        st.markdown("""
        - 确保图片清晰，光线充足
        - 尽量拍摄垃圾的正面特征
        - 避免背景过于复杂
        - 支持常见垃圾类型识别
        """)

    # 识别按钮
    if st.button("🚀🚀 点击开始AI识别分类", help="点击后调用AI模型，返回分类结果", use_container_width=True):
        with st.spinner('🤖 AI正在识别中，请稍候...'):
            # 调用后端API
            result = predict_image(uploaded_file)

            if 'error' in result:
                st.error(f"❌ 识别失败：{result['error']}")
            else:
                category = result['category']
                category_info = category_mapping.get(category, {})

                st.success("✅ AI识别完成！")

                # 显示识别结果
                st.markdown("---")
                st.markdown("### 📊📊 识别结果")

                # 结果卡片
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">识别类别：{category}</div>
                    <div class="result-content">
                        <strong>垃圾分类：</strong>{category_info.get('type', '未知')}<br>
                        <strong>物品描述：</strong>{category_info.get('description', '暂无描述')}<br>
                        <strong>处理方式：</strong>{category_info.get('handling', '暂无处理建议')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 根据分类类型显示不同的颜色提示
                garbage_type = category_info.get('type', '')
                if garbage_type == "可回收物":
                    st.markdown("""
                    <div style="background: #f0f9f5; padding: 15px; border-radius: 10px; border-left: 5px solid #4a7366;">
                    <span style="color: #4a7366; font-weight: 600;">♻♻️ 可回收物提示：</span>
                    <span style="color: #4a7366;">请清洁后投放至可回收物垃圾桶</span>
                    </div>
                    """, unsafe_allow_html=True)
                elif garbage_type == "厨余垃圾":
                    st.markdown("""
                    <div style="background: #fff1e6; padding: 15px; border-radius: 10px; border-left: 5px solid #e27d60;">
                    <span style="color: #e27d60; font-weight: 600;">🍚🍚 厨余垃圾提示：</span>
                    <span style="color: #e27d60;">请沥干水分后投放至厨余垃圾桶</span>
                    </div>
                    """, unsafe_allow_html=True)
                elif garbage_type == "有害垃圾":
                    st.markdown("""
                    <div style="background: #ffe5e5; padding: 15px; border-radius: 10px; border-left: 5px solid #e74c3c;">
                    <span style="color: #e74c3c; font-weight: 600;">⚠️ 有害垃圾提示：</span>
                    <span style="color: #e74c3c;">请轻放并投放至有害垃圾专用桶</span>
                    </div>
                    """, unsafe_allow_html=True)
                elif garbage_type == "其他垃圾":
                    st.markdown("""
                    <div style="background: #f1f5f9; padding: 15px; border-radius: 10px; border-left: 5px solid #64748b;">
                    <span style="color: #64748b; font-weight: 600;">🗑🗑️ 其他垃圾提示：</span>
                    <span style="color: #64748b;">请投放至其他垃圾桶</span>
                    </div>
                    """, unsafe_allow_html=True)
else:
    st.info("ℹℹ️ 请点击上方上传框，选择一张垃圾图片（如塑料瓶、果皮、电池、废纸等）")

st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown("""
<div class="footer">
中国大学生计算机设计大赛参赛项目 | 前端基于Streamlit开发 | 后端基于Flask和PyTorch
</div>
""", unsafe_allow_html=True)