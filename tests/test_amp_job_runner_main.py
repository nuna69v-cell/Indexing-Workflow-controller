import pytest
import sys
from unittest.mock import patch, MagicMock, AsyncMock
from amp_job_runner import main

@pytest.fixture
def mock_runner():
    with patch("amp_job_runner.AMPJobRunner") as MockRunner:
        runner_instance = MagicMock()
        runner_instance.run_next_job = AsyncMock()
        runner_instance.run_deploy_job = AsyncMock()
        MockRunner.return_value = runner_instance
        yield runner_instance

@pytest.mark.asyncio
async def test_main_status_command(mock_runner):
    with patch.object(sys, "argv", ["amp_job_runner.py", "status"]):
        await main()
        mock_runner.show_status.assert_called_once()
        mock_runner.run_next_job.assert_not_called()
        mock_runner.run_deploy_job.assert_not_called()

@pytest.mark.asyncio
async def test_main_run_command(mock_runner):
    with patch.object(sys, "argv", ["amp_job_runner.py", "run"]):
        await main()
        mock_runner.run_next_job.assert_awaited_once()
        mock_runner.show_status.assert_not_called()
        mock_runner.run_deploy_job.assert_not_called()

@pytest.mark.asyncio
async def test_main_deploy_command(mock_runner):
    with patch.object(sys, "argv", ["amp_job_runner.py", "deploy"]):
        await main()
        mock_runner.run_deploy_job.assert_awaited_once()
        mock_runner.show_status.assert_not_called()
        mock_runner.run_next_job.assert_not_called()

@pytest.mark.asyncio
async def test_main_unknown_command(mock_runner):
    with patch.object(sys, "argv", ["amp_job_runner.py", "unknown"]):
        with patch("builtins.print") as mock_print:
            await main()
            mock_print.assert_called_once_with("Usage: python amp_job_runner.py [status|run|deploy]")
            mock_runner.show_status.assert_not_called()
            mock_runner.run_next_job.assert_not_called()
            mock_runner.run_deploy_job.assert_not_called()

@pytest.mark.asyncio
async def test_main_no_arguments(mock_runner):
    with patch.object(sys, "argv", ["amp_job_runner.py"]):
        with patch("builtins.print") as mock_print:
            await main()

            # Check if print was called with expected lines
            expected_calls = [
                "🚀 AMP Job Runner",
                "Available commands:",
                "  status - Show AMP status",
                "  run    - Execute next job",
                "  deploy - Execute deployment job",
                "\nExample: python amp_job_runner.py deploy"
            ]

            calls = [call.args[0] for call in mock_print.call_args_list]
            for expected in expected_calls:
                assert expected in calls

            mock_runner.show_status.assert_not_called()
            mock_runner.run_next_job.assert_not_called()
            mock_runner.run_deploy_job.assert_not_called()
