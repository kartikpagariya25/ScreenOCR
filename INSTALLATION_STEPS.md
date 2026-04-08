# 📥 Complete Installation & Usage Guide

## 🎯 Quick Start (5 Minutes)

### Prerequisites
1. **Windows 10/11** ✅
2. **Python 3.11-3.13** - Download from [python.org](https://www.python.org/downloads/)
3. **Tesseract OCR** - Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

---

## 🚀 Installation Methods

### Method 1: One-Click Setup (Recommended) ⭐

**Run this single command:**
```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

**What it does:**
- ✅ Checks Python & Tesseract
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Registers Windows startup
- ✅ Starts ScreenOCR automatically

**Done!** Press `Shift+Q+W+E` to use.

---

### Method 2: Manual Setup

#### Step 1: Install Tesseract OCR

1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (keep default options)
3. Add to PATH:
   ```powershell
   setx TESSERACT_CMD "C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```
4. **Restart your terminal**

#### Step 2: Clone/Download ScreenOCR

```powershell
# If using Git:
git clone https://github.com/YOUR_USERNAME/ScreenOCR.git
cd ScreenOCR

# OR download ZIP and extract to F:\ScreenOCR
```

#### Step 3: Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

#### Step 5: Run ScreenOCR

```powershell
python screen_ocr.py
```

---

## 🎮 How to Use

### Basic Workflow

```
1. Start ScreenOCR
   ↓
2. Press Shift+Q+W+E
   ↓
3. Select text area
   ↓
4. Text copied!
   ↓
5. Paste with Ctrl+V
```

### Detailed Steps

#### 1. Start ScreenOCR

**Option A - Run once:**
```powershell
python screen_ocr.py
```

**Option B - Install as utility:**
```powershell
powershell -ExecutionPolicy Bypass -File .\install_utility_windows.ps1
```

**Option C - Use batch file:**
```
Double-click: start.bat
```

#### 2. Activate OCR

Press **Shift + Q + W + E** together

**What happens:**
- Dark semi-transparent overlay appears
- Cursor changes to crosshair (+)
- You can still see screen content

#### 3. Select Text

- **Click** where text starts
- **Drag** to create rectangle around text
- **Release** mouse button

**Tips:**
- Select tightly around text
- Include some padding
- Avoid selecting too much background

#### 4. Wait for Processing

- Small notification appears: "Text copied"
- Takes 1-3 seconds typically
- Text is now in clipboard

#### 5. Paste Text

Press **Ctrl + V** anywhere to paste

---

## ⚙️ Configuration

### Change Hotkey

Edit `screen_ocr.py` line 38:

```python
# Current hotkey: Shift+Q+W+E
self._hotkey_required = {"shift", "q", "w", "e"}

# Change to Ctrl+Alt+S:
self._hotkey_required = {"ctrl", "alt", "s"}

# Or Ctrl+Shift+C:
self._hotkey_required = {"ctrl", "shift", "c"}
```

**Restart ScreenOCR** after changing.

### Change OCR Language

Edit `screen_ocr.py` line 23:

```python
# Default: English
OCR_LANG = "eng"

# Hindi:
OCR_LANG = "hin"

# French:
OCR_LANG = "fra"

# Spanish:
OCR_LANG = "spa"
```

**Download languages:** https://github.com/tesseract-ocr/tessdata

### Adjust Overlay Transparency

Edit `screen_ocr.py` line 147:

```python
# Current: 55% brightness (0.55)
dimmed = ImageEnhance.Brightness(screenshot).enhance(0.55)

# More transparent (brighter):
dimmed = ImageEnhance.Brightness(screenshot).enhance(0.75)

# Less transparent (darker):
dimmed = ImageEnhance.Brightness(screenshot).enhance(0.35)
```

---

## 🛑 Stop & Restart

### Stop ScreenOCR

Press **Esc** key anytime

### Restart After Stopping

```powershell
.\.venv\Scripts\pythonw.exe screen_ocr.py
```

### Check If Running

```powershell
Get-Process pythonw -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'screen_ocr.py' }
```

---

## 📦 Build Standalone EXE

### Why Build EXE?

- ✅ No Python installation needed
- ✅ Share with others easily
- ✅ Looks like professional software
- ✅ Smaller download size

### Build Steps

1. **Run build script:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\build_exe.ps1
   ```

2. **Wait for completion** (1-2 minutes)

3. **Find EXE:**
   ```
   F:\ScreenOCR\dist\ScreenOCR.exe
   ```

4. **Test it:**
   ```
   Double-click ScreenOCR.exe
   ```

### Distribute EXE

**Option 1 - Share directly:**
- Send `ScreenOCR.exe` to friends/colleagues
- They need Tesseract installed

**Option 2 - Bundle Tesseract:**
- Create folder with EXE + Tesseract
- Include installation instructions

---

## 🔄 Auto-Start on Windows Login

### Already Configured!

If you ran `setup.ps1` or `install_utility_windows.ps1`, it's already set to auto-start.

### Verify Auto-Start

```powershell
Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" | Select-Object -ExpandProperty ScreenOCR
```

Should show:
```
"F:\ScreenOCR\.venv\Scripts\pythonw.exe" "F:\ScreenOCR\screen_ocr.py"
```

### Remove Auto-Start

```powershell
python register_startup_windows.py remove
```

### Add Auto-Start (if removed)

```powershell
python register_startup_windows.py
```

---

## 🐛 Troubleshooting

### Problem: Hotkey doesn't work

**Solution 1 - Check if running:**
```powershell
Get-Process pythonw -ErrorAction SilentlyContinue
```

**Solution 2 - Restart:**
```powershell
.\.venv\Scripts\pythonw.exe screen_ocr.py
```

**Solution 3 - Check conflicts:**
- Close other apps that might use same hotkey
- Try different hotkey combination

---

### Problem: "Tesseract not found"

**Solution:**
```powershell
# Set environment variable
setx TESSERACT_CMD "C:\Program Files\Tesseract-OCR\tesseract.exe"

# Restart terminal
# Run again:
python screen_ocr.py
```

---

### Problem: No text detected

**Causes:**
- Text too small
- Low contrast
- Blurry image
- Selection too large

**Solutions:**
1. Select larger text area
2. Ensure good contrast
3. Use clearer/higher resolution content
4. Try with different content first

---

### Problem: Overlay doesn't appear

**Solutions:**
1. Check ScreenOCR is running (no errors)
2. Try on desktop (not fullscreen app)
3. Restart ScreenOCR
4. Check Windows permissions

---

### Problem: Low OCR accuracy

**Improve results:**
- Select text tightly
- Use high-contrast content
- Avoid blurry/low-res sources
- Ensure text is horizontal
- Try with printed text first (not handwriting)

---

## 📊 Performance Tips

### For Best OCR Accuracy

1. **High Resolution** - Use 1080p or higher displays
2. **Clear Text** - Printed fonts work best
3. **Good Contrast** - Dark text on light background
4. **Horizontal Text** - Avoid rotated text
5. **Minimal Background** - Select tightly around text

### For Faster Processing

1. **Smaller Selection** - Less area = faster OCR
2. **Simple Text** - Plain fonts faster than decorative
3. **Single Language** - Don't mix languages

---

## 🎓 Learning More

### Understand the Code

Read these files:
- `screen_ocr.py` - Main application logic
- `implementation.md` - Technical architecture
- `QUICKSTART.md` - Quick reference

### Modify & Extend

**Easy modifications:**
- Change hotkey (line 38)
- Change language (line 23)
- Adjust overlay (line 147)
- Change indicator position (line 270)

**Advanced modifications:**
- Add new preprocessing profiles
- Integrate translation API
- Add OCR history
- Create settings GUI

---

## 📞 Get Help

### Documentation

- 📖 `README.md` - Main documentation
- 🚀 `QUICKSTART.md` - Quick reference
- 🔧 `implementation.md` - Technical details
- 📤 `GITHUB_GUIDE.md` - Publishing guide

### Check Logs

If running in terminal, watch for error messages.

### Common Error Messages

**"Import could not be resolved"**
```powershell
# Fix: Install dependencies
pip install -r requirements.txt
```

**"Tesseract is not installed"**
```powershell
# Fix: Install Tesseract and set path
setx TESSERACT_CMD "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

**"Port already in use"**
```powershell
# Fix: Kill existing instance
Get-Process pythonw | Stop-Process -Force
```

---

## ✅ Installation Checklist

Before using ScreenOCR:

- [ ] Python 3.11-3.13 installed
- [ ] Tesseract OCR installed
- [ ] Tesseract in PATH or TESSERACT_CMD set
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] ScreenOCR runs without errors
- [ ] Hotkey triggers overlay
- [ ] Text extraction works
- [ ] Clipboard copy works
- [ ] Auto-start configured (optional)

---

## 🎉 You're Ready!

Everything is set up. Now:

1. **Restart your laptop** to test auto-start
2. **Press Shift+Q+W+E** after login
3. **Extract text** from any video/image
4. **Enjoy!** 🚀

---

<div align="center">

**Having issues? Check [README.md](README.md) troubleshooting section.**

**Want to contribute? See [GITHUB_GUIDE.md](GITHUB_GUIDE.md)**

</div>
