# %%
from abc import ABC, abstractmethod


def block_concat(BlockList):
    return "\n".join([block.to_str() for block in BlockList])

def make_quoted_block(prompt, blockName=None):
    if blockName is None:
        blockStr = f"```\n{prompt}\n```\n\n"
    else:
        blockStr = f"```{blockName}\n{prompt}\n```\n\n"
    return blockStr


class PromptBlock(ABC):
    @abstractmethod
    def to_str(self):
        pass
    
    def print(self):
        print(self.to_str()) 
    
class System(PromptBlock):
    def __init__(self, prompt):
        self.blockName = "system_prompt"
        self.prompt = prompt
        
    def to_str(self):
        return make_quoted_block(self.prompt, self.blockName)

class Instruction(PromptBlock):
    def __init__(self, prompt):
        self.blockName = "instruction"
        self.prompt = prompt
        
    def to_str(self):
        return make_quoted_block(self.prompt, self.blockName)


class Message(PromptBlock):
    def __init__(self, speaker, message):
        self.speaker = speaker
        self.message = message

    def to_str(self):
        return f"{self.speaker}: {self.message}"


class Tool(PromptBlock):
    def __init__(self, tool_name, tool_args, outcome):
        self.tool_name = tool_name
        self.tool_args = tool_args
        self.outcome = outcome

    def to_str(self):
        tool_usage_data = {
            "ToolUsage": {
                "ToolName": self.tool_name,
                "Arguments": self.tool_args,
                "Outcome": self.outcome,
            }
        }
        return str(tool_usage_data)
