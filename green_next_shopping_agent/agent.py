from google.adk.agents import Agent
from green_next_shopping_agent.sub_agents.sequencial_delegation_agent import sequencial_delegation_agent
from green_next_shopping_agent.sub_agents.mcp_product_order_agent import mcp_product_order_agent
from green_next_shopping_agent.constants import GEMINI_MODEL
from google.adk.tools.tool_context import ToolContext
from typing import Dict

def set_user_id(
    tool_context: ToolContext,
    email_id: str,
) -> Dict:
    # Print key-value pairs
    tool_context.state["user_id"] = email_id
    return {"user_id": "User ID set in the state"}
    

root_agent = Agent(
    name="green_next_shopping_agent",
    model= GEMINI_MODEL,
    description="A Manager agent that orchestrates the Image and text analysis and MCP output.",
    instruction="""
     ## Your Role as Manager
     You are a manager agent that orchestrates the Image and text analysis and MCP output.
     
     First tell the user that you are going to help them with their shopping and find the greenest products for them.
    
     - You need to ask the user for their email address which will be used to send mail to the user.
     - Use the set_user_id tool to set the user id in the state.
     - You need to ask the user whether they want to search for a product or list the products 
     or ask for a photo of a similar product.
     - While all details are given You need to delegate the task to the sequencial_delegation_agent.

     **Mandetory: After completing the sequencial_delegation_agent. You need to ask the user whether they want to add a product to the cart or place the order.
     - If the user wants to place the order, you need to delegate the task to the mcp_product_order_agent.

     **MAndatory: Make sure first the Phase 1 is completed and then the Phase 2 is completed.
    """,
    sub_agents=[sequencial_delegation_agent,mcp_product_order_agent],
    tools=[set_user_id]

)
