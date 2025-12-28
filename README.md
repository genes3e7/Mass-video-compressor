# Mass Video Compressor (MVC)

**Turn gigabytes of raw footage into efficient, high-quality assets automatically.**

MVC is a "fire-and-forget" batch compressor tool designed for power users. Unlike standard converters, it doesn't just blindly encode files—it analyzes your hardware to pick the fastest engine and spins up the perfect number of parallel workers to saturate your system without crashing it.

## 🌟 Why use MVC?

* **🧠 Smart Hardware Switching:** Automatically detects if you have an **NVIDIA**, **AMD**, **Intel**, or **Apple** GPU. If hardware acceleration fails, it seamlessly falls back to CPU encoding.
* **⚡ Dynamic Parallelism:** Automatically calculates your CPU core count to determine the optimal number of simultaneous conversions.
* **🎛️ Specialized Presets:** Don't guess bitrate settings. Use pre-tuned profiles for Lectures, Archival, or Social Media.
* **📂 Drag & Drop Workflow:** No complex arguments. Just drag your source folder into the window.

---

## ⏱️ Presets & Performance Guide

*Note: "Time per 100MB" estimates are based on a standard 1080p input file. Your actual speed depends heavily on your specific CPU/GPU.*

### 1. Lecture Mode (Slides + Voice)
**"The Space Saver"**
* **Use Case:** University lectures, Zoom recordings, Coding tutorials.
* **Strategy:** Uses advanced CPU algorithms to detect static slides. It freezes the image data for seconds at a time to save massive amounts of space.
* **Speed Rating:** 🐢 **Slow** (Heavy CPU usage)
* **Processing Time:** ~3 to 5 minutes per 100MB input.
* **Result:** Tiny files (~2MB/min) with crystal clear text.

### 2. High Quality (HQ) Mode
**"The Daily Driver"**
* **Use Case:** Action cams, Family memories, Movies, Music.
* **Strategy:** Blasts through files using your GPU's hardware encoder. Keeps visual quality near-lossless while retaining stereo audio.
* **Speed Rating:** 🐇 **Fast** (GPU Accelerated)
* **Processing Time:** ~30 seconds per 100MB input.
* **Result:** Great quality (~20MB/min) processed rapidly.

### 3. Social Media (720p Limit)
**"The Shareable Clip"**
* **Use Case:** WhatsApp, Discord, Slack, Email attachments.
* **Strategy:** Downscales to 720p and strictly caps the bitrate to ensure files don't hit "File Too Large" errors.
* **Speed Rating:** 🐎 **Very Fast**
* **Processing Time:** ~45 seconds per 100MB input.
* **Result:** Guaranteed small files ready for upload.

### 4. Editing Proxy
**"The Editor's Friend"**
* **Use Case:** Video editing in Premiere/DaVinci on slow laptops.
* **Strategy:** Creates a low-quality, "buttery smooth" version of your footage specifically for scrubbing through timelines without lag.
* **Speed Rating:** ⚡ **Instant** (Ultrafast)
* **Processing Time:** < 10 seconds per 100MB input.
* **Result:** Large but extremely fast-to-decode files.

### 5. Archive Master (HEVC No-Compromise)
**"The Digital Vault"**
* **Use Case:** NAS Backups, 4K Masters, Precious Memories.
* **Strategy:** Uses the modern H.265 codec at **maximum quality** settings (`veryslow` / `p7`). It targets "Visually Lossless" fidelity (`QP 16`) with high-bitrate audio.
* **Speed Rating:** 🐢 **Slow**
* **Processing Time:** ~2 to 4 minutes per 100MB input.
* **Result:** Perfect visual preservation. File size may be large (20-40MB/min) but efficient for the quality.

---

## 📦 Installation & Usage

**Prerequisites:** Python 3.10 - 3.14

It is highly recommended to run this tool in a **Virtual Environment (venv)** to keep dependencies clean.

### 1. Set up the Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Tool
```bash
python main.py
```
*Follow the on-screen prompts to select a preset and drag-and-drop your folders.*

---

## 🔨 Building for Distribution

Want to give this tool to a friend who doesn't have Python? You can compile it into a standalone `.exe` file.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the Build Script:**
    ```bash
    python build.py
    ```

3.  **Locate the App:**
    Check the newly created `dist/` folder for your executable.

---

## 🛠️ Development

To run the test suite (ensures hardware detection and presets are valid):

```bash
pytest tests/
```
