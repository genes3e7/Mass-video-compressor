import subprocess

from config.settings import FFMPEG_EXE


def check_encoder(encoder_name):
    """
    Tests if a specific encoder is available by trying to encode 1 second of black video.
    """
    try:
        cmd = [
            FFMPEG_EXE,
            "-y",
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=1280x720:r=30",
            "-c:v",
            encoder_name,
            "-t",
            "1",
            "-f",
            "null",
            "-",
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def detect_gpu_codec():
    """
    Returns the best available GPU codec name, or None if no GPU found.
    """
    # Priority Order
    if check_encoder("h264_nvenc"):
        return "h264_nvenc"  # NVIDIA
    if check_encoder("h264_amf"):
        return "h264_amf"  # AMD
    if check_encoder("h264_qsv"):
        return "h264_qsv"  # Intel QuickSync
    if check_encoder("h264_videotoolbox"):
        return "h264_videotoolbox"  # Mac

    return None
