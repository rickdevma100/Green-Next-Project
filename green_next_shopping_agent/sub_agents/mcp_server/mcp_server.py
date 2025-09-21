from __future__ import annotations

import logging
import os
from typing import Any
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

from grpc_clients import (
    ProductCatalogClient,
    CartClient,
    CheckoutClient,
)

# Service endpoints - use environment variables for containerized deployment
PRODUCT_CATALOG_SERVICE = os.getenv("PRODUCT_CATALOG_SERVICE", "productcatalogservice:3550")
CART_SERVICE = os.getenv("CART_SERVICE", "cartservice:7070") 
CHECKOUT_SERVICE = os.getenv("CHECKOUT_SERVICE", "checkoutservice:5050")

# Debug: Log the actual values being used
logger.info(f"PRODUCT_CATALOG_SERVICE: {PRODUCT_CATALOG_SERVICE}")
logger.info(f"CART_SERVICE: {CART_SERVICE}")
logger.info(f"CHECKOUT_SERVICE: {CHECKOUT_SERVICE}")

# Create server
mcp = FastMCP("FastMCP Server for Green Next Shopping")
ip_address = os.getenv("IP_ADDRESS", "http://35.185.109.77/")
@mcp.tool()
def search_products(product_name: str) -> dict[str, Any]:
    logger.info(f"search_products called with target: {PRODUCT_CATALOG_SERVICE}")
    client = ProductCatalogClient(target=PRODUCT_CATALOG_SERVICE)
    try:
        resp = client.search_products(product_name)
        
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

@mcp.tool()
def list_products() -> dict[str, Any]:
    client = ProductCatalogClient(target=PRODUCT_CATALOG_SERVICE)
    try:
        resp = client.list_products()
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
            for p in resp.products]}
    finally:
        client.close()

@mcp.tool()
def add_item(user_id: str, product_id: str, quantity: int) -> dict:
    client = CartClient(target=CART_SERVICE)
    try:
        _ = client.add_item(user_id,product_id,quantity)
        logger.info(f"Add item response: {_}")
        return {"status": "OK"}
    finally:
        client.close()

@mcp.tool()
def place_order(user_id: str, user_currency: str, street_address: str, city: str, state: str, country: str, zip_code: int, email: str, credit_card_number: str, credit_card_cvv: int, credit_card_expiration_year: int, credit_card_expiration_month: int) -> dict:
    client = CheckoutClient(target=CHECKOUT_SERVICE)
    try:
        resp = client.place_order(
            user_id, user_currency, street_address, city, state, country, zip_code, email, credit_card_number, credit_card_cvv, credit_card_expiration_year, credit_card_expiration_month
        )
        result = {
            "order": {
                "order_id": resp.order.order_id,
                "shipping_tracking_id": resp.order.shipping_tracking_id,
                "shipping_cost": {
                    "currency_code": resp.order.shipping_cost.currency_code,
                    "units": resp.order.shipping_cost.units,
                    "nanos": resp.order.shipping_cost.nanos
                },
                "shipping_address": {
                    "street_address": resp.order.shipping_address.street_address,
                    "city": resp.order.shipping_address.city,
                    "state": resp.order.shipping_address.state,
                    "country": resp.order.shipping_address.country,
                    "zip_code": resp.order.shipping_address.zip_code
                },
                "items": [
                    {
                        "item": {
                            "product_id": item.item.product_id,
                            "quantity": item.item.quantity
                        },
                        "cost": {
                            "currency_code": item.cost.currency_code,
                            "units": item.cost.units,
                            "nanos": item.cost.nanos
                        }
                    }
                    for item in resp.order.items
                ]
            }
        }
        logger.info(f"Place order response")
        return result
    finally:
        client.close()


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
