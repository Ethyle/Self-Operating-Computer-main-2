# action_handler.py
import json
import re
from ai_interaction import locate_element
from utils import (
    perform_click,
    perform_double_click,
    perform_right_click,
    perform_drag_and_drop,
    write_text,
    perform_copy,
    perform_paste,
    perform_undo,
    perform_cut,
    perform_select_all,
    perform_enter,
    perform_rename_file
)

last_action = None  # To keep track of the last executed action

def interpret_json_action(assistant_reply, screenshot_path, image_w, image_h):
    """Interprets the JSON response and triggers the appropriate actions."""
    try:
        # Clean the response by removing the json tags
        cleaned_reply = re.sub(r"^json\s*|\s*$", "", assistant_reply, flags=re.MULTILINE).strip()

        # Try to load the cleaned response as JSON
        action = json.loads(cleaned_reply)

        # If the action is a list, iterate over each action
        if isinstance(action, list):
            for act in action:
                if not handle_action(act, screenshot_path, image_w, image_h):
                    return False  # If an action was not fully executed, the task continues
            return True  # All actions in the list were executed
        else:
            # If the action is a single object, handle it directly
            return handle_action(action, screenshot_path, image_w, image_h)

    except json.JSONDecodeError:
        print(f"Error interpreting JSON: {assistant_reply}")
        return False

def handle_action(action, screenshot_path, image_w, image_h):
    """Handles a single action extracted from JSON."""
    global last_action
    print(f"Action received: {action}")  # Added to verify the received action

    try:
        action_type = action.get("type")

        # Check if the action is the same as the previous one
        if action == last_action:
            print(f"Repeated action detected: {action}. Ignored.")
            return False

        last_action = action  # Update last action

        if action_type == "task_done":
            print("Task completed.")
            return True  # Task is complete

        if action_type == "type":
            print(f"Keyboard action: typing the text '{action['content']}'")
            write_text(action['content'])

        elif action_type == "shortcut":
            shortcut_action = action.get("action")
            print(f"Shortcut action: {shortcut_action}")
            if shortcut_action == "copy":
                perform_copy()
            elif shortcut_action == "paste":
                perform_paste()
            elif shortcut_action == "undo":
                perform_undo()
            elif shortcut_action == "cut":
                perform_cut()
            elif shortcut_action == "select_all":
                perform_select_all()  # Added handling for "select_all"
            elif shortcut_action == "enter":
                perform_enter()
            elif shortcut_action == "rename_file":
                perform_rename_file()

        elif action_type == "mouse_click":
            print(f"Mouse action: left click on '{action['description']}'")
            x, y = locate_element(action['description'], screenshot_path, image_w, image_h)
            if x is not None and y is not None:
                perform_click(x, y)
            else:
                print(f"Unable to locate element: '{action['description']}'.")

        elif action_type == "double_click":
            print(f"Mouse action: double click on '{action['description']}'")
            x, y = locate_element(action['description'], screenshot_path, image_w, image_h)
            if x is not None and y is not None:
                perform_click(x, y)
                perform_enter()
            else:
                print(f"Unable to locate element: '{action['description']}'.")

        elif action_type == "right_click":
            print(f"Mouse action: right click on '{action['description']}'")
            x, y = locate_element(action['description'], screenshot_path, image_w, image_h)
            if x is not None and y is not None:
                perform_right_click(x, y)
            else:
                print(f"Unable to locate element: '{action['description']}'.")

        elif action_type == "drag_and_drop":
            print(f"Mouse action: drag and drop from '{action['from']}' to '{action['to']}'")
            start_x, start_y = locate_element(action['from'], screenshot_path, image_w, image_h)
            end_x, end_y = locate_element(action['to'], screenshot_path, image_w, image_h)
            if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
                perform_drag_and_drop(start_x, start_y, end_x, end_y)
            else:
                print(f"Unable to locate one of the positions for drag and drop: from '{action['from']}' to '{action['to']}'.")

        return False  # Task is not complete
    except KeyError as e:
        print(f"Error in action: missing key {e}")
        return False
    except Exception as e:
        print(f"Error executing action: {e}")
        return False
