# %%
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


# %%
from langchain_core.messages.system import SystemMessage
system_message = SystemMessage(content="I am a chicken. I can't talk")




# %%
from langchain.agents import AgentExecutor, create_structured_chat_agent

from langchain import hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# %%
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
tools = []
# agent = create_structured_chat_agent(llm, tools, prompt)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you am a chicken. You can't talk",
        ),
        ("user", "{input}"),
    ]
)
agent = prompt | llm
agent.invoke({"input": "hello"})


# %%
# system message
from langchain_core.messages.system import SystemMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage

from langchain.agents import AgentExecutor, create_structured_chat_agent

from langchain_core.prompts.chat import ChatMessagePromptTemplate
from langchain_core.prompts.chat import BaseMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


system_message = SystemMessage(content="I am a chicken. I can't talk")
chat_history = []
chat_history.append(HumanMessage(content="hello"))

# prompt = ChatPromptTemplate.from_messages([system_message, HumanMessage(content="hello")])
prompt = ChatPromptTemplate.from_messages([system_message, HumanMessage(content="can you speak")])
# prompt = BaseMessagePromptTemplate.format_messages(system_message, chat_history)
agent = prompt | llm
agent.invoke({"input": "hello"})

# AgentExecutor(agent=agent, tools=[], verbose=True).invoke({"input": "hello"})

# %%