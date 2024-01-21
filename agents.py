# %%

import google.generativeai as genai
from google.generativeai.types import safety_types

from langchain_core.messages.system import SystemMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.chat import ChatMessage


def str2message(s):
    role, content = s.split(": ", 1)
    return ChatMessage(role=role, content=content)


class LLM:
    @classmethod
    def create_gemini(cls):
        from langchain_google_genai import GoogleGenerativeAI

        llm = GoogleGenerativeAI(model="gemini-pro")
        llm = cls._gemini_safety_settings(llm)
        return llm

    @classmethod
    def create_gemini_chat(cls):
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model="gemini-pro", convert_system_message_to_human=True
        )
        llm = cls._gemini_safety_settings(llm)
        return llm

    @staticmethod
    def _gemini_safety_settings(gemini_llm, setting=None):
        if setting is None:
            setting = {
                safety_types.HarmCategory.HARM_CATEGORY_HARASSMENT: safety_types.HarmBlockThreshold.BLOCK_NONE,
                safety_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: safety_types.HarmBlockThreshold.BLOCK_NONE,
                safety_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: safety_types.HarmBlockThreshold.BLOCK_NONE,
                safety_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: safety_types.HarmBlockThreshold.BLOCK_NONE,
            }
        gemini_llm.client._safety_settings = setting
        return gemini_llm


# %%
class Agent:
    def __init__(self, llm=None):
        if llm is None:
            llm = LLM.create_gemini()
        self.llm = llm

    def step(self, message):
        return self.llm.invoke(message)


# %%
class ChatAgent:
    def __init__(self, llm=None, role=None):
        if llm is None:
            llm = LLM.create_gemini()
        self.llm = llm

        if role is None:
            role = 'AI'    
        self.role = "AI" 

        self.chat_history = []
        self.chat_history.append(ChatMessage(role=self.role, content=f"I am {self.role}"))

    def step(self, message):
        # receive message
        message = ChatMessage(role="user", content=message)
        self.chat_history.append(message)

        # send message
        # message = ChatMessage(role=self.role, content="")
        # self.chat_history.append(message)
        response = self.llm.invoke(self.chat_history + [f'{self.role}: '])
        self.chat_history.append(ChatMessage(role=self.role, content=response))
        return response

# %%
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent

class ToolUsingAgent:
    def __init__(self, llm=None, role=None):
        if llm is None:
            llm = LLM.create_gemini()
        self.llm = llm
        
        if role is None:
            role = 'AI'    
        self.role = "AI" 
        
        self.system_prompt = hub.pull("hwchase17/structured-chat-agent")

    def step(self, message, tools):
        agent = create_structured_chat_agent(llm, tools, self.system_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        response = agent_executor.invoke({"input": "Tell me all members using tools"})
        return response

from langchain.tools import BaseTool, StructuredTool, tool
from typing import List

@tool
def list_members() -> List[str]:
    """List all members"""
    members = ["A", "B", "C"]
    return members
tools = [list_members]
llm = LLM.create_gemini()
agent = ToolUsingAgent(llm=llm)
agent.step("Tell me the history of PTT", tools)
