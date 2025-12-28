"""
test_hardware.py
Tests the GPU detection logic using mocks.
"""

import subprocess
from unittest.mock import patch

from core.hardware import check_encoder, detect_gpu_codec


@patch("subprocess.run")
def test_check_encoder_success(mock_run):
    """Should return True if ffmpeg command succeeds."""
    mock_run.return_value.returncode = 0
    assert check_encoder("h264_nvenc") is True


@patch("subprocess.run")
def test_check_encoder_failure(mock_run):
    """Should return False if ffmpeg command throws an error."""
    mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
    assert check_encoder("h264_nvenc") is False


@patch("core.hardware.check_encoder")
def test_detect_gpu_priority(mock_check):
    """Ensure priority order: NVIDIA -> AMD -> Intel -> Mac."""

    # Simulate: NVIDIA fails, but AMD works
    def side_effect(enc):
        return enc == "h264_amf"

    mock_check.side_effect = side_effect

    result = detect_gpu_codec()
    assert result == "h264_amf"


@patch("core.hardware.check_encoder")
def test_detect_no_gpu(mock_check):
    """Should return None if no hardware encoders work."""
    mock_check.return_value = False
    assert detect_gpu_codec() is None
