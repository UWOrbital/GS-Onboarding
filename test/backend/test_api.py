
from fastapi.testclient import TestClient

from backend.api.models.request_model import CommandRequest
from backend.data.enums import CommandStatus


def test_get_commands(fastapi_test_client: TestClient, commands_json):
    with fastapi_test_client as client: 
        res = client.get("/commands/")
        assert res.status_code == 200
        assert res.json() == {"data": commands_json} 


def test_create_command(fastapi_test_client: TestClient): 
    command = CommandRequest(command_type=1, params="123456789")
    model_dump = command.model_dump()
    print(model_dump)
    with fastapi_test_client as client:
        res = client.post("/commands/", json=model_dump, headers={"Content-Type": "application/json"})
        # res = client.post("/commands/", json=command)
        res.raise_for_status()
        assert res.status_code == 200
        result = res.json().get("data")
        assert result is not None
        assert result.get("id") == 3
        assert result.get("command_type") == 1
        assert result.get("status") == CommandStatus.PENDING.value
        assert result.get("params") == "123456789"
        # TODO: Figure out a better way to check the times
        assert result.get("created_on") 
        assert result.get("updated_on")
