import json
import re

def extract_json_from_string(s):
    # Regular expression pattern to find JSON content
    pattern = r'\{.*?\}'

    # Find all matches of JSON content in the string
    json_matches = re.findall(pattern, s)

    # Parse each JSON object and store them in a list
    json_objects = []
    for match in json_matches:
        try:
            json_objects.append(json.loads(match))
        except ValueError:
            # JSON content might be malformed, ignore and continue
            pass

    return json_objects

def get_model_response(json_data):
    try:
        data = json.loads(json_data)
        if 'choices' in data and len(data['choices']) > 0:
            return data['choices'][0]['message']['content']
        else:
            return "No response found"
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None