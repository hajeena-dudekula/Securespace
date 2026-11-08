def test_profile_requires_login(client):
    response = client.get("/profile")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_profile_displays_current_user_details(
    client, users, login_as
):
    login_as("testowner", "OwnerPass123!")

    response = client.get("/profile")

    assert response.status_code == 200
    assert b"testowner" in response.data
    assert b"owner@test.local" in response.data
    assert b"Owner" in response.data
    assert b"Member Since" in response.data


def test_dashboard_profile_links_to_profile_page(
    client, users, login_as
):
    login_as("testowner", "OwnerPass123!")

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b'href="/profile"' in response.data
