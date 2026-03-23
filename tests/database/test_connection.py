import pytest
from unittest.mock import patch, MagicMock
from database.connection import get_db


def test_get_db_success():
    """Test that get_db yields a session and closes it afterward."""
    # Create a mock session object
    mock_session = MagicMock()

    # Patch SessionLocal to return our mock session
    with patch("database.connection.SessionLocal", return_value=mock_session):
        # get_db is a generator, so we need to iterate it
        db_generator = get_db()

        # Get the yielded value
        yielded_db = next(db_generator)

        # Verify it yielded our mock session
        assert yielded_db is mock_session

        # At this point, close shouldn't have been called yet
        mock_session.close.assert_not_called()

        # Trigger the finally block by stopping iteration
        with pytest.raises(StopIteration):
            yielded_db = next(db_generator)

        # Now close should have been called
        mock_session.close.assert_called_once()


def test_get_db_exception():
    """Test that get_db closes the session even if an exception occurs during use."""
    mock_session = MagicMock()

    with patch("database.connection.SessionLocal", return_value=mock_session):
        db_generator = get_db()

        # Get the yielded value
        _yielded_db = next(db_generator)

        # Simulate an exception happening while the caller is using the db
        with pytest.raises(ValueError):
            # Throw an exception back into the generator to trigger the finally block
            db_generator.throw(ValueError("Simulated error during db usage"))

        # Verify close was still called despite the exception
        mock_session.close.assert_called_once()
