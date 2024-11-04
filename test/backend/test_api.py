
def test_get_commands(fastapi_test_client, commands_json):
    with fastapi_test_client as client: 
        response = client.get("/commands/")
        assert response.status_code == 200
        assert response.json() == {"data": commands_json} 
