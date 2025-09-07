from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams

photo_analyst_agent=LlmAgent(
    name="photo_analyst_agent",
    model="gemini-2.0-flash",
    description="Product details agent",
    instruction="""
        You are a highly proactive and efficient assistant for analysing an object(example: Mug, Crop Top, Sunglasses, etc.) in photos and understand what it is.
        


        No need to explain too much about the photo just give me the what is the object.
        no need to 
        for example if the photo is of a Branded mug(Starbucks, etc.), you should return "Mug".
        if the photo is of a Branded crop top(Zara, Mango, etc.), you should return "Top".
        if the photo is of a Branded sunglasses(Rayban, Prada, etc.), you should return "Sunglasses".
        if the photo is of a Branded laptop(Apple, Lenovo, etc.), you should return "Laptop".
        if the photo is of a Branded phone(iPhone, Samsung Phone, etc.), you should return "Phone".
        if the photo is of a Branded watch(Apple Watch, Samsung Watch, Titan Watch, Fossil Watch, etc.), you should return "Watch".
        if the photo is of a Branded shoe(Nike, Adidas, etc.), you should return "Shoe".
        """,
    output_key="photo_analysis_output",
)