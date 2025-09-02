from __future__ import annotations

import argparse

from green_next_client.grpc_clients import (
    ProductCatalogClient,
    CartClient,
    CheckoutClient,
)


def cmd_search(args: argparse.Namespace) -> None:
    client = ProductCatalogClient(target=args.target)
    try:
        resp = client.search_products(query=args.query)
        print(resp)
    finally:
        client.close()


def cmd_add_item(args: argparse.Namespace) -> None:
    client = CartClient(target=args.target)
    try:
        _ = client.add_item(user_id=args.user_id, product_id=args.product_id, quantity=args.quantity)
        print("OK")
    finally:
        client.close()


def cmd_place_order(args: argparse.Namespace) -> None:
    client = CheckoutClient(target=args.target)
    try:
        resp = client.place_order(
            user_id=args.user_id,
            user_currency=args.user_currency,
            street_address=args.street,
            city=args.city,
            state=args.state,
            country=args.country,
            zip_code=args.zip,
            email=args.email,
            credit_card_number=args.cc_number,
            credit_card_cvv=args.cc_cvv,
            credit_card_expiration_year=args.cc_year,
            credit_card_expiration_month=args.cc_month,
        )
        print(resp)
    finally:
        client.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run gRPC client calls against Hipster Shop services")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search", help="Search products")
    p.add_argument("--query", required=True)
    p.add_argument("--target", default="localhost:3550", help="ProductCatalogService host:port")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("add-item", help="Add item to cart")
    p.add_argument("--user-id", required=True)
    p.add_argument("--product-id", required=True)
    p.add_argument("--quantity", type=int, default=1)
    p.add_argument("--target", default="localhost:7070", help="CartService host:port")
    p.set_defaults(func=cmd_add_item)

    p = sub.add_parser("place-order", help="Place checkout order")
    p.add_argument("--user-id", required=True)
    p.add_argument("--user-currency", required=True)
    p.add_argument("--street", required=True)
    p.add_argument("--city", required=True)
    p.add_argument("--state", required=True)
    p.add_argument("--country", required=True)
    p.add_argument("--zip", type=int, required=True)
    p.add_argument("--email", required=True)
    p.add_argument("--cc-number", required=True)
    p.add_argument("--cc-cvv", type=int, required=True)
    p.add_argument("--cc-year", type=int, required=True)
    p.add_argument("--cc-month", type=int, required=True)
    p.add_argument("--target", default="localhost:5050", help="CheckoutService host:port")
    p.set_defaults(func=cmd_place_order)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
