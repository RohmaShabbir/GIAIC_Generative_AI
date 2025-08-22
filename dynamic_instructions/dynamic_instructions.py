from agents import Agent, RunContextWrapper

def dynamic_intructions(context: RunContextWrapper, agent: Agent) -> str:
    return f"You are {agent.name}. Adapt to the user's needs"

agent = Agent(
    name="Smart Assistant",
    instructions=dynamic_intructions,   # Change based on context
)
