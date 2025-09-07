from google.adk.agents import SequentialAgent
from green_next_shopping_agent.sub_agents.photo_analyst import photo_analyst_agent
from green_next_shopping_agent.sub_agents.mcp_output import mcp_output_agent
from green_next_shopping_agent.sub_agents.mcp_output_elaboration import mcp_output_elaboration_agent


sequencial_delegation_agent = SequentialAgent(
    name="sequencial_delegation_agent",
    sub_agents=[photo_analyst_agent,mcp_output_agent]
)