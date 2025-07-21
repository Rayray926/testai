from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool, ToolException, StructuredTool
from pydantic import BaseModel, Field


# api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
# tool = WikipediaQueryRun(api_wrapper=api_wrapper)
# tool.run({"query": "langchain"})
# print(tool.run({"query": "langchain"}))

# @tool
# def search(query: str) -> str:
#     """Look up things online."""
#     return "LangChain"
#
# print(search.name)
# print(search.description)
# print(search.args)

# class SearchInput(BaseModel):
#     # 定义参数的描述
#     # 参数名 = Field(description="参数的描述")
#     query: str = Field(description="should be a search query")
#
#
# @tool("search-tool", args_schema=SearchInput, return_direct=False)
# def search(query: str) -> str:
#     """Look up things online."""
#     return "LangChain"
#
# print(search.name)
# print(search.description)
# print(search.args)
# print(search.return_direct)

def search_tool1(s: str):
    raise ToolException("The search tool1 is not available.")

# # 效果等同于给 search_tool1 加装饰器
# search = StructuredTool.from_function(
#     func=search_tool1,
#     name="Search_tool1",
#     description="A bad tool",
# )

search = StructuredTool.from_function(
    func=search_tool1,
    name="Search_tool1",
    description="A bad tool",
    # 捕获异常错误
    handle_tool_error=True,
)

search.run("test")

print(search.run("test"))