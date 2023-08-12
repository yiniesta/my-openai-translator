import streamlit as st
import requests

# Streamlit App 标题
st.title("PDF 翻译工具")

# 添加一个文本框，用于输入 OpenAI Key
openai_key = st.text_input("请输入 OpenAI Key")

# 添加一个文本框，用于输入翻译语言
language = st.text_input("请输入翻译语言")

# 添加一个文件上传控件，限制只能上传 PDF 文件
uploaded_file = st.file_uploader("请选择要翻译的 PDF 文件", type="pdf")

# 当用户点击“开始翻译”按钮时触发这个回调函数
if st.button("开始翻译"):
    # 检查是否已经选择了文件
    if uploaded_file is None:
        st.warning("请先选择要翻译的 PDF 文件！")
    # 检查是否已经输入了 OpenAI Key
    elif not openai_key:
        st.warning("请先输入 OpenAI Key！")
    # 检查是否已经输入了翻译语言
    elif not language:
        st.warning("请先输入翻译语言！")
    else:
        # 创建用于发送 API 请求的 URL
        translate_url = "http://127.0.0.1:5000/translate_pdf"

        # 构造请求体，包括 OpenAI Key、翻译语言和上传的文件
        data = {
            "openai_key": openai_key,
            "language": language,
            "file": uploaded_file
        }

        # 发送 API 请求
        response = requests.post(translate_url, files=data)

        if response.status_code == 200:
            # 获取翻译结果
            translated_text = response.text

            # 在界面上显示翻译后的文本
            st.success("翻译成功！")
            st.text_area("翻译结果", translated_text)

        else:
            st.error("翻译失败，请检查参数是否正确！")
