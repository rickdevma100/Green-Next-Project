from google.adk.agents.llm_agent import LlmAgent
from green_next_shopping_agent.constants import GEMINI_MODEL
from google.adk.tools import google_search

product_greeness_analyzer = LlmAgent(
    name="ProductGreenessAnalyzer",
    model=GEMINI_MODEL,
    instruction="""
    You are a product eco friendliness analyzer.
    You need to analyse the product's eco friendliness based on the following product details:
    {mcp_product_details}
    see the description of the product to analyse the product's eco friendliness with similar products available in the market.
    Use the google_search tool to find out similar products
    For example: if the product description in {mcp_product_details} is 
    "This gold-tone stainless steel watch will work with most of your outfits." 
    then you can use the google_search tool to find out similar products like 
    "gold-tone stainless steel watch" and then you can get the product's eco friendliness 
    and then derive what could be given as the product's eco friendliness in the output.
    - Rate a product or a list of products based on the following criteria in 150 words maximum:
        - Carbon Footprint
        - Water Usage
        - Energy Usage
        - Waste Management
        - Recycling
        - Packaging
        - Transportation
        - Manufacturing Process
        - Sustainable Materials
        - Social Responsibility
        - Overall Impact

    - Provide a total score out of 100 for the product.

    **Mandetory: ask the user if they want to add the product to the cart or place the order.
    take the user's response and delegate the task to the mcp_product_order_agent.
    """,
    description="Analyse and the product's eco friendliness",
    tools=[google_search],
    output_key="analysed_product_greeness"
)