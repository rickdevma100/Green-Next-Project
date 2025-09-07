from google.adk.agents import Agent
from green_next_shopping_agent.sub_agents.sequencial_delegation_agent import sequencial_delegation_agent

root_agent = Agent(
    name="green_next_shopping_agent",
    model="gemini-2.0-flash",
    description="A manager agent that orchestrates the Image analysis and MCP output.",
    instruction="""
    You are an Agent which delegate the task to the sub agent.
    """,
    sub_agents=[sequencial_delegation_agent],

)
