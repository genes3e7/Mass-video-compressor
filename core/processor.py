import subprocess

from tqdm import tqdm

from config.settings import FFMPEG_EXE


def build_command(input_path, output_path, preset, gpu_codec=None):
    """
    Constructs the FFMPEG command based on the preset and detected hardware.
    """
    cmd = [FFMPEG_EXE, "-y", "-v", "error", "-i", input_path]

    # VIDEO SECTION
    if preset["use_gpu"] and gpu_codec:
        cmd.extend(["-c:v", gpu_codec])
        cmd.extend(preset["gpu_quality_flags"].get(gpu_codec, []))
    else:
        # CPU Mode (Fallback or intentional)
        params = preset.get("video_params", preset.get("cpu_fallback", []))
        cmd.extend(params)

    # AUDIO SECTION
    cmd.extend(preset["audio_params"])

    # OUTPUT
    cmd.append(output_path)

    return cmd


def process_file(args):
    """
    Worker function to run the compression.
    """
    input_path, output_path, filename, preset, gpu_codec = args

    tqdm.write(f"▶ STARTING: {filename}")

    cmd = build_command(input_path, output_path, preset, gpu_codec)

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        tqdm.write(f"✔ COMPLETED: {filename}")
        return True
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.decode().strip() if e.stderr else "Unknown Error"
        tqdm.write(f"✘ FAILED: {filename} -> {err_msg}")
        return False
