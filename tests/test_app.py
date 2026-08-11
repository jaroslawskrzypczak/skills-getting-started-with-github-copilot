from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_data():
    # Arrange
    # No setup needed for this simple endpoint.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_for_activity_adds_participant():
    # Arrange
    original_participants = list(activities["Chess Club"]["participants"])

    # Act
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")

    # Assert
    assert response.status_code == 200
    assert "test@example.com" in activities["Chess Club"]["participants"]

    # Cleanup
    activities["Chess Club"]["participants"] = original_participants


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    original_participants = list(activities["Chess Club"]["participants"])

    # Act
    response = client.delete("/activities/Chess%20Club/participants/michael@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    # Cleanup
    activities["Chess Club"]["participants"] = original_participants
