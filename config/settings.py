import os

import imageio_ffmpeg

# Auto-detect the ffmpeg binary location
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# ==========================================
# AUTO-DETECT WORKER COUNT
# ==========================================
# Logic:
# 1. Get total logical CPU cores (threads).
# 2. Divide by 4.
#    (Since we enforce '-threads 4' in presets, 1 worker effectively consumes 4 logical cores).
# 3. Cap at 5.
#    (Consumer NVIDIA GPUs often limit concurrent encoding sessions to 5).
# 4. Ensure at least 1 worker.


def _get_optimal_workers():
    try:
        # Returns number of logical CPUs (threads)
        cores = os.cpu_count()
        if not cores:
            return 2  # Fallback

        # Calculate optimal workers (1 worker per 4 logical cores)
        workers = int(cores / 4)

        # Clamp between 1 and 5
        # (Upper limit protects against GPU session limits and excessive context switching)
        return max(1, min(workers, 5))

    except Exception:
        return 2


DEFAULT_WORKERS = _get_optimal_workers()
