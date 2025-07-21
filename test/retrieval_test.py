from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import List, Optional

from langchain_community.embeddings import OpenAIEmbeddings


class OllamaCompatibleEmbeddings(OpenAIEmbeddings):

    def _tokenize(self, texts: List[str], chunk_size: int) -> tuple:
        """
        禁用 Tokenization，直接返回原始文本和索引
        """
        indices = list(range(len(texts)))
        return (range(0, len(texts), chunk_size), texts, indices)

    def _get_len_safe_embeddings(
            self, texts: List[str], *, engine: str, chunk_size: Optional[int] = None
    ) -> List[List[float]]:
        """
        直接传递原始文本，跳过 Token 化步骤
        """
        _chunk_size = chunk_size or self.chunk_size
        batched_embeddings: List[List[float]] = []

        # 直接遍历原始文本分块
        for i in range(0, len(texts), _chunk_size):
            chunk = texts[i: i + _chunk_size]

            # 关键修改：input 直接使用文本列表
            response = self.client.create(
                input=chunk,  # 直接使用原始文本列表
                model=self.model,  # 显式传递模型参数
                **{k: v for k, v in self._invocation_params.items() if k != "model"}
            )

            if not isinstance(response, dict):
                response = response.model_dump()
            batched_embeddings.extend(r["embedding"] for r in response["data"])

        # 跳过空文本处理（Ollama 不需要）
        return batched_embeddings

    async def _aget_len_safe_embeddings(
            self, texts: List[str], *, engine: str, chunk_size: Optional[int] = None
    ) -> List[List[float]]:
        """
        异步版本处理逻辑
        """
        _chunk_size = chunk_size or self.chunk_size
        batched_embeddings: List[List[float]] = []

        for i in range(0, len(texts), _chunk_size):
            chunk = texts[i: i + _chunk_size]

            response = await self.async_client.create(
                input=chunk,
                model=self.model,
                **{k: v for k, v in self._invocation_params.items() if k != "model"}
            )

            if not isinstance(response, dict):
                response = response.model_dump()
            batched_embeddings.extend(r["embedding"] for r in response["data"])  # 注意: 实际应为 "embedding"

        return batched_embeddings
# 从指定的 URL 加载网页内容,用于将网页数据导入为 LangChain 可处理的数据格式
loader = WebBaseLoader("https://python.langchain.com/docs/tutorials/rag/")
#docs 是一个包含网页内容的 Document 对象列表。
docs = loader.load()

#数据切分,将长文本递归分割为较小的块，以避免超出模型的最大输入长度限制。
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
embeddings  = OllamaCompatibleEmbeddings(
    model="modelscope.cn/Embedding-GGUF/gte-Qwen2-7B-instruct-GGUF:latest",
    openai_api_base="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama" , # Ollama 默认无需真实 API Key，填任意值即可
    # chunk_size=512
)
#将文档转换为向量表示，并构建一个 FAISS 向量数据库,documents: 经过切分后的文档对象列表,embeddings: 嵌入模型，用于将文本转换为向量。
vector = FAISS.from_documents(documents, embeddings)
# 查询检索
# 创建 prompt
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
<context>
{context}
</context>
Question: {input}""")
llm = ChatOpenAI(
    model_name="qwen2.5:latest",
    base_url="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama"  # Ollama 默认无需真实 API Key，填任意值即可
)
# 创建 document 的chain，  获取文档，并将其格式化到提示词中
document_chain = create_stuff_documents_chain(llm, prompt)
from langchain.chains import create_retrieval_chain
# # 创建搜索chain 将 FAISS 向量数据库封装成一个检索器（Retriever）对象
retriever = vector.as_retriever()
#创建一个链，将检索器（Retriever）和文档链（Document Chain）组合成一个完整的 RAG 链。
retrieval_chain = create_retrieval_chain(retriever, document_chain)
# # 执行请求
response = retrieval_chain.invoke({"input": "what is Chat models and prompts?"})
print(response["answer"])


