# screenshot_manager.py
import pyautogui
import base64
import os
from PIL import Image
import time

def take_screenshot(screenshot_path="screenshot.png"):
    """Takes a screenshot and saves it."""
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        print(f"Screenshot taken and saved at: {screenshot_path}")
        image_w, image_h = pyautogui.size()
        print(f"Image dimensions: {image_w}x{image_h}")
        return screenshot_path, image_w, image_h
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None, None, None

def image_to_data_uri(image_path):
    """Converts a local image to Data URI."""
    try:
        print("[DEBUG] Converting image to Data URI...")
        mime_type = "image/png"  # Adjust according to image type (png, jpg, etc.)
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            data_uri = f"data:{mime_type};base64,{base64_image}"
            print("[DEBUG] Conversion successful.")
            return data_uri
    except Exception as e:
        print(f"Error converting image to Data URI: {e}")
        return None
