import pprint

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter

llm=ChatOpenAI( model_name="llama3.1:8b",
            base_url="http://localhost:11434/v1",  # Ollama API 地址
            api_key="ollama",  # Ollama 默认无需真实 API Key，填任意值即可
            temperature=0)

# 定义提取方法
def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke(content)

def scrape_with_playwright(urls, schema):
    # 加载数据
    loader = AsyncChromiumLoader(urls)
    print(loader)
    docs = loader.load()
    print(docs)

    # 数据转换
    bs_transformer = BeautifulSoupTransformer()
    # 提取其中的span标签
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["span"]
    )
    # 数据切分
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=0)
    splits = splitter.split_documents(docs_transformed)
    # 因为数据量太大，输入第一片数据使用，传入使用的架构
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint.pprint(extracted_content)
    return extracted_content

urls = ["https://ceshiren.com/"]
schema = {
    "properties": {
        "title": {"type": "string"},
        "url": {"type": "string"},
    },
    "required": ["title", "url"],
}
extracted_content = scrape_with_playwright(urls, schema=schema)
