from langchain.globals import set_debug
from langchain_core.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI

set_debug(True)
# 初始化客户端，指向 Ollama 的本地服务
client = ChatOpenAI(
    model_name="llama3:8b",
    base_url="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama"  # Ollama 默认无需真实 API Key，填任意值即可
)

# 提示词模板
prompt = ChatPromptTemplate.from_template("出给一个关于 {goods} 的广告宣传语")
# ChatGPT模型调用对象
model = client
# 将两个对象使用顺序组合创建一个调用链，实现提示词组装，模型调用的功能
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

#chain = prompt | model.bind(function_call={"name": "advertisement"}, functions=functions)| JsonKeyOutputFunctionsParser(key_name="ad")
# 输入提示词模版中的变量部分，调用链会自动完成后续的调用和解析
map_ = RunnableParallel(goods=RunnablePassthrough())
chain = (
        map_
        | prompt
        | model.bind(function_call={"name": "advertisement"}, functions=functions)
        | JsonKeyOutputFunctionsParser(key_name="ad")
)
res = chain.invoke({"goods": "冰淇淋"})
print(res)
