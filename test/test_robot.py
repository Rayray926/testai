import os

from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_text_splitters import MarkdownHeaderTextSplitter

from OllamaCompatibleEmbeddings import OllamaCompatibleEmbeddings

embeddings  = OllamaCompatibleEmbeddings(
    model="modelscope.cn/Embedding-GGUF/gte-Qwen2-7B-instruct-GGUF:latest",
    openai_api_base="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama" , # Ollama 默认无需真实 API Key，填任意值即可
    # chunk_size=512
)
# 定义一个函数，用于加载本地文件中的文本
def load_text_from_file(path):
    return open(path, encoding='utf-8').read()


#  根据测试用例文档中的结构，定义一个MarkdownHeaderTextSplitter实例，用于将markdown文档切分为文本片段，方便后续embedding处理和向量数据库的构建
testcase_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##", "模块名称"), ("###", "用例名称")])
docs = testcase_splitter.split_text(load_text_from_file(path="D:/python/AITest/data/测试用例.md"))
# 同样处理设计文档，因为设计文档中的结构与测试用例文档不一致，所以要新定义一个MarkdownHeaderTextSplitter实例
design_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##", "功能名称"), ("###", "模块名称")])
docs += design_splitter.split_text(load_text_from_file(path="D:/python/AITest/data/设计文档.md"))
 #同理，处理需求文档
prd_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("###", "功能名称")])
docs += prd_splitter.split_text(load_text_from_file(path="D:/python/AITest/data/需求文档.md"))

# 将切分后的文本片段输出，可以查看切分结果，和里面附带的数据信息
# for doc in docs:
#     print(doc)
persist_directory = 'chroma'
if os.path.isdir(persist_directory):
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

else:
    # 将切分后的数据，通过OpenAIEmbeddings实例，转换为向量数据，
    # 并保存到向量数据库中，持久化到本地指定目录下
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
# 设定最终提出的问题
question = "问题：请统计出用户注册用例中，用到的所有用户名、密码、电子邮箱数据，并将它们列成一个表格"
# 从向量数据库中找到相似度最高的k条文本片段数据
answer_docs = vectordb.similarity_search(query=question, k=4)
llm = ChatOpenAI(
    model_name="qwen2.5:latest",
    base_url="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
    temperature=0.0)
# 将向量数据库中检索到的文本片段组装成字符串，作为输入的数据源
resource_doc = "".join([chunk.page_content for chunk in answer_docs])
# 将数据源字符串和问题组装成最终请求大模型的字符串
final_llm_text = f"{resource_doc} {question}"
# 通过大模型获取字符串的回答信息
response = llm.call_as_llm(message=final_llm_text)
print(f"回答结果：\n{response}")