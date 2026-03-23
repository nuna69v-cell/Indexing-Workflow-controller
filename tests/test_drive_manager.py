import sys
from unittest.mock import patch, MagicMock

# Mock out Windows-specific modules if they are imported elsewhere
sys.modules["winreg"] = MagicMock()

from utils.drive_manager import DriveManager  # noqa: E402


class TestDriveManager:
    @patch("utils.drive_manager.platform.system")
    @patch("utils.drive_manager.os.path.exists")
    @patch("utils.drive_manager.subprocess.check_output")
    def test_get_available_drives_windows(
        self, mock_check_output, mock_path_exists, mock_system
    ):
        # Setup mocks
        mock_system.return_value = "Windows"

        # We only want one drive to exist for the test (E:)
        def mock_exists_side_effect(path):
            if path == "E:\\":
                return True
            return False

        mock_path_exists.side_effect = mock_exists_side_effect
        mock_check_output.return_value = b"Volume in drive E is TestDriveLabel"  # To ensure output.decode().split()[-1] returns TestDriveLabel

        # Run function
        manager = DriveManager()
        drives = manager.get_available_drives()

        # Verify
        assert len(drives) == 1
        assert drives[0]["letter"] == "E:"
        assert drives[0]["label"] == "TestDriveLabel"

        # Verify the secure subprocess call
        mock_check_output.assert_called_once_with(["cmd.exe", "/c", "vol", "E:"])

    @patch("utils.drive_manager.platform.system")
    @patch("utils.drive_manager.os.path.exists")
    @patch("utils.drive_manager.subprocess.check_output")
    def test_get_available_drives_windows_no_label(
        self, mock_check_output, mock_path_exists, mock_system
    ):
        # Setup mocks
        mock_system.return_value = "Windows"

        # We only want one drive to exist for the test (F:)
        def mock_exists_side_effect(path):
            if path == "F:\\":
                return True
            return False

        mock_path_exists.side_effect = mock_exists_side_effect

        # Simulate subprocess failure (e.g. permission denied)
        import subprocess

        mock_check_output.side_effect = subprocess.CalledProcessError(1, "cmd")

        # Run function
        manager = DriveManager()
        drives = manager.get_available_drives()

        # Verify
        assert len(drives) == 1
        assert drives[0]["letter"] == "F:"
        assert drives[0]["label"] == "Unknown"

        # Verify the secure subprocess call
        mock_check_output.assert_called_once_with(["cmd.exe", "/c", "vol", "F:"])

    @patch("utils.drive_manager.platform.system")
    def test_get_available_drives_non_windows(self, mock_system):
        # Setup mocks
        mock_system.return_value = "Linux"

        # Run function
        manager = DriveManager()
        drives = manager.get_available_drives()

        # Verify (currently the implementation returns empty list for non-Windows)
        assert len(drives) == 0
