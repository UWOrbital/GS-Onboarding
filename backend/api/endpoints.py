from fastapi import APIRouter

resource = APIRouter()


@resource.get("/")
async def get_items():
    """
    Gets all the items

    @return Returns a list of items
    """
    return {"Hello": "World"}


@resource.post("/")
async def create_item(payload):
    """
    Creates an item with the given payload and returns the payload with some other information

    @param payload: The data used to create an item
    @return returns the data with some other information
    """
    # TODO: Implement this endpoint


@resource.delete("/{id}")
async def delete_item(id: int):
    """
    Deletes the item with the given id if it exists. Otherwise raises a 404 error.

    @param id: The id of the item to delete
    """
    # TODO: Implement this endpoint
