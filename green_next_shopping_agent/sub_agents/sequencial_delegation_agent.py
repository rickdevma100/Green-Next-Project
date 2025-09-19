from google.adk.agents import SequentialAgent
from green_next_shopping_agent.sub_agents.analyse_the_product_greeness.agent import product_greeness_analyzer
from green_next_shopping_agent.sub_agents.mcp_product_details_client_agent import mcp_product_details_agent

sequencial_delegation_agent = SequentialAgent(
    name="sequencial_delegation_agent",
    sub_agents=[mcp_product_details_agent,product_greeness_analyzer]
)