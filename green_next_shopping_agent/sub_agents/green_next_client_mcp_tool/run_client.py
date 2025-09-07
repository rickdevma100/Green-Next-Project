from __future__ import annotations

import logging
from typing import Any
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

from grpc_clients import (
    ProductCatalogClient,
    CartClient,
    CheckoutClient,
)

# Create server
mcp = FastMCP("FastMCP Server for Green Next Shopping")

@mcp.tool()
def search_products(product_name: str) -> dict[str, Any]:
    client = ProductCatalogClient(target="localhost:3550")
    try:
        resp = client.search_products(product_name)
        ip_address = "http://35.196.239.161"
        return {
            "results": [
            {
                "id": p.id, 
                "name": p.name, 
                "description": p.description, 
                "picture": (f"{ip_address}{p.picture}" if ip_address else p.picture),
                "price_usd": p.price_usd.units,
                "price_usd_nanos": p.price_usd.nanos,
                "categories": list(p.categories)
            } 
            for p in resp.results]}
    finally:    
        client.close()

# @mcp.tool()
# def add_item(user_id: str, product_id: str, quantity: int) -> dict:
#     client = CartClient(target="localhost:7070")
#     try:
#         _ = client.add_item(user_id,product_id,quantity)
#         logger.info(f"Add item response: {_}")
#         return {"status": "OK"}
#     finally:
#         client.close()


# def place_order(user_id: str, user_currency: str, street_address: str, city: str, state: str, country: str, zip_code: int, email: str, credit_card_number: str, credit_card_cvv: int, credit_card_expiration_year: int, credit_card_expiration_month: int) -> dict:
#     client = CheckoutClient(target="localhost:5050")
#     try:
#         resp = client.place_order(
#             user_id, user_currency, street_address, city, state, country, zip_code, email, credit_card_number, credit_card_cvv, credit_card_expiration_year, credit_card_expiration_month
#         )
#         logger.info(f"Place order response: {resp.to_dict()}")
#         return resp.to_dict()
#     finally:
#         client.close()


# def build_parser() -> argparse.ArgumentParser:
#     parser = argparse.ArgumentParser(description="Run gRPC client calls against Hipster Shop services")
#     sub = parser.add_subparsers(dest="cmd", required=True)

#     p = sub.add_parser("search", help="Search products")
#     p.add_argument("--query", required=True)
#     p.add_argument("--target", default="localhost:3550", help="ProductCatalogService host:port")
#     p.set_defaults(func=cmd_search)

#     p = sub.add_parser("add-item", help="Add item to cart")
#     p.add_argument("--user-id", required=True)
#     p.add_argument("--product-id", required=True)
#     p.add_argument("--quantity", type=int, default=1)
#     p.add_argument("--target", default="localhost:7070", help="CartService host:port")
#     p.set_defaults(func=cmd_add_item)

#     p = sub.add_parser("place-order", help="Place checkout order")
#     p.add_argument("--user-id", required=True)
#     p.add_argument("--user-currency", required=True)
#     p.add_argument("--street", required=True)
#     p.add_argument("--city", required=True)
#     p.add_argument("--state", required=True)
#     p.add_argument("--country", required=True)
#     p.add_argument("--zip", type=int, required=True)
#     p.add_argument("--email", required=True)
#     p.add_argument("--cc-number", required=True)
#     p.add_argument("--cc-cvv", type=int, required=True)
#     p.add_argument("--cc-year", type=int, required=True)
#     p.add_argument("--cc-month", type=int, required=True)
#     p.add_argument("--target", default="localhost:5050", help="CheckoutService host:port")
#     p.set_defaults(func=cmd_place_order)

#     return parser


def main():
    mcp.run()  # Defaults to STDIO
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp")
    # mcp.run(transport="sse", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
