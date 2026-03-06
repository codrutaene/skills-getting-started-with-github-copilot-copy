"""Unit tests for business logic of the activities management system using AAA pattern."""

import pytest


class TestActivityValidation:
    """Unit tests for activity validation logic."""

    def test_activity_exists_in_dict(self, sample_activities):
        """
        Test checking if activity exists in activities dictionary.
        
        Arrange: Setup activities dict with known activities
        Act: Check if known activity exists
        Assert: Verify activity found
        """
        # Arrange
        activity_name = "Chess Club"

        # Act
        activity_exists = activity_name in sample_activities

        # Assert
        assert activity_exists is True

    def test_activity_not_exists_in_dict(self, sample_activities):
        """
        Test checking if non-existent activity returns False.
        
        Arrange: Setup activities dict
        Act: Check for non-existent activity
        Assert: Verify activity not found
        """
        # Arrange
        activity_name = "Nonexistent Activity"

        # Act
        activity_exists = activity_name in sample_activities

        # Assert
        assert activity_exists is False

    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Drama Club",
        "Debate Team",
        "Science Club"
    ])
    def test_all_default_activities_exist(self, sample_activities, activity_name):
        """
        Test all default activities exist in the dictionary.
        
        Arrange: Setup activities dict
        Act: Check each default activity
        Assert: Verify all exist
        """
        # Act
        activity_exists = activity_name in sample_activities

        # Assert
        assert activity_exists is True


class TestParticipantManagement:
    """Unit tests for participant list management."""

    def test_participant_in_list(self, sample_activities):
        """
        Test checking if participant is in activity's participant list.
        
        Arrange: Setup activity with known participants
        Act: Check if known participant in list
        Assert: Verify participant found
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        is_participant = email in sample_activities[activity_name]["participants"]

        # Assert
        assert is_participant is True

    def test_participant_not_in_list(self, sample_activities):
        """
        Test checking if non-existent participant is not in list.
        
        Arrange: Setup activity
        Act: Check for non-existent participant
        Assert: Verify participant not found
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notmember@mergington.edu"

        # Act
        is_participant = email in sample_activities[activity_name]["participants"]

        # Assert
        assert is_participant is False

    def test_add_participant_to_list(self, sample_activities):
        """
        Test adding a new participant to an activity.
        
        Arrange: Setup activity and new email
        Act: Add email to participants list
        Assert: Verify email added and list length increased
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = "newstudent@mergington.edu"
        initial_count = len(sample_activities[activity_name]["participants"])

        # Act
        sample_activities[activity_name]["participants"].append(new_email)

        # Assert
        assert new_email in sample_activities[activity_name]["participants"]
        assert len(sample_activities[activity_name]["participants"]) == initial_count + 1

    def test_remove_participant_from_list(self, sample_activities):
        """
        Test removing a participant from an activity.
        
        Arrange: Setup activity with known participant
        Act: Remove participant email from list
        Assert: Verify email removed and list length decreased
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "james@mergington.edu"
        initial_count = len(sample_activities[activity_name]["participants"])
        assert email in sample_activities[activity_name]["participants"]

        # Act
        sample_activities[activity_name]["participants"].remove(email)

        # Assert
        assert email not in sample_activities[activity_name]["participants"]
        assert len(sample_activities[activity_name]["participants"]) == initial_count - 1

    @pytest.mark.parametrize("email", [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ])
    def test_add_multiple_participants(self, sample_activities, email):
        """
        Test adding multiple different participants.
        
        Arrange: Setup activity and various emails
        Act: Add each email
        Assert: Verify each email added successfully
        """
        # Arrange
        activity_name = "Art Studio"

        # Act
        sample_activities[activity_name]["participants"].append(email)

        # Assert
        assert email in sample_activities[activity_name]["participants"]

    def test_participant_list_isolation(self, sample_activities):
        """
        Test that modifying one activity's participants doesn't affect others.
        
        Arrange: Setup two different activities
        Act: Add participant to one activity
        Assert: Verify other activity's participants unchanged
        """
        # Arrange
        activity1 = "Chess Club"
        activity2 = "Drama Club"
        new_email = "newperson@mergington.edu"
        drama_initial_count = len(sample_activities[activity2]["participants"])

        # Act
        sample_activities[activity1]["participants"].append(new_email)

        # Assert
        assert new_email in sample_activities[activity1]["participants"]
        assert new_email not in sample_activities[activity2]["participants"]
        assert len(sample_activities[activity2]["participants"]) == drama_initial_count


class TestActivityMetadata:
    """Unit tests for activity metadata validation."""

    def test_activity_has_description(self, sample_activities):
        """
        Test all activities have description field.
        
        Arrange: Setup activities dict
        Act: Check for description in each activity
        Assert: Verify all have descriptions
        """
        # Act & Assert
        for activity_name, activity_data in sample_activities.items():
            assert "description" in activity_data, \
                f"{activity_name} missing description"
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0

    def test_activity_has_schedule(self, sample_activities):
        """
        Test all activities have schedule field.
        
        Arrange: Setup activities dict
        Act: Check for schedule in each activity
        Assert: Verify all have schedules
        """
        # Act & Assert
        for activity_name, activity_data in sample_activities.items():
            assert "schedule" in activity_data, \
                f"{activity_name} missing schedule"
            assert isinstance(activity_data["schedule"], str)
            assert len(activity_data["schedule"]) > 0

    def test_activity_has_max_participants(self, sample_activities):
        """
        Test all activities have max_participants field.
        
        Arrange: Setup activities dict
        Act: Check for max_participants in each activity
        Assert: Verify all have valid max_participants
        """
        # Act & Assert
        for activity_name, activity_data in sample_activities.items():
            assert "max_participants" in activity_data, \
                f"{activity_name} missing max_participants"
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_activity_has_participants_list(self, sample_activities):
        """
        Test all activities have participants list.
        
        Arrange: Setup activities dict
        Act: Check for participants in each activity
        Assert: Verify all have participant lists
        """
        # Act & Assert
        for activity_name, activity_data in sample_activities.items():
            assert "participants" in activity_data, \
                f"{activity_name} missing participants"
            assert isinstance(activity_data["participants"], list)
            # Verify all participants are email strings
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant

    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Class",
        "Gym Class"
    ])
    def test_initial_participants_match_expected(self, sample_activities, activity_name):
        """
        Test that initial participants match expected counts.
        
        Arrange: Setup activities and expected counts
        Act: Check initial participant counts
        Assert: Verify counts match
        """
        # Arrange
        expected_counts = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2
        }

        # Act
        actual_count = len(sample_activities[activity_name]["participants"])

        # Assert
        assert actual_count == expected_counts[activity_name]


class TestDuplicateDetection:
    """Unit tests for duplicate participant detection."""

    def test_detect_duplicate_participant(self, sample_activities):
        """
        Test detecting duplicate participant in list.
        
        Arrange: Setup activity with participants
        Act: Check if known participant exists
        Assert: Verify duplicate detected
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        is_duplicate = email in sample_activities[activity_name]["participants"]

        # Assert
        assert is_duplicate is True

    def test_no_duplicate_for_new_participant(self, sample_activities):
        """
        Test new participant not detected as duplicate.
        
        Arrange: Setup activity and new email
        Act: Check if new email exists
        Assert: Verify not a duplicate
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "neweight@mergington.edu"

        # Act
        is_duplicate = new_email in sample_activities[activity_name]["participants"]

        # Assert
        assert is_duplicate is False

    @pytest.mark.parametrize("email,is_expected_duplicate", [
        ("michael@mergington.edu", True),
        ("daniel@mergington.edu", True),
        ("nonexistent@mergington.edu", False),
        ("another@mergington.edu", False)
    ])
    def test_duplicate_detection_parametrized(self, sample_activities, email, is_expected_duplicate):
        """
        Test duplicate detection with multiple email scenarios.
        
        Arrange: Setup activities and various emails
        Act: Check if each email is in Chess Club
        Assert: Verify expected duplicate status
        """
        # Act
        is_duplicate = email in sample_activities["Chess Club"]["participants"]

        # Assert
        assert is_duplicate == is_expected_duplicate
