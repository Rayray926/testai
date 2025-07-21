from operator import itemgetter

from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

db = SQLDatabase.from_uri("sqlite:///D:/python/AITest/data/Chinook.db")
# 通过LLM 获取查询语句
llm = ChatOpenAI(
    model_name="llama3.1:8b",
    base_url="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
    temperature=0)
# # 执行查询动作，将自然语言转换为一条sql语句
execute_query = QuerySQLDataBaseTool(db=db)
# # 获取sql 查询语句
write_query = create_sql_query_chain(llm, db)
# 先生成查询语句，再执行查询动作
chain = write_query | execute_query
# print(chain.get_prompts()[0].pretty_print())
response = chain.invoke({"question": "How many Employees are there?"})
#响应结果为一条sql语句
print(response)
print("=======")
# print(db.run(response))

#查询结果转换为自然语言（更好让人理解）
# 定义提示词，其中有 question、query、result 三个变量
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)
answer = answer_prompt | llm | StrOutputParser()
# query通过write_query链的执行结果获取
# result 通过使用 itemgetter("query") 从上一步的上下文中取出 SQL 查询语句。 execute_query链获取
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)
print(chain.invoke({"question": "How many employees are there"}))