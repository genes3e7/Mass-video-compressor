"""
Defines the compression profiles.
"""

PRESETS = {
    "1": {
        "name": "Lecture Mode (Slides + Voice)",
        "description": "High CPU compression, readable text, clear mono voice.",
        "use_gpu": False,
        "video_params": [
            "-threads",
            "4",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-tune",
            "animation",
            "-crf",
            "26",
            "-g",
            "300",
            "-pix_fmt",
            "yuv420p",
        ],
        "audio_params": ["-c:a", "aac", "-b:a", "64k", "-ac", "1"],
    },
    "2": {
        "name": "High Quality / Music",
        "description": "GPU accelerated, near lossless video, low-mid audio.",
        "use_gpu": True,
        "gpu_quality_flags": {
            "h264_nvenc": ["-rc", "constqp", "-qp", "20", "-preset", "p7"],
            "h264_amf": [
                "-usage",
                "transcoding",
                "-quality",
                "quality",
                "-rc",
                "cqp",
                "-qp_i",
                "20",
                "-qp_p",
                "20",
                "-qp_b",
                "20",
            ],
            "h264_qsv": ["-preset", "veryslow", "-global_quality", "20"],
            "h264_videotoolbox": ["-q", "80"],
        },
        "cpu_fallback": [
            "-threads",
            "4",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
        ],
        "audio_params": ["-c:a", "aac", "-b:a", "128k", "-ac", "2"],
    },
    "3": {
        "name": "Social Media (720p limit)",
        "description": "Downscales to 720p with bitrate caps. Fits most chat app limits.",
        "use_gpu": True,
        "gpu_quality_flags": {
            # NVIDIA: Enforce max bitrate of 1Mbps
            "h264_nvenc": ["-rc", "vbr", "-b:v", "1M", "-maxrate", "1.5M", "-bufsize", "2M"],
            # AMD
            "h264_amf": [
                "-usage",
                "transcoding",
                "-rc",
                "vbr_peak",
                "-b:v",
                "1M",
                "-maxrate",
                "1.5M",
            ],
        },
        "cpu_fallback": [
            "-threads",
            "4",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "28",
        ],
        "video_params": [
            # Common filter to scale height to 720, keep aspect ratio
            "-vf",
            "scale=-2:720",
        ],
        "audio_params": ["-c:a", "aac", "-b:a", "128k", "-ac", "2"],
    },
    "4": {
        "name": "Editing Proxy (Ultrafast)",
        "description": "Low quality, high speed. Optimized for smooth timeline scrubbing.",
        "use_gpu": True,
        "gpu_quality_flags": {
            # NVIDIA: Ultrafast preset, very frequent keyframes
            "h264_nvenc": ["-preset", "p1", "-g", "15"],
        },
        "cpu_fallback": [
            "-threads",
            "4",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-tune",
            "fastdecode",
            "-g",
            "15",
        ],
        "video_params": [
            "-vf",
            "scale=-2:720",  # 720p is standard for proxies
        ],
        "audio_params": [
            "-c:a",
            "pcm_s16le",  # Uncompressed audio (fastest to process)
        ],
    },
    "5": {
        "name": "Archive Master (No Compromises)",
        "description": "H.265/HEVC at max quality. Visually lossless preservation.",
        "use_gpu": True,
        "gpu_quality_flags": {
            # NVIDIA: p7 is the absolute slowest/best preset. QP 16 is near-lossless.
            "hevc_nvenc": ["-rc", "constqp", "-qp", "16", "-preset", "p7", "-tier", "high"],
            # AMD
            "hevc_amf": [
                "-usage",
                "transcoding",
                "-quality",
                "quality",
                "-rc",
                "cqp",
                "-qp_i",
                "16",
                "-qp_p",
                "16",
                "-tier",
                "high",
            ],
            # Intel
            "hevc_qsv": ["-preset", "veryslow", "-global_quality", "16"],
            # Mac
            "hevc_videotoolbox": ["-q", "90"],
        },
        "cpu_fallback": [
            "-threads",
            "4",
            "-c:v",
            "libx265",
            "-preset",
            "veryslow",  # Takes forever, but maximum compression efficiency
            "-crf",
            "16",  # Visually Lossless
        ],
        "audio_params": ["-c:a", "aac", "-b:a", "320k", "-ac", "2"],
    },
}
