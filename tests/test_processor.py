"""
test_processor.py
Tests the FFmpeg command generation logic.
"""

from config.presets import PRESETS
from core.processor import build_command


def test_build_command_cpu():
    """Test CPU command generation (Lecture Mode)."""
    preset = PRESETS["1"]
    cmd = build_command("in.mp4", "out.mp4", preset, gpu_codec=None)

    assert "libx264" in cmd
    assert "-tune" in cmd
    assert "out.mp4" in cmd


def test_build_command_gpu_nvenc():
    """Test GPU command generation (HQ Mode)."""
    preset = PRESETS["2"]
    cmd = build_command("in.mp4", "out.mp4", preset, gpu_codec="h264_nvenc")

    assert "h264_nvenc" in cmd
    assert "-rc" in cmd


def test_build_command_hevc_archive():
    """Test Archive command generation (HEVC)."""
    preset = PRESETS["5"]
    cmd = build_command("in.mp4", "out.mp4", preset, gpu_codec="hevc_nvenc")

    # Should use HEVC encoder
    assert "hevc_nvenc" in cmd
    # Should NOT use H.264
    assert "h264_nvenc" not in cmd


def test_build_command_gpu_fallback():
    """Test Fallback to CPU when GPU is missing."""
    preset = PRESETS["2"]
    # Pass None as gpu_codec
    cmd = build_command("in.mp4", "out.mp4", preset, gpu_codec=None)

    # Should fallback to CPU (libx264)
    assert "libx264" in cmd
    assert "h264_nvenc" not in cmd
