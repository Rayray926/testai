from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# 提示词模板
prompt = ChatPromptTemplate.from_template("出给一个关于 {goods} 的广告宣传语")
# ChatGPT模型调用对象

model =  OllamaLLM(model="qwen2.5:latest", base_url="http://127.0.0.1:11434")
functions = [
    {
        "name": "advertisement",
        "description": "一段广告词",
        "parameters": {
            "type": "object",
            "properties": {
                "goods": {"type": "string", "description": "要进行广告的产品"},
                "ad": {"type": "string", "description": "广告词"},
            },
            "required": ["goods", "ad"],
        },
    }
]
chain = prompt | model
res = chain.invoke({"goods": "冰淇淋"})
print(res)
print(type(res))

