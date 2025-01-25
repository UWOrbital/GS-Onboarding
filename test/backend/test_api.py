from fastapi.testclient import TestClient
from backend.api.models.request_model import CommandRequest
from backend.data.enums import CommandStatus
from backend.utils.time import to_unix_time


def test_get_commands(fastapi_test_client: TestClient, commands_json):
    with fastapi_test_client as client: 
        res = client.get("/commands/")
        assert res.status_code == 200
        assert res.json() == {"data": commands_json} 


def test_create_command(fastapi_test_client: TestClient): 
    command = CommandRequest(command_type=1, params="123456789")
    model_dump = command.model_dump()
    with fastapi_test_client as client:
        res = client.post("/commands/", json=model_dump, headers={"Content-Type": "application/json"})
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

def test_delete_command_fail(fastapi_test_client: TestClient):
    with fastapi_test_client as client:
        res = client.delete("/commands/0") # Should never have an id of 0 in the db
        assert res.status_code == 404

def test_delete_command(fastapi_test_client: TestClient, default_datetime):
    with fastapi_test_client as client:
        res = client.delete("/commands/1")
        assert res.status_code == 200
        result = res.json().get("data")
        assert result is not None
        assert len(result) == 1 # Should only have 1 element in db
        result = result[0]
        assert result.get("id") == 2
        assert result.get("command_type") == 2
        assert result.get("status") == CommandStatus.PENDING.value
        assert result.get("params") == f"1,{to_unix_time(default_datetime)}"
        # TODO: Figure out a better way to check the times
        assert result.get("created_on") 
        assert result.get("updated_on")


def test_main_commands(fastapi_test_client: TestClient):
    with fastapi_test_client as client:
        res = client.get("/main-commands/")
        assert res.status_code == 200
        result = res.json().get("data")
        assert result is not None
        assert len(result) == 2 
        main_command = result[0]
        assert main_command.get("id") == 1
        assert main_command.get("name") == "RTC Sync"
        assert main_command.get("params") == "time"
        assert main_command.get("format") == "int 7 bytes" 
        assert main_command.get("data_size") == 7
        assert main_command.get("total_size") == 8
        main_command = result[1]
        assert main_command.get("id") == 2
        assert main_command.get("name") == "Manually activate an emergency mode for a specified amount of time"
        assert main_command.get("params") == "mode_state_number,time"
        assert main_command.get("format") == "int 1 byte, int 7 bytes" 
        assert main_command.get("data_size") == 8
        assert main_command.get("total_size") == 9
        
