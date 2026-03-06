"""Integration tests for FastAPI activities endpoints using AAA (Arrange-Act-Assert) pattern."""

import pytest
from fastapi.testclient import TestClient


class TestGetActivitiesEndpoint:
    """Tests for GET /activities endpoint."""

    def test_get_activities_success(self, client: TestClient):
        """
        Test successful retrieval of all activities.
        
        Arrange: Setup client with fresh activities
        Act: GET /activities
        Assert: Verify 200 response with activity list
        """
        # Arrange
        expected_activity_names = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Drama Club",
            "Debate Team",
            "Science Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == 9
        for activity_name in expected_activity_names:
            assert activity_name in activities
            assert "description" in activities[activity_name]
            assert "schedule" in activities[activity_name]
            assert "max_participants" in activities[activity_name]
            assert "participants" in activities[activity_name]
            assert isinstance(activities[activity_name]["participants"], list)

    def test_get_activities_response_structure(self, client: TestClient):
        """
        Test response structure contains expected fields for each activity.
        
        Arrange: Setup client
        Act: GET /activities
        Assert: Verify all required fields present
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields, \
                f"Activity {activity_name} missing required fields"


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client: TestClient):
        """
        Test successful signup for an activity.
        
        Arrange: Setup client with activity and new participant email
        Act: POST /activities/{activity}/signup
        Assert: Verify 200 response and participant added
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client: TestClient):
        """
        Test signup fails when activity doesn't exist.
        
        Arrange: Setup client with invalid activity name
        Act: POST /activities/{invalid}/signup
        Assert: Verify 404 response
        """
        # Arrange
        activity_name = "NonexistentActivity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_already_registered(self, client: TestClient):
        """
        Test signup fails when student is already registered.
        
        Arrange: Setup activity with existing participant, use same email
        Act: POST /activities/{activity}/signup with existing email
        Assert: Verify 400 response and participants list unchanged
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club

        # Get initial participant count
        activities_response = client.get("/activities")
        initial_participants = activities_response.json()[activity_name]["participants"].copy()
        initial_count = len(initial_participants)

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

        # Verify participants list unchanged
        activities_response = client.get("/activities")
        updated_participants = activities_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_count
        assert updated_participants == initial_participants

    def test_signup_multiple_participants(self, client: TestClient):
        """
        Test multiple participants can be added to an activity.
        
        Arrange: Setup activity and new participant emails
        Act: POST signup for multiple different emails
        Assert: Verify all participants added successfully
        """
        # Arrange
        activity_name = "Programming Class"
        new_emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]

        # Act & Assert
        for email in new_emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Verify all participants added
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        for email in new_emails:
            assert email in participants


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/participants endpoint."""

    def test_unregister_success(self, client: TestClient):
        """
        Test successful unregistration from an activity.
        
        Arrange: Setup activity with existing participant
        Act: DELETE /activities/{activity}/participants
        Assert: Verify 200 response and participant removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Get initial count
        activities_response = client.get("/activities")
        initial_count = len(activities_response.json()[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

        # Verify participant was removed
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email not in participants
        assert len(participants) == initial_count - 1

    def test_unregister_activity_not_found(self, client: TestClient):
        """
        Test unregister fails when activity doesn't exist.
        
        Arrange: Setup client with invalid activity name
        Act: DELETE /activities/{invalid}/participants
        Assert: Verify 404 response
        """
        # Arrange
        activity_name = "NonexistentActivity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_not_registered(self, client: TestClient):
        """
        Test unregister fails when student is not registered.
        
        Arrange: Setup activity and email not in participants
        Act: DELETE /activities/{activity}/participants with non-participant
        Assert: Verify 400 response and participants list unchanged
        """
        # Arrange
        activity_name = "Chess Club"
        unregistered_email = "notregistered@mergington.edu"

        # Get initial participants
        activities_response = client.get("/activities")
        initial_participants = activities_response.json()[activity_name]["participants"].copy()
        initial_count = len(initial_participants)

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": unregistered_email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student not signed up for this activity"

        # Verify participants list unchanged
        activities_response = client.get("/activities")
        updated_participants = activities_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_count
        assert updated_participants == initial_participants

    def test_unregister_multiple_participants(self, client: TestClient):
        """
        Test removing multiple participants from an activity.
        
        Arrange: Setup activity with known participants
        Act: DELETE /activities/{activity}/participants for multiple emails
        Assert: Verify all participants removed successfully
        """
        # Arrange
        activity_name = "Tennis Club"
        emails_to_remove = ["james@mergington.edu", "sarah@mergington.edu"]

        # Act & Assert
        for email in emails_to_remove:
            response = client.delete(
                f"/activities/{activity_name}/participants",
                params={"email": email}
            )
            assert response.status_code == 200

        # Verify all participants removed
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        for email in emails_to_remove:
            assert email not in participants


class TestSignupAndUnregisterFlow:
    """Integration tests for combined signup and unregister workflows."""

    def test_signup_then_unregister(self, client: TestClient):
        """
        Test complete flow: signup for activity, then unregister.
        
        Arrange: Setup client and new email
        Act: POST signup, then DELETE unregister
        Assert: Verify participant added then removed
        """
        # Arrange
        activity_name = "Debate Team"
        email = "newdebater@mergington.edu"

        # Act - Signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert signup
        assert signup_response.status_code == 200

        # Verify participant added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity_name]["participants"]

        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert unregister
        assert unregister_response.status_code == 200

        # Verify participant removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()[activity_name]["participants"]

    def test_signup_unregister_signup_again(self, client: TestClient):
        """
        Test student can unregister and re-register for the same activity.
        
        Arrange: Setup client and email
        Act: POST signup, DELETE unregister, POST signup again
        Assert: Verify all operations succeed
        """
        # Arrange
        activity_name = "Art Studio"
        email = "artist@mergington.edu"

        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200

        # Act - Unregister
        response2 = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        assert response2.status_code == 200

        # Act - Re-signup
        response3 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert - All operations succeed
        assert response3.status_code == 200

        # Verify final state: participant is registered
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity_name]["participants"]
