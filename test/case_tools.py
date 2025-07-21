from langchain_core.tools import tool
from pydantic import BaseModel, Field

class PythonFileInput(BaseModel):
    # 定义参数的描述
    filename: str = Field(description="filename")
    source_code: str = Field(description="source code data")

class PytestFileName(BaseModel):
    # 定义参数的描述
    filename: str = Field(description="The name of the file to be executed")

@tool(args_schema=PythonFileInput)
def write_file(filename, source_code):
    """
    Generate python files based on input source code
    """
    with open(filename, "w") as f:
        f.write(source_code)


@tool(args_schema=PytestFileName)
def execute_test_file(filename):
    """
    Pass in the file name, execute the test case and return the execution result
    """
    import subprocess
    # 使用subprocess模块执行pytest命令
    result = subprocess.run(['pytest', filename], capture_output=True, text=True)
    # 检查pytest的执行结果
    if result.returncode == 0:
        print("测试运行成功！")
    else:
        print("测试运行失败：")
    print(result.stdout)
    return result.stdout

tools=[write_file,execute_test_file]

if __name__ == '__main__':
    execute_test_file("test_demo.py");