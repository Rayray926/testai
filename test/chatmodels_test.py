# ChatGPT模型调用对象
from langchain.globals import set_debug
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser, PydanticOutputParser
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

model  = ChatOpenAI(
    model_name="qwen2.5:latest",
    base_url="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama"  # Ollama 默认无需真实 API Key，填任意值即可
)
# # 消息列表
# messages = [
#     {"role": "system", "content": "你是一个制定方案的助手"},
#     {"role": "user", "content": "请给出我一个旅行方案，在北京的一日游"},
# ]
# message_1 = [
#     {"role": "system", "content": "你是一个制定方案的助手"},
#     {"role": "user", "content": "请给出我一个旅行方案，在北京的一日游"},
# ]
# message_2 = [
#     {"role": "system", "content": "你是一个制定方案的助手"},
#     {"role": "user", "content": "请给出我一个考雅思方案，备考时间三个月"},
# ]
# # invoke 调用
# res = model.invoke(messages)
# print(res)
#
# # batch 调用
# res_list = model.batch([message_1, message_2])
# print("=======")
# print(res_list)

# message=ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(content="你是一个翻译各种语言的助手"),
#         HumanMessagePromptTemplate.from_template("把 {poetry} 的原文诗翻译为英文")
#     ]
# )
# chain=message | model |StrOutputParser()
# res = chain.invoke({"poetry": "静夜思"})
# print(res)
set_debug(True)
# Json输出解析器
# parser = JsonOutputParser()
# print("========="+parser.get_format_instructions())
#
# # 模板提示，输出 json 格式的回答
# prompt = PromptTemplate(
#     template="根据用户的输入，给出一段中文宣传语 \n{format_instructions}\n{ads}\n",
#     input_variables=["ads"],
#     partial_variables={"format_instructions": parser.get_format_instructions()},
# )
# # 调用链 包含json输出解析器
# chain_with_parser = prompt | model | parser
# res_with_parser = chain_with_parser.invoke({"ads": "音乐节"})
# print(res_with_parser)
# print(type(res_with_parser))

# class Translation(BaseModel):
#     origin_str: str = Field(description="原始输入的值")
#     trans_str: str = Field(description="翻译后的值")
#
# parser = PydanticOutputParser(pydantic_object=Translation)
# prompt = PromptTemplate(
#     template="翻译用户输入的内容为英文\n{format_instructions}\n{query}\n",
#     input_variables=["query"],
#     partial_variables={"format_instructions": parser.get_format_instructions()},
# )
# chain_with_parser = prompt | model | parser
# res_parser = chain_with_parser.invoke({"query": "赏花"})
# print(res_parser)
# print(type(res_parser))

# response_schemas = [
#     ResponseSchema(name="slogan", description="宣传语内容"),
#     ResponseSchema(name="req", description="宣传语限制在10个字符内"),
# ]
# output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
# prompt = PromptTemplate(
#     template="根据用户输入的商品给出宣传语\n{format_instructions}\n{goods}",
#     input_variables=["goods"],
#     partial_variables={"format_instructions": output_parser.get_format_instructions()},
# )
# chain_with_parser = prompt | model | output_parser
# res_with_parser = chain_with_parser.invoke({"goods": "音乐节"})
# print(res_with_parser)
# print(type(res_with_parser))

prompt = ChatPromptTemplate.from_template("出给一个关于 {goods} 的广告宣传语")
functions = [
    {
        "name": "advertisement",
        "description": "一段广告词",
        "parameters": {
            "type": "object",
            "properties": {
                "goods": {"type": "string", "description": "要进行广告的产品"},
                "ads": {"type": "string", "description": "广告词"},
            },
            "required": ["goods", "ads"],
        },
    }
]

chain_json_with_parser = prompt | model.bind(function_call={"name": "advertisement"},
                                             functions=functions) | JsonOutputFunctionsParser()
res_json_with_parser = chain_json_with_parser.invoke({"goods": "冰淇淋"})
print(res_json_with_parser)
print(type(res_json_with_parser))