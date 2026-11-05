def test_user_can_register_and_login(client):
    response = client.post(
        "/register",
        data={
            "username": "testowner",
            "email": "owner@test.local",
            "password": "TestPassword123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    response = client.post(
        "/login",
        data={
            "username": "testowner",
            "password": "TestPassword123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
