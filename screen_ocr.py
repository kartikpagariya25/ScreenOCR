import os
import threading
import tkinter as tk
from dataclasses import dataclass
from typing import Optional

import cv2
import mss
import numpy as np
import pyperclip
import pytesseract
from PIL import Image, ImageEnhance, ImageTk
from pynput import keyboard


# Optional: set this env var if Tesseract is not on PATH.
# Example: setx TESSERACT_CMD "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
TESSERACT_CMD = os.environ.get("TESSERACT_CMD", "").strip()
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


OCR_LANG = "eng"
MIN_SELECTION_SIZE = 8
INDICATOR_TIMEOUT_MS = 1300


@dataclass(frozen=True)
class ScreenBounds:
    left: int
    top: int
    width: int
    height: int


class ScreenOCRApp:
    def __init__(self) -> None:
        self._hotkey_required = {"shift", "q", "w", "e"}
        self._pressed_keys: set[str] = set()
        self._triggered = False
        self._selection_lock = threading.Lock()
        self._listener: Optional[keyboard.Listener] = None
        self._is_stopping = False

    def run(self) -> None:
        print("Screen OCR is running.")
        print("Press Shift+Q+W+E to capture text from any visible region.")
        print("Press Esc to stop the hotkey utility.")
        print("Press Ctrl+C in this terminal to stop.")

        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as listener:
            self._listener = listener
            listener.join()

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        if key == keyboard.Key.esc:
            self._stop_hotkey_utility()
            return

        token = self._normalize_key(key)
        if token:
            self._pressed_keys.add(token)

        if self._hotkey_required.issubset(self._pressed_keys) and not self._triggered:
            self._triggered = True
            threading.Thread(target=self._start_selection_flow, daemon=True).start()

    def _on_release(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        if key == keyboard.Key.esc:
            return

        token = self._normalize_key(key)
        if token and token in self._pressed_keys:
            self._pressed_keys.discard(token)

        if not self._hotkey_required.issubset(self._pressed_keys):
            self._triggered = False

    def _stop_hotkey_utility(self) -> None:
        if self._is_stopping:
            return

        self._is_stopping = True
        self._pressed_keys.clear()
        self._triggered = False
        self._show_indicator("Hotkey utility stopped")

        if self._listener is not None:
            self._listener.stop()

    @staticmethod
    def _normalize_key(key: keyboard.Key | keyboard.KeyCode) -> Optional[str]:
        if key in {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r}:
            return "shift"

        if isinstance(key, keyboard.KeyCode) and key.char:
            return key.char.lower()

        return None

    def _start_selection_flow(self) -> None:
        # Prevent overlapping selectors if hotkey is hit repeatedly.
        if not self._selection_lock.acquire(blocking=False):
            return

        try:
            screenshot, bounds = self._capture_full_virtual_screen()
            region = self._select_region(screenshot, bounds)
            if not region:
                return

            cropped = screenshot.crop(region)
            text = self._extract_text(cropped)
            if text:
                pyperclip.copy(text)
                self._show_indicator("Text copied")
            else:
                self._show_indicator("No text detected")
        except Exception as exc:
            self._show_indicator(f"OCR error: {exc}")
        finally:
            self._selection_lock.release()

    @staticmethod
    def _capture_full_virtual_screen() -> tuple[Image.Image, ScreenBounds]:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            left = int(monitor["left"])
            top = int(monitor["top"])
            width = int(monitor["width"])
            height = int(monitor["height"])
            shot = sct.grab(monitor)

        image = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        return image, ScreenBounds(left=left, top=top, width=width, height=height)

    def _select_region(self, screenshot: Image.Image, bounds: ScreenBounds) -> Optional[tuple[int, int, int, int]]:
        region_holder: dict[str, Optional[tuple[int, int, int, int]]] = {"region": None}

        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.geometry(f"{bounds.width}x{bounds.height}+{bounds.left}+{bounds.top}")
        root.config(cursor="crosshair")

        dimmed = ImageEnhance.Brightness(screenshot).enhance(0.55)
        background = ImageTk.PhotoImage(dimmed)

        canvas = tk.Canvas(root, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, anchor="nw", image=background)

        start_x = 0
        start_y = 0
        rect_id: Optional[int] = None

        def on_press(event: tk.Event) -> None:
            nonlocal start_x, start_y, rect_id
            start_x, start_y = event.x, event.y
            rect_id = canvas.create_rectangle(
                start_x,
                start_y,
                start_x,
                start_y,
                outline="#00e0ff",
                width=2,
                dash=(5, 2),
            )

        def on_drag(event: tk.Event) -> None:
            if rect_id is not None:
                canvas.coords(rect_id, start_x, start_y, event.x, event.y)

        def on_release(event: tk.Event) -> None:
            x1 = min(start_x, event.x)
            y1 = min(start_y, event.y)
            x2 = max(start_x, event.x)
            y2 = max(start_y, event.y)

            if (x2 - x1) >= MIN_SELECTION_SIZE and (y2 - y1) >= MIN_SELECTION_SIZE:
                region_holder["region"] = (x1, y1, x2, y2)

            root.destroy()

        def on_cancel(_: tk.Event) -> None:
            root.destroy()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)
        root.bind("<Escape>", on_cancel)

        root.mainloop()

        return region_holder["region"]

    @staticmethod
    def _extract_text(cropped_image: Image.Image) -> str:
        bgr = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)
        profiles = ScreenOCRApp._build_ocr_profiles(bgr)

        best_text = ""
        best_score = -1.0

        for candidate, psm in profiles:
            text, confidence = ScreenOCRApp._ocr_with_confidence(candidate, psm)
            if not text:
                continue

            punctuation_count = sum(text.count(mark) for mark in ".,;:!?")
            score = confidence + min(10.0, punctuation_count * 0.75)

            if score > best_score:
                best_score = score
                best_text = text

        return ScreenOCRApp._normalize_text(best_text)

    @staticmethod
    def _build_ocr_profiles(bgr: np.ndarray) -> list[tuple[np.ndarray, int]]:
        scaled = cv2.resize(bgr, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)

        denoised = cv2.bilateralFilter(gray, 7, 50, 50)
        adaptive = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            7,
        )

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
        _, otsu = cv2.threshold(clahe, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        soft = cv2.GaussianBlur(gray, (0, 0), 1.0)
        sharpened = cv2.addWeighted(gray, 1.45, soft, -0.45, 0)

        return [
            (adaptive, 6),
            (otsu, 6),
            (sharpened, 6),
            (sharpened, 11),
        ]

    @staticmethod
    def _ocr_with_confidence(image: np.ndarray, psm: int) -> tuple[str, float]:
        config = f"--oem 3 --psm {psm}"
        data = pytesseract.image_to_data(
            image,
            lang=OCR_LANG,
            config=config,
            output_type=pytesseract.Output.DICT,
        )

        conf_values: list[float] = []
        for conf, token in zip(data.get("conf", []), data.get("text", [])):
            if not token or not token.strip():
                continue
            try:
                value = float(conf)
            except (TypeError, ValueError):
                continue
            if value >= 0:
                conf_values.append(value)

        confidence = (sum(conf_values) / len(conf_values)) if conf_values else 0.0
        text = pytesseract.image_to_string(image, lang=OCR_LANG, config=config).strip()
        return text, confidence

    @staticmethod
    def _normalize_text(text: str) -> str:
        if not text:
            return ""
        lines = [line.rstrip() for line in text.splitlines()]
        clean = [line for line in lines if line.strip()]
        return "\n".join(clean).strip()

    @staticmethod
    def _show_indicator(message: str) -> None:
        window = tk.Tk()
        window.overrideredirect(True)
        window.attributes("-topmost", True)
        window.attributes("-alpha", 0.95)

        screen_w = window.winfo_screenwidth()
        width = 280
        height = 54
        x = screen_w - width - 18
        y = 22
        window.geometry(f"{width}x{height}+{x}+{y}")
        window.configure(bg="#1f2a39")

        label = tk.Label(
            window,
            text=message,
            bg="#1f2a39",
            fg="#f5f7fa",
            font=("Segoe UI", 10, "bold"),
            anchor="center",
            padx=8,
        )
        label.pack(fill=tk.BOTH, expand=True)

        window.bind("<Button-1>", lambda _: window.destroy())
        window.after(INDICATOR_TIMEOUT_MS, window.destroy)
        window.mainloop()


def main() -> None:
    app = ScreenOCRApp()
    app.run()


if __name__ == "__main__":
    main()
