from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_activity_data():
    # Arrange
    expected_keys = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert expected_keys.issubset(set(activities.keys()))
    assert all("description" in details for details in activities.values())
    assert all("participants" in details for details in activities.values())


def test_signup_for_activity_adds_new_participant():
    # Arrange
    email = "test.student@mergington.edu"
    activity_name = "Programming Class"
    signup_url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    signup_response = client.post(signup_url)

    # Assert
    assert signup_response.status_code == 200
    assert "Signed up" in signup_response.json()["message"]

    activity_response = client.get("/activities")
    assert activity_response.status_code == 200
    activity = activity_response.json()[activity_name]
    assert email in activity["participants"]


def test_remove_participant_unregisters_student():
    # Arrange
    email = "delete.me@mergington.edu"
    activity_name = "Chess Club"
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    client.post(signup_url)
    delete_url = f"/activities/{activity_name}/participants?email={email}"

    # Act
    delete_response = client.delete(delete_url)

    # Assert
    assert delete_response.status_code == 200
    assert "Removed" in delete_response.json()["message"]

    activity_response = client.get("/activities")
    assert activity_response.status_code == 200
    activity = activity_response.json()[activity_name]
    assert email not in activity["participants"]
