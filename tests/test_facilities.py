from utils import RequestMethod


async def test_create_facility(http_request, access_token):
    title = "spa"
    description = "place to relax"
    response = await http_request(
        "/facility",
        method=RequestMethod.POST,
        token=access_token,
        json={"title": title, "description": description},
    )
    assert response.status_code == 201
    data = response.json()
    assert data == {"id": data["id"], "title": title, "description": description}


async def test_get_facilities(http_request, access_token):
    response = await http_request(
        "/facility", method=RequestMethod.GET, token=access_token
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0] == {
        "id": data[0]["id"],
        "title": data[0]["title"],
        "description": data[0]["description"],
    }
