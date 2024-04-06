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
