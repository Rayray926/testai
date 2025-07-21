import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model_name="qwen2.5:latest",
    base_url="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama"  # Ollama 默认无需真实 API Key，填任意值即可
)

# 提示词模板对象
prompt = ChatPromptTemplate.from_template(
   "给出一个关于 {topic} 的宣传语"
)

# 将ChatGPT返回结果转换为字符串的处理器对象
output_parser = StrOutputParser()
# 将三个对象根据使用顺序组合成一个调用链，实现提示词组装、模型调用、结果解析的功能
chain = prompt | model | output_parser
# 输入提示词模版中的变量部分，调用链会自动完成后续的调用和解析
res = chain.invoke({"topic": "音乐节"})
# 打印结果
print(res)
