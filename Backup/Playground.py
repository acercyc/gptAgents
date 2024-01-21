from PrimeAgent import PrimeAgent
import tools
import json


if __name__ == "__main__":
    agent = PrimeAgent()
    commandTool = tools.CommandTool()

    for iStep in range(100):
        try:
            action_json = agent.act()
            action = json.loads(action_json)
            print(agent.context)

            if action["action"] == "SPEAK":
                print(action["text"])
                outcome = ""
            elif action["action"] == "ASK USER":
                outcome = "User:" + input("\n" + action["question"] + "\n")
            elif action["action"] == "Use CommandTool":
                outcome = commandTool.use(action["command"])
            else:
                outcome = "Error: action not recognized"
        except Exception as e:
            outcome = "Error: " + str(e)
        
        agent.perceive(outcome)
