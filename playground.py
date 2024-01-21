# %%
from prompt_blocks import System, Instruction, block_concat, PromptBlock
from agents import LLM




class Message(PromptBlock):
    def __init__(self, role, action, action_content):
        self.role = role
        self.action = action
        self.action_content = action_content

    def to_str(self):
        return f"{self.role}[{self.action}]: {self.action_content}"


system = System("You are a chat bot.")
instruction = Instruction(
    """
Welcome to our interactive session! Here, all interactions follow a specific format:

Format: $role[$action]: $action_content

Let's look at an example dialogue between an AI and a user:
AI[say]: How can I assist you today?
User[say]: Could you tell me today's weather?
AI[say]: Today is sunny and clear.

Key Points:
- Each turn involves one role performing an action.
- Currently, the available actions are: [say] and [think].

Please select your action thoughtfully for each turn.
"""
)



class Agent:
    def __init__(self, name=None, llm=None):
        if llm is None:
            self.llm = LLM.create_gemini()
        else:
            self.llm = llm

        if name is None:
            self.name = "AI"
        else:
            self.name = name

    def step(self, prompt):
        return self.llm.invoke(prompt)


class ChatAgent(Agent):
    def __init__(self, name=None, llm=None):
        super().__init__(name=name, llm=llm)

    def step(self, prompt):
        reply = self.llm.invoke(prompt + f"\n{self.name}[say]:")
        message = Message(role=self.name, action="say", action_content=reply)
        return message



# %%

prompts = [system, instruction]
agent = ChatAgent()

while True:
    s = input(">>> ")
    message = Message(role="User", action="say", action_content=s)
    message.print()
    prompts.append(message)
    
    prompt = block_concat(prompts)
    message = agent.step(prompt)
    prompts.append(message)
    message.print()

# %%
