import openai
from langchain_openai import ChatOpenAI

llm=ChatOpenAI( model_name="qwen3:8b",
            base_url="http://localhost:11434/v1",  # Ollama API 地址
            api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
            temperature=0)

def get_message(role_prompt):
    message = []
    message.append({
                    'role': 'user',
                    'content': role_prompt
                })
    response = openai.chat.completions.create(
                model=llm,
                messages=message,
                temperature=0
            )
    # # 打印大模型的返回值
    answer = response
    return answer

def test_get_message():
    # 文档读取
    with open("data/旅游软件需求文档.md") as f:
        content = f.read()
    # 文档替换
    # role_prompt = """
    # 你是一个测试工程师，需要将需求文档转化为测试用例。要求输出的测试用例的格式为plantuml中的mindmap格式。
    # 需求文档的内容为：{context}
    # """.format(context=content)
    role_prompt="清朝持续了多少年"
    print(get_message(role_prompt))
