# 🖥️ ScreenOCR - Copy Text from Any Screen Region

[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue)]()
[![Python](https://img.shields.io/badge/Python-3.11%2B-green)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()
[![OCR](https://img.shields.io/badge/Engine-Tesseract%20v5-orange)]()

**Extract text from anywhere on your screen - videos, images, PDFs, apps - with a single hotkey!**

![Demo](https://img.shields.io/badge/Hotkey-Shift%2BQ%2BW%2BE-red)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## 🎯 What is ScreenOCR?

ScreenOCR is a **lightweight Windows utility** that lets you copy text from any visible screen region using OCR (Optical Character Recognition). Perfect for:

- 📺 **Videos** - Extract subtitles, captions, or any text from YouTube, VLC, Netflix
- 🖼️ **Images** - Copy text from memes, screenshots, photos
- 📄 **PDFs** - Grab text from protected or scanned documents
- 🌐 **Websites** - Copy text that's blocked or non-selectable
- 💻 **Applications** - Extract text from any desktop app UI

**No more manual typing!** Just press a hotkey, select the area, and text is copied to your clipboard.

---

## ✨ Key Features

### 🚀 Core Features
- ⌨️ **Global Hotkey** - `Shift + Q + W + E` works from any application
- 🎯 **Smart Selection** - Drag-to-select region with visual overlay
- 📋 **Auto-Copy** - Extracted text automatically copied to clipboard
- ⚡ **Fast OCR** - Multi-pass preprocessing for better accuracy
- 🎨 **Dark Overlay** - Semi-transparent selection layer (like Snipping Tool)
- 🛑 **Quick Exit** - Press `Esc` to stop the utility anytime

### 🔥 Advanced Features
- 📊 **Multi-Pass OCR** - 4 different preprocessing profiles for maximum accuracy
- 🎯 **Confidence Scoring** - Automatically selects best OCR result
- 🔤 **Punctuation Enhancement** - Special handling for `.`, `,`, `;`, `:`, `!?` 
- 📈 **Image Upscaling** - 2x-3x scaling for better small text recognition
- 🎚️ **Adaptive Threshold** - Works on low-contrast and blurry frames
- 💾 **Startup Auto-Load** - Runs automatically when you log into Windows

### 🛠️ Developer Features
- 🔧 **Easy Configuration** - Change hotkey, language, settings via code
- 📦 **EXE Build Support** - Package as standalone executable
- 🎨 **Customizable UI** - Modify overlay colors, indicator position
- 📝 **Extensible** - Add new OCR engines, languages, or features

---

## 📦 Installation

### Quick Install (Recommended)

**One-command setup:**
```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

This script will:
1. ✅ Check Python and Tesseract installation
2. ✅ Create virtual environment
3. ✅ Install all dependencies
4. ✅ Verify imports
5. ✅ Register Windows startup
6. ✅ Start ScreenOCR automatically

---

### Manual Install

#### Step 1: Install Prerequisites

**Python 3.11-3.13** (Download from [python.org](https://www.python.org/downloads/))

**Tesseract OCR** (Required for text extraction):
```powershell
# Download and install from:
https://github.com/UB-Mannheim/tesseract/wiki

# After install, verify:
tesseract --version

# If not in PATH, set environment variable:
setx TESSERACT_CMD "C:\Program Files\Tesseract-OCR\tesseract.exe"
# Then restart your terminal
```

#### Step 2: Clone or Download
```powershell
git clone https://github.com/YOUR_USERNAME/ScreenOCR.git
cd ScreenOCR
```

#### Step 3: Setup Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Step 4: Run ScreenOCR
```powershell
python screen_ocr.py
```

---

## 🎮 Usage

### Basic Usage

1. **Start ScreenOCR** (if not already running):
   ```powershell
   python screen_ocr.py
   # or
   .\.venv\Scripts\pythonw.exe screen_ocr.py
   ```

2. **Activate OCR**:
   - Press `Shift + Q + W + E` together
   - Dark overlay appears with crosshair cursor

3. **Select Text Area**:
   - Click and drag to draw rectangle around text
   - Release mouse button

4. **Paste Text**:
   - Small notification shows "Text copied"
   - Text is in clipboard
   - Press `Ctrl + V` to paste anywhere

### Stop ScreenOCR

Press `Esc` key anytime to stop the utility.

### Restart After Stopping

```powershell
.\.venv\Scripts\pythonw.exe screen_ocr.py
```

---

## ⚙️ Advanced Configuration

### Run as Background Utility

**Install to startup** (runs automatically on Windows login):
```powershell
powershell -ExecutionPolicy Bypass -File .\install_utility_windows.ps1
```

**Remove from startup**:
```powershell
python register_startup_windows.py remove
```

### Build Standalone EXE

Create a standalone executable (no Python installation needed):

```powershell
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1
```

**Register EXE for startup**:
```powershell
powershell -ExecutionPolicy Bypass -File .\register_startup_exe_windows.ps1
```

**Remove EXE from startup**:
```powershell
powershell -ExecutionPolicy Bypass -File .\register_startup_exe_windows.ps1 -Remove
```

### Customize Hotkey

Edit `screen_ocr.py` line 38:
```python
self._hotkey_required = {"shift", "q", "w", "e"}
# Change to: {"ctrl", "alt", "s"} for Ctrl+Alt+S
```

### Change OCR Language

Edit `screen_ocr.py` line 23:
```python
OCR_LANG = "eng"  # Change to "hin" for Hindi, "fra" for French, etc.
```

Download additional languages from Tesseract: https://github.com/tesseract-ocr/tessdata

---

## 🔍 How It Works

### Architecture Overview

```
┌─────────────────┐
│  Global Hotkey  │ ← Shift+Q+W+E
│   Listener      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Screen Capture │ ← Full screenshot
│      (mss)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Region Select  │ ← Drag overlay
│     (Tkinter)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preprocessing  │ ← OpenCV enhancement
│    (4 passes)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OCR Engine     │ ← Tesseract
│  (Multi-pass)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Clipboard Copy │ ← pyperclip
│  + Indicator    │
└─────────────────┘
```

### OCR Pipeline

1. **Upscale** - 2x-3x scaling for better detail
2. **Grayscale** - Convert to single channel
3. **Denoise** - Bilateral filter removes noise
4. **Enhance** - Multiple profiles:
   - Adaptive threshold (Gaussian)
   - CLAHE + Otsu threshold
   - Sharpened version
5. **OCR Pass** - Run Tesseract on each profile
6. **Score & Select** - Pick best result using confidence + punctuation score
7. **Normalize** - Clean up line breaks and spacing

---

## 📁 Project Structure

```
ScreenOCR/
├── screen_ocr.py              # Main application
├── setup.ps1                  # One-click setup script ⭐
├── install_utility_windows.ps1 # Install as background utility
├── start.bat                  # Quick start batch file
├── build_exe.ps1              # Build standalone EXE
├── register_startup_windows.py # Windows startup registration
├── register_startup_exe_windows.ps1 # EXE startup registration
├── add_to_task_scheduler.ps1  # Task Scheduler registration
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── QUICKSTART.md              # Quick reference guide
├── implementation.md          # Technical implementation details
├── LICENSE                    # MIT License
└── .gitignore                 # Git ignore rules
```

---

## 🛠️ Dependencies

### Python Packages
```txt
mss>=10.1.0              # Screen capture
numpy>=1.26.0            # Numerical operations
opencv-python>=4.10.0    # Image preprocessing
Pillow>=11.2.1           # Image processing
pynput>=1.7.7            # Keyboard listener
pyperclip>=1.9.0         # Clipboard access
pytesseract>=0.3.13      # Tesseract OCR wrapper
```

### System Requirements
- **OS**: Windows 10/11
- **Python**: 3.11, 3.12, or 3.13
- **Tesseract**: v5.0+
- **RAM**: 512MB+ available
- **Screen**: Any resolution

---

## 🎯 Use Cases

### 📺 Video Subtitles
Watching a YouTube video with useful information? Extract subtitles instantly!

### 🖼️ Image Text
Got a meme or screenshot with text? Copy it without retyping.

### 📄 Scanned PDFs
Working with scanned documents? Extract text for editing.

### 🌐 Protected Web Content
Website blocking text selection? ScreenOCR bypasses it.

### 💻 Error Messages
Need to copy an error from a dialog box? Select and paste.

### 🎮 Game Text
Extract text from games where copy-paste doesn't work.

---

## 🔧 Troubleshooting

### Hotkey Not Working

**Check if ScreenOCR is running:**
```powershell
Get-Process pythonw -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'screen_ocr.py' }
```

**Restart manually:**
```powershell
.\.venv\Scripts\pythonw.exe screen_ocr.py
```

**Check for hotkey conflicts:**
- Make sure no other app is using `Shift+Q+W+E`
- Try pressing keys more deliberately (all together)

### No Text Detected

**Try these:**
- Select a larger area around the text
- Ensure text has good contrast (dark on light)
- Make sure text is clearly visible
- Try with higher resolution content

### Tesseract Not Found

**Fix PATH issue:**
```powershell
# Set environment variable
setx TESSERACT_CMD "C:\Program Files\Tesseract-OCR\tesseract.exe"

# Restart terminal and run:
python screen_ocr.py
```

### Overlay Not Appearing

**Check:**
- ScreenOCR is running (no errors in terminal)
- No fullscreen app blocking overlays
- Try on desktop first to verify it works

### Low OCR Accuracy

**Improve results:**
- Select text area tightly (minimize background)
- Use high-contrast, clear text
- Avoid blurry or low-resolution content
- Ensure text is horizontal (not rotated)

---

## 🚀 Performance

- **Startup Time**: < 1 second
- **Hotkey Response**: < 100ms
- **OCR Processing**: 1-3 seconds (depends on region size)
- **Memory Usage**: ~50-100MB
- **CPU Usage**: < 5% (idle), ~30% (during OCR)

---

## 📝 Roadmap

### Completed ✅
- [x] Global hotkey listener
- [x] Dark overlay selection
- [x] Multi-pass OCR preprocessing
- [x] Confidence-based result selection
- [x] Punctuation enhancement
- [x] Auto-copy to clipboard
- [x] Windows startup registration
- [x] EXE build support
- [x] Esc to stop functionality

### Planned 🔜
- [ ] System tray icon with menu
- [ ] Configurable hotkey via settings file
- [ ] Multiple OCR language support
- [ ] OCR history (last 20 captures)
- [ ] Direct translation integration
- [ ] Image preprocessing presets
- [ ] Custom overlay colors
- [ ] Multi-monitor support improvements

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Areas for Contribution
- 🌍 Additional OCR language support
- 🎨 Better image preprocessing algorithms
- 🖥️ System tray integration
- 📜 OCR history and search
- 🔧 Configuration UI
- 📦 Installer package (MSI/InnoSetup)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**What this means:**
- ✅ Free to use for personal and commercial projects
- ✅ Modify and distribute as you like
- ✅ No warranty provided
- ⚠️ Include original license in distributions

---

## 🙏 Acknowledgments

- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)** - Powerful OCR engine
- **[UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)** - Windows builds
- **[pynput](https://github.com/moses-palmer/pynput)** - Keyboard/mouse control
- **[mss](https://github.com/BoboTiG/python-mss)** - Fast screen capture
- **[OpenCV](https://opencv.org/)** - Image processing library

---

## 📞 Support

### Found a Bug?
Open an issue on [GitHub Issues](https://github.com/YOUR_USERNAME/ScreenOCR/issues)

### Need Help?
- Check [QUICKSTART.md](QUICKSTART.md) for quick reference
- Read [implementation.md](implementation.md) for technical details
- Review troubleshooting section above

### Feature Requests?
Submit your ideas on [GitHub Issues](https://github.com/YOUR_USERNAME/ScreenOCR/issues)

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Frepos%2FYOUR_USERNAME%2FScreenOCR&query=%24.stargazers_count&label=Stars&color=yellow)
![GitHub forks](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Frepos%2FYOUR_USERNAME%2FScreenOCR&query=%24.forks_count&label=Forks&color=blue)
![GitHub issues](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Frepos%2FYOUR_USERNAME%2FScreenOCR&query=%24.open_issues_count&label=Issues&color=red)

---

## 🎓 Learning Resources

Want to understand how this works? Check out:
- [Tesseract Documentation](https://tesseract-ocr.github.io/)
- [OpenCV Python Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- [pynput Documentation](https://pynput.readthedocs.io/)
- [Python Tkinter Guide](https://realpython.com/python-gui-tkinter/)

---

<div align="center">

**Made with ❤️ for easier text extraction**

If you find this useful, please ⭐ star this repository!

</div>
