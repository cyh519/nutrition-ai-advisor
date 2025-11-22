import streamlit as st
import os

# --- 页面设置 ---
st.set_page_config(
    page_title="营养配餐智能助手",
    page_icon="🍎",
    layout="wide"
)

# --- 核心功能函数 ---

# 1. 加载知识库
def load_knowledge_base(filepath):
    """从txt文件中加载知识"""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return "暂无知识。"

# 2. 保存新的知识到知识库
# 3. 生成AI回答

# 3. 生成AI回答 (已修改为使用 Replicate API)
def generate_ai_response(user_question, knowledge_base):
    """调用 Replicate 的 Llama 3 API 生成回答"""
    # 这里是给AI的“指令”，告诉它如何工作
    prompt = f"""你是一位专业的营养配餐师。请根据下面提供的知识库内容，为用户提供专业、清晰、易于理解的中文回答。

    如果知识库中没有相关信息，请诚实地告诉用户：“抱歉，我暂时没有这方面的知识。”
    禁止编造信息。回答时尽量分点，使用用户容易理解的语言。

    知识库内容：
    {knowledge_base}

    用户的问题是：{user_question}
    """
    
    # 关键：设置你的 Replicate API 密钥
    # 建议使用环境变量，这里为了简化，直接替换为你的密钥
    replicate.api_key = "r8_X7J09ew3NjONmsIG5HuRqiaNrQymGvd3xPkJi" # <--- 把这里替换成你自己的API密钥
    
    try:
        # 调用 Replicate 上的 Llama 3 模型
        output = replicate.run(
            "meta/llama-3-8b-instruct:0e681bc6a195d5b871b873d03c6207f86dd66a7b02043b9ba6d98502c524103a",
            input={"prompt": prompt, "max_tokens": 1000, "temperature": 0.1}
        )
        # Replicate 的输出是一个生成器，我们需要将其连接成一个完整的字符串
        return "".join(output)
    except Exception as e:
        return f"调用AI模型失败，请检查API密钥或网络连接。错误信息: {e}"
# --- 网页界面设计 ---

# 主标题
st.title("🍎 营养配餐智能助手")

# 创建一个侧边栏
with st.sidebar:
    st.header("📚 知识管理")
    
    # 显示当前知识库内容
    st.subheader("当前知识库")
    knowledge_text = load_knowledge_base("knowledge.txt")
    st.text_area("查看或编辑知识", knowledge_text, height=300)

    # 提供一个输入框，让用户添加新知识
    st.subheader("添加新知识")
    new_knowledge_input = st.text_area("请按照'[分类] - 内容'的格式输入新的知识")
    
    # 添加一个保存按钮
    if st.button("保存新知识"):
        if new_knowledge_input.strip():
            save_to_knowledge_base("knowledge.txt", new_knowledge_input)
            st.success("知识保存成功！")
            # 刷新页面以显示最新内容
            st.rerun()

# 主内容区 - 问答交互
st.header("💬 智能问答")
user_question = st.text_input("请输入您的问题，例如：糖尿病患者今天午餐吃什么？")

# 添加一个提交按钮
if st.button("获取AI回答"):
    if user_question.strip():
        # 显示一个加载动画
        with st.spinner("AI正在努力思考中..."):
            # 调用核心函数生成回答
            ai_answer = generate_ai_response(user_question, knowledge_text)
        
        # 显示回答结果
        st.subheader("AI回答：")
        st.write(ai_answer)
    else:
        st.warning("请输入您的问题后再提问。")