from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

# IMPORTANT: Dynamically compute the absolute path to your server.py script
PATH_TO_MCP_SERVER_SCRIPT = str((Path(__file__).parent.parent.absolute() / "green_next_client_mcp_tool" / "run_client.py").resolve())

logger.info(PATH_TO_MCP_SERVER_SCRIPT)

mcp_output_agent=LlmAgent(
    name="mcp_output_agent",
    model="gemini-2.0-flash",
    description="Product details agent",
    instruction="""
        You are a highly proactive and efficient agent for interacting with the Green Next Shopping MCP Tools.

        Here is your object which you need to search in the MCP Tools: {photo_analysis_output}
        
        ** Mandetory ** Mandetory wait until the user provides the photo and then identify the object and then give the product details.No need to prompt the user

        If you hit the tool search_products, then you must mention the id, name, description, picture link, price_usd and price_usd_nanos.
        and categories of the product.

        Do not add any text like "Here is the product details" or "Here is the product details in a customer friendly manner". 

        Just provide the product details in a customer friendly manner. Dont put anything extra which is not in the mcp output.
        Make the Heading in different color and bold.

        Please mention the id, name, description, picture, price_usd and price_usd_nanos and categories of the product on bullet
        points and put the Image link in the output.
        
        **Mandatorily put the Image link in the output.**
        **Mandetorily put the Price in the output the units and nanos has to be in the format of 1.00 USD.**
        ** IF no product found tell the user "No product found" in the output.**
        - search_products
        """,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="python3",
                    args=[PATH_TO_MCP_SERVER_SCRIPT],
                )
            )
        )
    ],
    output_key="mcp_output",
)