# %%
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

from langchain_community.vectorstores import Chroma
vectorstore = Chroma("langchain_store", embeddings)
retriever = vectorstore.as_retriever()

from langchain_experimental.tools import PythonREPLTool
tools = [PythonREPLTool()]

from langchain_experimental.autonomous_agents.autogpt.agent import AutoGPT

ai_name = "test"
ai_role = "You are an autonomous agent that can answer questions about langsmith."
memory = retriever
tools = tools

# agent = AutoGPT.from_llm_and_tools(ai_name: str, ai_role: str, memory: VectorStoreRetriever, tools: List[BaseTool], llm: BaseChatModel,)  
agent = AutoGPT.from_llm_and_tools(ai_name, ai_role, memory, tools, llm)
agent.run(["Talk to me about the weather"])




from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent










prompt = hub.pull("hwchase17/structured-chat-agent")

url = "https://www.timeshighereducation.com/unijobs/listings/europe/"


from langchain_experimental.tools import PythonREPLTool
tools = [PythonREPLTool()]


agent = create_structured_chat_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# %%
# agent_executor.invoke({"input": "27*37=?"})
agent_executor.invoke({"input": "run python print('hello')"})

# %%
from langchain import hub
# prompt = hub.pull("hwchase17/react-chat-json")
prompt = hub.pull("hwchase17/structured-chat-agent")


prompt


# %%
# from langchain.chat.message import 