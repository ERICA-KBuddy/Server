# --------------------------------------------------------------------------
# Item model의 schema를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import Optional

from pydantic import BaseModel, Field

from src.db.models import Item


class ItemCreate(BaseModel):
    name: str = Field(..., title="Item Name", description="The name of the item.")
    price: float = Field(..., title="Item Price", description="The price of the item.")
    owner_id: int = Field(..., title="Item Owner", description="The owner of the item.")


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        title="Item Name",
        description="The name of the item. Leave this field empty if you do not want to update it.",
    )
    price: Optional[float] = Field(
        None,
        title="Item Price",
        description="The price of the item. Leave this field empty if you do not want to update it.",
    )


class Item(BaseModel):  # type: ignore
    id: int = Field(
        ..., title="Item ID", description="The unique identifier of the item."
    )
    name: str = Field(..., title="Item Name", description="The name of the item.")
    price: float = Field(..., title="Item Price", description="The price of the item.")
    owner_id: int = Field(..., title="Item Owner", description="The owner of the item.")

    class ConfigDict:
        orm_model = Item
        from_attributes = True
