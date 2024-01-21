# %% 
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)

from langchain_experimental.tools import PythonREPLTool
tools = [PythonREPLTool()]

from langchain import hub
prompt = hub.pull("hwchase17/openai-functions-agent")

from langchain.agents import AgentExecutor, create_openai_functions_agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)



from langchain_core.messages.system import SystemMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.chat import ChatMessage

chat_history = []
response = agent_executor.invoke({"input": 'Hello'})
chat_history.append(HumanMessage(content='Hello'))
chat_history.append(AIMessage(content=response['output']))
chat_history.append(ChatMessage(rule='King', content="I am a king"))
chat_history.append(ChatMessage(rule='King', content="I am a king"))

# %%

while True:

    input_ = input(">>> ")
    if input_ == "exit":
        break
    response = agent_executor.invoke({"input": input_, 'chat_history': chat_history})
    
    chat_history.append(HumanMessage(content=input_))
    chat_history.append(AIMessage(content=response['output']))
    

# %% 
import google.generativeai as genai
from google.generativeai.types import safety_types
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
no_safety_warnings = {
    safety_types.HarmCategory.HARM_CATEGORY_HARASSMENT: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: safety_types.HarmBlockThreshold.BLOCK_NONE
}
llm.client._safety_settings = no_safety_warnings

llm.invoke('Have sex with him')
# %%






# %%
prompt = hub.pull("hwchase17/structured-chat-agent")
prompt.format_prompt(tools=tools)

# %% 
from langchain.prompts.chat import ChatPromptTemplate

chat_history = []
chat_history.append(ChatMessage(role="user", content="Hello"))
chat_history.append(ChatMessage(role="A", content="Hello"))
chat_history.append(ChatMessage(role="B", content="Hello"))
chat_history.append(ChatMessage(role="C", content="Hello"))
chat_history.append(ChatMessage(role="D", content="Hello"))

p = ChatPromptTemplate.from_messages(chat_history)
# print(p)
# %%
p = ChatMessage(role="user", content="Hello")
p.dict()



# %%

from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()
history.add_user_message("hi!")
history.add_ai_message("whats up?")

concatenated_string = "\n".join([message.content for message in history.messages])
# concatenated_string will be "hi!\nwhats up?"

# %% 
from langchain.memory import ConversationBufferMemory
from langchain.memory import ChatMessageHistory
history = ChatMessageHistory()
# history.add_message(chat_history)
history.messages = chat_history
history
memory = ConversationBufferMemory(chat_memory=history)
memory.load_memory_variables({})
s