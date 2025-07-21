from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationTokenBufferMemory, ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

model  = ChatOpenAI(
    model_name="qwen2.5:latest",
    base_url="http://localhost:11434/v1",  # Ollama API 地址
    api_key="ollama"  ,# Ollama 默认无需真实 API Key，填任意值即可
    temperature=0.0
)
#创建带有对话记录功能的实例
# memory = ConversationBufferMemory()
# 生成对话链实例，用于后续对话使用
# 通过verbose=True参数可以看到LangChain具体的实现的方式
# conversation = ConversationChain(llm=model, memory=memory)
# 几轮对话之后，再询问第一个问题中给出的信息，还是可以正常获取到
#通过 conversation 实例调用predict方法，将对话链中的信息存放在该实例中。同时可以通过 memory.buffer 获取所有的对话记录信息
# res = conversation.predict(input="你好，我叫天马")
# print(res)
# res = conversation.predict(input="1+1等于几？")
# print(res)
# res = conversation.predict(input="今天是周二，昨天是周几？")
# print(res)
# res = conversation.predict(input="我的名字是什么？")
# print(res)
# # 输出已经保存的对话记录
# print(memory.buffer)
# print('无预制信息对话开始:')
# # 无预制信息时，相关对话结果是模型直接生成的数据
# res = conversation.predict(input="你叫什么")
# print(res)
# res = conversation.predict(input="你从哪来？")
# print(res)
# print('无预制信息对话结束')
# # 清空之前的对话数据，避免数据互相干扰
# memory.clear()
#
# print('有预制信息对话开始:')
# memory.save_context(inputs={'input': "你现在模拟的是精通的测试开发工程师，名字是: test"},
#                     outputs={'output': '好的'})
# # 几轮对话之后，再询问第一个问题中给出的信息，还是可以正常获取到
# # 通过verbose=True参数可以看到具体的实现过程
# res = conversation.predict(input="你叫什么")
# print(res)
# res = conversation.predict(input="你是哪个组织的？")
# print(res)
memory = ConversationSummaryBufferMemory(llm=model)
memory.save_context(inputs={'input': "你好，我叫天马"}, outputs={'output': '好的'})
memory.save_context(inputs={'input': "今天天气很不错"}, outputs={'output': '是的，今天晴空万里，适合出游'})
schedule = "今天的行程安排如下：早上6点起床，洗漱完毕。7点开始做饭，8点吃完饭准备出门，骑自行车大约1小时，9点到达公司，上午进行大模型教程的编写，大约3小时。中午12点吃饭后午休"
memory.save_context(inputs={'input': "今天的日程安排是什么？"}, outputs={'output': schedule})
print("输出已经保存的对话数据")
# 输出已经保存的对话记录,会发现保存的对话数据为空，因为之前的对话由于长度过长，已经通过LLM将对话信息进行了总结，并保存到了System中
print(memory.buffer)
# 通过读取memory里面保存的全部数据，可以发现history中存在System数据，保存了已经被总结过的对话信息
print(memory.load_memory_variables({}))
conversation = ConversationChain(llm=model, memory=memory)
print(f"对话开始:")
res = conversation.predict(input="我的名字是什么？")
print(res)
# 之前的上下文数据通过system+简述的方式传递给大模型，保证了关键信息不丢失
res = conversation.predict(input="我几点吃的早饭？")
print(res)
# 进行两轮对话之后，由于本次对话数据较短，没有触发token的限制，所以对话数据还是以原本的方式保存在history中
print(memory.buffer)
print(memory.load_memory_variables({}))
