# ScreenOCR - Quick Start Guide

## ✅ Installation Complete

Your ScreenOCR utility is now installed and running in the background.

---

## 🎯 How to Use

### Step 1: Activate OCR
Press **Shift + Q + W + E** together

### Step 2: Select Text Area
- Your cursor will change to crosshair
- Click and drag to select the text area
- Release mouse button

### Step 3: Text Copied!
- A small notification appears: "Text copied"
- Text is now in your clipboard
- Paste it anywhere with Ctrl+V

---

## 🛑 Stop the Utility

Press **Esc** key anytime to stop the hotkey utility.

---

## 🔄 Restart After Stopping

If you pressed Esc or want to restart manually:

```powershell
.\.venv\Scripts\pythonw.exe screen_ocr.py
```

---

## ⚙️ Auto-Start on Windows Login

The utility is already registered to start automatically when you log in to Windows.

To remove from startup:
```powershell
python register_startup_windows.py remove
```

---

## 📝 What Works

- ✅ Any video playing (YouTube, VLC, etc.)
- ✅ Images (photos, screenshots, memes)
- ✅ PDFs and documents
- ✅ Applications with non-selectable text
- ✅ Websites with protected text

---

## 🔧 Troubleshooting

### Hotkey not working?
1. Make sure ScreenOCR is running:
   ```powershell
   .\.venv\Scripts\pythonw.exe screen_ocr.py
   ```
2. Check if another app is using the same hotkey
3. Try pressing keys more deliberately (all together)

### No text detected?
- Select a larger area
- Ensure text is clear and visible
- Try with high-contrast text (dark on light background)

### Utility stopped?
- Press Esc to stop intentionally
- Restart with command above
- Or run setup again: `powershell -ExecutionPolicy Bypass -File .\setup.ps1`

---

## 📁 Project Files

- `screen_ocr.py` - Main application
- `setup.ps1` - One-click setup script
- `install_utility_windows.ps1` - Install and start utility
- `build_exe.ps1` - Build standalone .exe (optional)
- `requirements.txt` - Python dependencies

---

## 🚀 Next Steps

1. Test it now on any video or image
2. Press Shift+Q+W+E and select some text
3. Paste with Ctrl+V to verify it works

---

**Enjoy your Screen OCR utility!** 🎉
