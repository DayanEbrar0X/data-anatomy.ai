from tools import search, calculator
from model import think          # the LLM call

goal = "What is 15% of Q3 revenue?"
memory = [goal]

for step in range(5):
    action, arg = think(memory)
    if action == "answer":
        print("answer:", arg)
        break
    tool = {"search": search,
            "calc": calculator}[action]
    result = tool(arg)
    memory.append(result)
    print(step, action, "->", result)
