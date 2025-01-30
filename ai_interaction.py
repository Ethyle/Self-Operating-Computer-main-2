# ai_interaction.py
import re
import json
import replicate
from config import CLIENT, CURRENT_OS
from screenshot_manager import image_to_data_uri
from utils import normalize_coordinates

def locate_element(description, screenshot_path, image_w, image_h, retries=3):
    """Locates an element on the screen using Replicate and returns its coordinates."""
    print(f"[DEBUG] Locating element: {description}")
    image_data_uri = image_to_data_uri(screenshot_path)
    description = "You are an expert in Location, you only answer with coordinates. Give me ONLY the x and y coordinates of the exact center of " + description

    if not image_data_uri:
        print("Unable to convert image to Data URI.")
        return None, None

    for attempt in range(retries):
        try:
            print("[DEBUG] Calling Replicate to locate the element...")
            output = replicate.run(
                "zsxkib/molmo-7b:76ebd700864218a4ca97ac1ccff068be7222272859f9ea2ae1dd4ac073fa8de8",
                input={
                    "text": description,
                    "image": image_data_uri,
                    "top_k": 50,
                    "top_p": 1,
                    "temperature": 1,
                    "length_penalty": 1,
                    "max_new_tokens": 200
                }
            ) 
            timeout=120  # Increase the waiting time if the API allows
            print(f"Molmo AI Response: {output}")

            # Extract coordinates from response
            match = re.findall(r'\b\d+\.\d+\b', output)

            if len(match) >= 2:
                x = float(match[0])  # First number found
                y = float(match[1])  # Second number found

                x, y = normalize_coordinates(x, y, image_w, image_h)

                print(f"Element '{description}' located at coordinates: ({x}, {y})")
                return x, y
        except Exception as e:
            print(f"Error locating coordinates, attempt {attempt + 1}/{retries}): {e}")
    return None, None

def supervise_task(task_description, screenshot_path):
    """Interacts with OpenAI to determine the next action."""
    image_data_uri = image_to_data_uri(screenshot_path)
    if not image_data_uri:
        return "Error converting image."

    prompt = f"""You are an expert in digital tasks. You assist a user in their tasks on a computer. Your job is to provide the next action needed to accomplish the given task using the context of the current screen.

Task given: {task_description}

Current screen provided as a screenshot.
To help you in your reasoning, here are some contexte about computer usage : 
Computers operate through a combination of hardware interfaces (mouse, keyboard, touchpad, etc.) and software interfaces (operating systems and applications). 
The primary methods of interaction involve clicking, typing, dragging, and using shortcuts. 
Applications on a computer can be accessed either from a desktop (requiring a double click) or a taskbar (requiring a single click). 
Many tasks require users to understand the context of the screen and the application's state. 
For example, text can be selected for copying using the mouse (click and drag) or by using the keyboard (to select all). 
Renaming files requires selecting the file first (clicking once), then using either a shortcut or context menu to rename it. 
Navigating browsers involves typing in a search bar, pressing Enter, and clicking on relevant links. 
Icons and buttons are often interactive and can trigger actions with clicks. 
If the task involves repetitive steps, actions must be repeated methodically for the number of required iterations. 
Additionally, certain apps (e.g., text editors, web browsers) allow immediate typing without selecting a text field. 
Keyboard shortcuts and mouse gestures can simplify navigation and execution. 
Understanding these interaction patterns and screen layouts is crucial for executing any computer-based task.
Respond only using JSON format to perform the actions:

To enter text:
   {{ "type": "type", "content": "<text to enter>" }}
To perform shortcuts (possible actions: "copy", "paste", "undo", "cut", "select_all", "enter", "rename_file"):
   {{ "type": "shortcut", "action": "<action>" }}
To click the mouse:
   {{ "type": "mouse_click", "description": "<element to locate name of the icon, or location, or if photo: describe it>" }}
To double click:
   {{ "type": "double_click", "description": "<element to locate name of the icon, or location, or if photo: describe it>" }}
To right-click:
   {{ "type": "right_click", "description": "<element to locate name of the icon, or location, or if photo: describe it>" }}
To drag-and-drop:
   {{ "type": "drag_and_drop", "from": "<starting point to locate name of the icon, or location, or if photo: describe it>", "to": "<endpoint to locate name of the icon, or location, or if photo: describe it> " }}
To indicate the task is complete:
   {{ "type": "task_done" }}

IMPORTANT:
- Provide only a JSON response.
- If you need to click an element, make sure to use the correct description of that element.
- Do not provide additional instructions or explanatory text, only JSON.

"""

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user",  "content": [
                {
                    "type": "text",
                    "text": f"Here is the step you are on the screen in your task accomplishement:"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_data_uri
                    }
                }
            ]
        }          
    ]

    try:
        response = CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=900,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        print(response)

        # Clean response by removing ```json tags and ``` at the end
        raw_response = response.choices[0].message.content.strip()
        cleaned_response = re.sub(r"^```json|```$", "", raw_response, flags=re.MULTILINE).strip()
        return cleaned_response
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return "Error calling OpenAI."
