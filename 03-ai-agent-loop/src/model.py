# Stand-in for the LLM: reads memory, returns the next action.
# In production this is one API call that returns the same (action, arg) shape.


def think(memory):
    facts = " ".join(map(str, memory))
    if "revenue:" not in facts:
        return "search", "Q3 revenue"
    if len(memory) < 3:
        revenue = memory[1].split(": ")[1]
        return "calc", f"0.15 * {revenue}"
    return "answer", f"${memory[-1]:,.0f}"
