# main.py
import time
from screenshot_manager import take_screenshot
from ai_interaction import supervise_task
from action_handler import interpret_json_action
from ai_interpretation import interpret_user_request

def main(task_description):
    """Main function handeling the process."""

    # Step 1: Interpret the user query
    final_result, repeat_action, number_iterations = interpret_user_request(task_description)
    
    if not final_result or not repeat_action or not number_iterations:
        print("Failed to interpret user request.")
        return
    
    print(f"Final Result : {final_result}")
    print(f"Repeat Action : {repeat_action}")
    print(f"Number of Iterations : {number_iterations}")
    
    i = 0  # Initialising the iteration counter
    
    while i < number_iterations:
        print(f"\n--- Iteration {i+1} of {number_iterations} ---")
        
        # Screenshot and determination of specific action
        screenshot_path, image_w, image_h = take_screenshot()
        if not screenshot_path:
            print("Unable to continue without a screenshot.")
            return

        # Set action based on `repeat_action` and current state (via screenshot)
        assistant_reply = supervise_task(repeat_action, screenshot_path)

        # Interpret and execute the specified action
        task_completed = interpret_json_action(assistant_reply, screenshot_path, image_w, image_h)
        
        # Check if task has been completed
        if task_completed:
            print(f"Action for '{repeat_action}' completed successfully.")
            i += 1  # Increment the counter if the action is successful
        else:
            print(f"Action for '{repeat_action}' not completed. Try again...")
            # You could add some retry logic for the action here if needed
            
        time.sleep(2)  # Pause to avoid system overload
    
    # Final verification of the result
    print("\n--- Final Result Check ---")
    screenshot_path, image_w, image_h = take_screenshot()
    assistant_reply = supervise_task(number_iterations, screenshot_path)
    verification = interpret_json_action(assistant_reply, screenshot_path, image_w, image_h)
    
    if verification:
        print("The end result matches the desired result.")
    else:
        print("The end result does not match the desired result.")
    
    print("Task fully completed.")
