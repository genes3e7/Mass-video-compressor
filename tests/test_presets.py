"""
test_presets.py
Verifies the integrity of the compression profiles.
"""

from config.presets import PRESETS


def test_presets_structure():
    """Ensure all presets have required keys."""
    for key, p in PRESETS.items():
        assert "name" in p
        assert "description" in p
        assert "use_gpu" in p
        assert "audio_params" in p


def test_lecture_mode_settings():
    """Verify Lecture Mode (Preset 1)."""
    p = PRESETS["1"]
    assert p["use_gpu"] is False
    assert "-tune" in p["video_params"]
    assert "animation" in p["video_params"]
    assert "64k" in p["audio_params"]


def test_hq_mode_settings():
    """Verify HQ Mode (Preset 2)."""
    p = PRESETS["2"]
    assert p["use_gpu"] is True
    assert "h264_nvenc" in p["gpu_quality_flags"]


def test_social_mode_settings():
    """Verify Social Media Mode (Preset 3)."""
    p = PRESETS["3"]
    # Must enforce 720p scaling
    assert any("720" in x for x in p["video_params"])
    # Must use VBR capping
    assert any("-maxrate" in x for x in p["gpu_quality_flags"]["h264_nvenc"])


def test_archive_mode_settings():
    """Verify Archive Mode (Preset 5)."""
    p = PRESETS["5"]
    # Must use HEVC/H.265
    assert "hevc_nvenc" in p["gpu_quality_flags"]
    assert "libx265" in p["cpu_fallback"]
