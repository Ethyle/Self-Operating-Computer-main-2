# utils.py
import pyautogui
import time
from pynput.mouse import Button, Controller
from config import CURRENT_OS

mouse = Controller()

def perform_click(x, y):
    """Performs a click at specific coordinates."""
    try:
        pyautogui.click(x, y)
        print(f"Click performed at coordinates: ({x}, {y})")
        time.sleep(1)  # Wait for the action to be taken into account
    except Exception as e:
        print(f"Error clicking: {e}")

def perform_double_click(x, y):
    """Performs a double click at specific coordinates with an optional interval."""
    try:
        # Move to the precise coordinates first
        mouse.position = (x, y)
        
        # Perform two consecutive left clicks with a small delay
        mouse.click(Button.left, 1)
        time.sleep(0.1)  # Short delay between clicks
        mouse.click(Button.left, 1)
        print(f"Double click performed at coordinates: ({x}, {y})")
    except Exception as e:
        print(f"Error double clicking: {e}")

def perform_right_click(x, y):
    """Performs a right click at specific coordinates."""
    try:
        pyautogui.rightClick(x, y)
        print(f"Right click performed at coordinates: ({x}, {y})")
    except Exception as e:
        print(f"Error right clicking: {e}")

def perform_drag_and_drop(start_x, start_y, end_x, end_y):
    """Performs a drag-and-drop."""
    try:
        pyautogui.moveTo(start_x, start_y)
        pyautogui.dragTo(end_x, end_y, duration=2, button='left')
        print(f"Drag and drop performed from ({start_x}, {start_y}) to ({end_x}, {end_y})")
    except Exception as e:
        print(f"Error drag-and-dropping: {e}")

def write_text(text):
    """Types text at the current location."""
    try:
        pyautogui.write(text, interval=0.05)  # Types text with an interval between characters
        print(f"Text written: '{text}'")
    except Exception as e:
        print(f"Error writing text: {e}")

def perform_copy():
    """Performs a shortcut to copy (CTRL+C or Command+C)."""
    try:
        if CURRENT_OS in ["windows", "linux"]:  
            pyautogui.hotkey('ctrl', 'c')
        elif CURRENT_OS == "darwin":  # MacOS
            pyautogui.hotkey('command', 'c')
        print("Copy action performed (CTRL+C or Command+C).")
    except Exception as e:
        print(f"Error performing 'copy': {e}")

def perform_paste():
    """Performs a shortcut to paste (CTRL+V or Command+V)."""
    try:
        if CURRENT_OS in ["windows", "linux"]:  
            pyautogui.hotkey('ctrl', 'v')
        elif CURRENT_OS == "darwin":  # MacOS
            pyautogui.hotkey('command', 'v')
        print("Paste action performed (CTRL+V or Command+V).")
    except Exception as e:
        print(f"Error performing 'paste': {e}")

def perform_undo():
    """Performs a shortcut to undo (CTRL+Z or Command+Z)."""
    try:
        if CURRENT_OS in ["windows", "linux"]:  
            pyautogui.hotkey('ctrl', 'z')
        elif CURRENT_OS == "darwin":  # MacOS
            pyautogui.hotkey('command', 'z')
        print("Undo action performed (CTRL+Z or Command+Z).")
    except Exception as e:
        print(f"Error performing 'undo': {e}")

def perform_cut():
    """Performs a shortcut to cut (CTRL+X or Command+X)."""
    try:
        if CURRENT_OS in ["windows", "linux"]:  
            pyautogui.hotkey('ctrl', 'x')
        elif CURRENT_OS == "darwin":  # MacOS
            pyautogui.hotkey('command', 'x')
        print("Cut action performed (CTRL+X or Command+X).")
    except Exception as e:
        print(f"Error performing 'cut': {e}")

def perform_select_all():
    """Performs a shortcut to select all (CTRL+A)."""
    try:
        if CURRENT_OS in ["windows", "linux"]:  
            pyautogui.hotkey('ctrl', 'a')
        elif CURRENT_OS == "darwin":  # MacOS
            pyautogui.hotkey('command', 'a')
        print("'Select all' action performed (CTRL+A or Command+A).")
    except Exception as e:
        print(f"Error selecting all text: {e}")

def perform_enter():
    """Performs a shortcut to enter text (Enter)."""
    try:
        pyautogui.press('enter')
        print("Enter action performed (ENTER).")
    except Exception as e:
        print(f"Error performing 'enter': {e}")

def perform_rename_file():
    """Performs a shortcut to rename a file (F2 for Windows/Linux, Enter for MacOS)."""
    try:
        if CURRENT_OS in ["windows", "linux"]:
            pyautogui.press('f2')  # Press F2 to rename
        elif CURRENT_OS == "darwin":  # MacOS
            pyautogui.press('enter')  # Press Enter to rename
        print("Rename action performed (F2 on Windows/Linux or Enter on MacOS).")
    except Exception as e:
        print(f"Error performing rename action: {e}")

def normalize_coordinates(x, y, image_w, image_h):
    """
    De-normalizes normalized coordinates (0-100) by adjusting them to the actual dimensions of the screen.
    """
    # Apply ratio to transform coordinates according to the size of the image
    x_adjusted = (x / 100.0) * image_w
    y_adjusted = (y / 100.0) * image_h
    return x_adjusted, y_adjusted
