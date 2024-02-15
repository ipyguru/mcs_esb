from typing import Union
from fastapi import APIRouter

from item.schema import Item

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@router.put("/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
