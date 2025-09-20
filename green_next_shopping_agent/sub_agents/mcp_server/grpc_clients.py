from __future__ import annotations

import grpc
from typing import Optional

import demo_pb2, demo_pb2_grpc


class ProductCatalogClient:
    def __init__(self, target: str = "productcatalogservice:3550", channel: Optional[grpc.Channel] = None) -> None:
        self._own_channel = channel is None
        self._channel = channel or grpc.insecure_channel(target)
        self._stub = demo_pb2_grpc.ProductCatalogServiceStub(self._channel)

    def search_products(self, query: str) -> demo_pb2.SearchProductsResponse:
        request = demo_pb2.SearchProductsRequest(query=query)
        return self._stub.SearchProducts(request)

    def list_products(self) -> demo_pb2.ListProductsResponse:
        request = demo_pb2.Empty()
        return self._stub.ListProducts(request)
            
    def close(self) -> None:
        if self._own_channel:
            self._channel.close()


class CartClient:
    def __init__(self, target: str = "cartservice:7070", channel: Optional[grpc.Channel] = None) -> None:
        self._own_channel = channel is None
        self._channel = channel or grpc.insecure_channel(target)
        self._stub = demo_pb2_grpc.CartServiceStub(self._channel)

    def add_item(self, user_id: str, product_id: str, quantity: int = 1) -> demo_pb2.Empty:
        request = demo_pb2.AddItemRequest(user_id=user_id, item=demo_pb2.CartItem(product_id=product_id, quantity=quantity))
        return self._stub.AddItem(request)

    def close(self) -> None:
        if self._own_channel:
            self._channel.close()


class CheckoutClient:
    def __init__(self, target: str = "checkoutservice:5050", channel: Optional[grpc.Channel] = None) -> None:
        self._own_channel = channel is None
        self._channel = channel or grpc.insecure_channel(target)
        self._stub = demo_pb2_grpc.CheckoutServiceStub(self._channel)

    def place_order(
        self,
        user_id: str,
        user_currency: str,
        street_address: str,
        city: str,
        state: str,
        country: str,
        zip_code: int,
        email: str,
        credit_card_number: str,
        credit_card_cvv: int,
        credit_card_expiration_year: int,
        credit_card_expiration_month: int,
    ) -> demo_pb2.PlaceOrderResponse:
        address = demo_pb2.Address(
            street_address=street_address,
            city=city,
            state=state,
            country=country,
            zip_code=zip_code,
        )
        credit_card = demo_pb2.CreditCardInfo(
            credit_card_number=credit_card_number,
            credit_card_cvv=credit_card_cvv,
            credit_card_expiration_year=credit_card_expiration_year,
            credit_card_expiration_month=credit_card_expiration_month,
        )
        request = demo_pb2.PlaceOrderRequest(
            user_id=user_id,
            user_currency=user_currency,
            address=address,
            email=email,
            credit_card=credit_card,
        )
        return self._stub.PlaceOrder(request)

    def close(self) -> None:
        if self._own_channel:
            self._channel.close()
