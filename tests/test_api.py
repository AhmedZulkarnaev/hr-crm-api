"""Тесты регистрации и аутентификации пользователей API."""


def test_register_user(client):
    """Проверяем, что эндпоинт регистрации работает корректно."""
    response = client.post(
        "/users/",
        json={
            "username": "robot_tester",
            "email": "testrobot@example.com",
            "password": "supersecretpassword",
            "role": "candidate",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "testrobot@example.com"
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_user(client):
    """Проверяем, что нельзя зарегистрировать двух юзеров с одним email."""
    user_data = {
        "email": "clone@example.com",
        "username": "clone_user",
        "password": "password123",
        "role": "candidate",
    }

    response1 = client.post("/users/", json=user_data)
    assert response1.status_code == 200

    response2 = client.post("/users/", json=user_data)
    assert response2.status_code == 400
    assert "detail" in response2.json()


def test_login_success(client):
    """Проверяем успешный логин и получение токена."""

    client.post(
        "/users/",
        json={
            "email": "hr@example.com",
            "username": "hr_boss",
            "password": "strongpassword",
            "role": "hr",
        },
    )

    response = client.post(
        "/users/login",
        json={
            "email": "hr@example.com",
            "password": "strongpassword",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Проверяем, что с неверным паролем токен не выдается."""

    client.post(
        "/users/",
        json={
            "email": "hacker@example.com",
            "username": "hacker",
            "password": "realpassword",
            "role": "candidate",
        },
    )

    response = client.post(
        "/users/login/",
        json={
            "email": "hacker@example.com",
            "password": "WRONG_PASSWORD",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный email или пароль"
