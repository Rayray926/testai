# 配置连接参数
import os

from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "123qazxsw"

neo4j_graph  = Neo4jGraph(refresh_schema=False)

# 初始化链对象
graph_chain = GraphCypherQAChain.from_llm(
    graph=neo4j_graph,
    llm=ChatOpenAI( model_name="llama3.1:8b",
            base_url="http://localhost:11434/v1",  # Ollama API 地址
            api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
            temperature=0),
    return_intermediate_steps=True,
    verbose=True,
    allow_dangerous_requests=True
)

# 编写查询函数
def run_query(query):
    response = graph_chain.run(query)
    return response

# 实现交互模块
def get_user_input():
    query = input("请输入您的查询 (输入 'exit' 退出): ")
    return query

def display_results(results):
    if isinstance(results, list):
        for result in results:
            print(result)
    else:
        print(results)

# 运行智能体
def run_agent():
    while True:
        query = get_user_input()
        if query.lower() in ['exit', 'quit']:
            print("退出程序...")
            break
        results = run_query(query)
        display_results(results)

run_agent()
