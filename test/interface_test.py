from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

llm=ChatOpenAI( model_name="gemma3n:e4b",
            base_url="http://localhost:11434/v1",  # Ollama API 地址
            api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
            temperature=0)

def get_by_filename(filename):
    info = TextLoader(f'D:/python/AITest/data/{filename}', encoding='utf-8')
    return info.load()


def get_case_data(_):
    template = """
        你是一个自动化测试工程师，你非常熟悉requests库
        {context}
        Question: {input}
        请根据传入的接口信息提取request中的 ip 、 url 、method、json。
        key值为前面提到的字段，如果没有则无需添加。如果有则提取对应的value。
        要求返回的格式为json格式
        """
    prompt = PromptTemplate.from_template(template=template)

    data_chain = (
            RunnablePassthrough.assign(context=lambda x: get_by_filename("ip.har"), )
            | prompt
            | llm
            | JsonOutputParser()
    )
    return data_chain

def     get_case():
    """
    通过大模型生成测试数据。
    :return:
    """
    template = """
        你是一个自动化测试工程师，精通的技术栈为 Python pytest requests库
        以下是这个接口的具体信息，你的

        {context}

        请求的参数信息将输入一个字典，输入的内容为
        {req}

        Question: {input}"""
    # 模板提示，输出 json 格式的回答
    prompt = PromptTemplate.from_template(
        template=template, )
    chain = (
            RunnablePassthrough.
            assign(context=lambda x: get_by_filename("ip.har"),
                   req=get_case_data)
            | prompt
            | llm
            | StrOutputParser()
    )

    input_template = """
    根据每条测试用例的测试步骤，生成对应的测试数据信息，
    每条测试用例要求都有一条对应的单独的pytest函数
    """
    print(chain.invoke({"input": input_template}))


if __name__ == '__main__':
    print("===")
    get_case()