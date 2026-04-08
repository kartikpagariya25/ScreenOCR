qwe# ScreenOCR Utility Implementation Plan

## Goal
Build a stable laptop utility that runs in the background, activates by global hotkey (`Shift+Q+W+E`), allows drag-select of any visible region, and copies OCR text reliably with better punctuation capture.

## Current Status
- Implemented: transparent selection layer (no dark dim screen)
- Implemented: compact status indicator only (no full text popup)
- Implemented: multi-pass OCR preprocessing for better punctuation and low-quality video frames
- Implemented: EXE build script and startup registration script

## Architecture
1. Hotkey listener
- Global keyboard listener (`pynput`) waits for all required keys.
- Prevents repeated triggers while keys are still held.

2. Capture and region selection
- Full virtual screen capture via `mss` before selector starts.
- Transparent fullscreen selector receives drag events.
- Only a rectangle border is drawn; no dim background overlay.

3. OCR pipeline (accuracy-focused)
- Input crop is upscaled to improve small punctuation readability.
- Multiple preprocessing profiles are generated:
  - Adaptive threshold profile
  - CLAHE + Otsu profile
  - Soft sharpen profile
- OCR runs on each profile with confidence scoring.
- Best result is selected using confidence + punctuation-weighted score.

4. Result handling
- Extracted text is copied directly to clipboard (`pyperclip`).
- Minimal top-right indicator shows status (`Text copied`, `No text detected`, or error).

## Why punctuation improves
- Tiny punctuation marks are often lost in low-resolution frames.
- Upscaling + profile diversity recovers edge detail.
- Multi-pass scoring avoids relying on one aggressive threshold style.

## Utility Mode On Laptop
You have two operational modes.

1. Python utility mode
- Run app with virtualenv Python.
- Add startup with existing startup script.
- Good for development and quick changes.

2. EXE utility mode (recommended)
- Build a standalone executable with PyInstaller.
- Register executable in Windows startup.
- No need to open terminal each time.

## Build and install (EXE)
1. Create venv with Python 3.11/3.12/3.13.
2. Install dependencies and build:

```powershell
.\build_exe.ps1
```

3. Register EXE at startup:

```powershell
.\register_startup_exe_windows.ps1
```

4. Optional removal from startup:

```powershell
.\register_startup_exe_windows.ps1 -Remove
```

## Validation Checklist
- Hotkey triggers selector while video is playing.
- No dark overlay appears during selection.
- Small indicator appears after OCR and disappears quickly.
- Clipboard receives extracted text.
- Punctuation (`.`, `,`, `;`, `:`) is captured on typical subtitle/UI text.
- EXE starts on login and hotkey works without terminal.

## Future Upgrades
- Config file for hotkey and OCR language.
- Tray icon for Pause/Resume/Exit.
- Optional history of recent OCR captures.
- Optional second OCR engine fallback for hard scenes.
