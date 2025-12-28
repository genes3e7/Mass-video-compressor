"""
Configuration settings for the Mass Video Compressor.

Handles:
- FFmpeg binary detection via imageio-ffmpeg.
- Automatic worker thread calculation based on CPU core count.
"""

import os

import imageio_ffmpeg

# Auto-detect the ffmpeg binary location
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()


def _get_optimal_workers():
    """
    Calculate the optimal number of concurrent worker processes.

    Logic:
    1. Get total logical CPU cores.
    2. Divide by 4.
       Note: We force '-threads 4' in presets to limit encoder threads.
       However, this is an approximation for scaling, as demuxing, filtering,
       and muxing spawn additional threads (often 8-12 total OS threads per worker).
       It does not represent a hard guarantee of core usage.
    3. Clamp between 1 and 5 to respect GPU encoding session limits and reduce overhead.

    Returns:
        int: The number of workers to use (1-5).
    """
    try:
        # Returns number of logical CPUs (threads)
        cores = os.cpu_count()
        if not cores:
            return 2  # Fallback

        # Calculate optimal workers (1 worker per ~4 logical cores)
        workers = cores // 4

        # Clamp between 1 and 5
        return max(1, min(workers, 5))

    except Exception:
        return 2


DEFAULT_WORKERS = _get_optimal_workers()
