from fastapi.testclient import TestClient
import urllib.parse


from .main import app

client = TestClient(app)

def test_get():
    response = client.get("/get")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_valid_csrf_headers():
    csrf_token = client.cookies.get("cookie_name")
    response = client.post(
        "/post1",
        headers={"header_name": csrf_token},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }

def test_valid_csrf_input_form():
    response = client.get("/form")
    assert response.status_code == 200

    form_data = response.content
    
    print(form_data)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/post2",
        data = form_data,
        headers=headers,        
    )
    assert response.status_code == 200