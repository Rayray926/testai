import os

from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI

os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "123qazxsw"
def connect_neo4j():
    graph = Neo4jGraph(refresh_schema=False)
    print(graph.schema)
    # query 中输入 cypher 语句，就可以完成对 neo4j 数据库的操作，执行成功后会创建出如下节点和关系
    # 可以用match (n) return n 查看所有节点
    graph.query(
        """
        MERGE (b:Book {name:"红楼梦", author:"曹雪芹"})
        WITH b
        UNWIND ["贾宝玉", "林黛玉", "薛宝钗", "王熙凤"] AS character
        MERGE (c:Character {name:character})
        MERGE (c)-[:FEATURED_IN]->(b)

    """
    )

def chain_with_graph():
    graph = Neo4jGraph(refresh_schema=False)
    chain = GraphCypherQAChain.from_llm(
        ChatOpenAI(
            model_name="llama3.1:8b",
            base_url="http://localhost:11434/v1",  # Ollama API 地址
            api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
            temperature=0),
        graph=graph,
        verbose=True,
        top_k=2,
        allow_dangerous_requests=True #用于防止 GraphCypherQAChain 自动生成并执行潜在危险的 Cypher 查询（如删除、修改数据等）
    )
    res = chain.invoke({"query": "红楼梦中的角色都有谁"})
    print(res)

if __name__ == '__main__':
    chain_with_graph()
