# %%
llm = LLM.create_gemini_chat()
from langchain.agents import AgentExecutor, create_structured_chat_agent

tools = [list_members]

from langchain import hub

prompt = hub.pull("hwchase17/structured-chat-agent")

agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "Tell me all members using tools"})




# %%
from langchain.tools import BaseTool, StructuredTool, tool
from typing import List



@tool
def list_members() -> List[str]:
    """List all members"""
    members = ["A", "B", "C"]
    return members

# %%

data = {}
nested_dict = {
    'key1': {
        'nested_key1': 'value1',
        'nested_key2': 3
    },
    'key2': {
        'nested_key3': [1, 2, 3],
        'nested_key4': 'value4'
    }
}

str(nested_dict)