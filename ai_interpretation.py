# ai_interpretation.py
import re
import json
from config import CLIENT
from screenshot_manager import image_to_data_uri

def interpret_user_request(task_description):
    """
    Uses AI to interpret the user query and define the ideal outcome, the major action to loop and the number of iterations.
    """
    prompt = f"""
    You are an expert in interpreting user queries for computer manipulations. You interpret user queries and define the ideal result as well as the general action to repeat to achieve it. 
    For example, if the user wants to rename 60 pdfs to customer names from excel files, the end result will be: copy the excel customer name and paste it by renaming the corresponding pdf. 
    User query : {task_description}
    
    Reply in JSON with the following keys:
        - "final_result": Text description of the desired result.
        - "repat_action": General action to repeat.
        - "number_iterations": Number of times to execute the action loop.
    
    Example response :
    {{
        "final_result": "The 10 desktop photos have been dragged into the NamePhotos folder",
        "repeat_action": [Drag and drop a desktop photo into the NamePhotos folder],
        "number_iterations": 10
    }}
    """

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Interprets the request and provides the necessary information."}
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
        
        raw_response = response.choices[0].message.content.strip()
        cleaned_response = re.sub(r"^```json|```$", "", raw_response, flags=re.MULTILINE).strip()
        data = json.loads(cleaned_response)
        return data['final_result'], data['repeat_action'], data['number_iterations']
    except Exception as e:
        print(f"Error interpreting user request : {e}")
        return None, None, None
