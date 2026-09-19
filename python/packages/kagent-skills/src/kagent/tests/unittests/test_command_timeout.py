import pytest

from kagent.skills.shell import _get_command_timeout_seconds, execute_command


@pytest.mark.parametrize("command", ["echo hello", "python script.py", "python3 script.py"])
def test_configured_timeout_overrides_command_defaults(monkeypatch, command):
    monkeypatch.setenv("KAGENT_COMMAND_TIMEOUT", "120")
    assert _get_command_timeout_seconds(command) == 120


@pytest.mark.asyncio
async def test_configured_timeout_is_enforced(monkeypatch, tmp_path):
    monkeypatch.setenv("KAGENT_COMMAND_TIMEOUT", "1")
    result = await execute_command("exec sleep 2", working_dir=tmp_path)
    assert result == "Error: Command timed out after 1s"


@pytest.mark.parametrize(
    "configured", [None, "", "0", "-1", "1.5", "NaN", "Inf", "1s", "invalid", "1_0", "９", "9223372037", "9" * 5000]
)
@pytest.mark.parametrize("command, expected", [("echo hello", 30), ("python script.py", 60), ("python3 script.py", 60)])
def test_invalid_or_unset_timeout_preserves_defaults(monkeypatch, configured, command, expected):
    if configured is None:
        monkeypatch.delenv("KAGENT_COMMAND_TIMEOUT", raising=False)
    else:
        monkeypatch.setenv("KAGENT_COMMAND_TIMEOUT", configured)
    assert _get_command_timeout_seconds(command) == expected


@pytest.mark.parametrize("configured", [" 120 ", "00120"])
def test_configured_timeout_accepts_whitespace_and_leading_zeroes(monkeypatch, configured):
    monkeypatch.setenv("KAGENT_COMMAND_TIMEOUT", configured)
    assert _get_command_timeout_seconds("echo hello") == 120
