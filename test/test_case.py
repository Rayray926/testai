from plantuml import PlantUML
from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.tools import create_retriever_tool, tool
from langchain_openai import ChatOpenAI

from retrieval_test import OllamaCompatibleEmbeddings

llm=ChatOpenAI( model_name="llama3.1:8b",
            base_url="http://localhost:11434/v1",  # Ollama API 地址
            api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
            temperature=0)

#使用 TextLoader 读取 Markdown 文件，Windows 系统下 Python 默认使用 gbk 编码读取文件
loader = TextLoader("D:/python/AITest/data/测试用例.md",encoding="utf-8")
data = loader.load()
#这个模型用于将文档和查询语句编码为向量，便于 FAISS 做语义相似度匹配
embeddings  = OllamaCompatibleEmbeddings(
    model="modelscope.cn/Embedding-GGUF/gte-Qwen2-7B-instruct-GGUF:latest",
    openai_api_base="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama" , # Ollama 默认无需真实 API Key，填任意值即可
    # chunk_size=512
)
# 4. 向量存储，将文档通过 embeddings 向量化后存入 FAISS
vector = FAISS.from_documents(data, embeddings)
#创建 retriever，可用于根据输入问题在文档中查找最相关的内容
retriever = vector.as_retriever()
#create_retriever_tool将 retriever 封装为一个可被 LangChain Agent 调用的工具
retriever_tool = create_retriever_tool(
    retriever,
    "search_demand",
    "找到需求文档中具体说明需求的地方",
)
#定义生成 UML 图像的工具，tool 需要写注释
@tool
def generate_png(uml_code, filename):
    """根据提供的 PlantUML 代码生成 PNG 图像文件。
       参数:
           uml_code (str): PlantUML 格式的文本内容
           filename (str): 输出的图片文件名（不带扩展名）
       """
    print("================="+filename)

    plantuml = PlantUML(url='https://plantuml.ceshiren.com/img/')
    image_bytes = plantuml.processes(uml_code)
    print("2================="+filename)
    with open(f'{filename}.png', 'wb') as f:
        f.write(image_bytes)
# 将两个工具注册给 LLM，LLM 可以根据用户输入决定是否调用这些工具
tools = [retriever_tool, generate_png]
llm_with_tools = llm.bind_tools(tools)
#从 LangChain Hub 拉取标准的 Prompt 模板
prompt = hub.pull("hwchase17/openai-tools-agent")
#使用 create_openai_tools_agent 构建 Agent
agent = create_openai_tools_agent(llm, tools, prompt )
#使用 AgentExecutor 执行 Agent；
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = agent_executor.invoke({
    "input": """我是一个测试工程师，我需要从以上的需求文档中梳理出来需求信息，请帮我将所有的需求梳理出来，"
             "思维导图的第一级是需求文档中的1.x开头的标题信息，表示功能模块，第二级是该功能模块的测试点，"
             "请先输出一个 plantuml 格式的源码，源码格式如代码内所示
            @startmindmap
            * root node
                * some first level node
                    * second level node
                    * another second level node
                * another first level node
            @endmindmap
             然后再根据plantuml 生成的格式的源码信息输出一个plantuml格式的思维导图文件。生成一个图片文件，文件名为图片路径加任意随机数"""
})
