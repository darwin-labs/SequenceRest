import requests 
import json

#Data Models for decoding the response from the model
class ChatCompletion:
    def __init__(self, data):
        self.id = data['id']
        self.model = data['model']
        self.created = data['created']
        self.usage = data['usage']
        self.object = data['object']
        self.choices = [Choice(choice_data) for choice_data in data['choices']]

class Choice:
    def __init__(self, choice_data):
        self.index = choice_data['index']
        self.finish_reason = choice_data['finish_reason']
        self.message = Message(choice_data['message'])
        self.delta = Delta(choice_data['delta'])

class Message:
    def __init__(self, message_data):
        self.role = message_data['role']
        self.content = message_data['content']

class Delta:
    def __init__(self, delta_data):
        self.role = delta_data['role']
        self.content = delta_data['content']


#GPTService for handling any type requests
class GPTService:

    
    def getResponse(self):
        api_key = "lo-kud2TUZah6y5zdqTo6cSx3AE9QGn526hxktpn4A9zvT3mwwr"
        url = "https://api.llmos.dev/v1/chat/completions"

        headers = {
         "Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json"
    }
        payload = self._getPayload("Hello World!", "user")

        response = requests.request("POST", url, json=payload, headers=headers)

        json_string = response.text

        json_content = json.loads(json_string)
        
        return json_content
        

    def _getPayload(self, content, role="Assistant", name="GPTService"):
        print(f"content is: {content} \nrole is: {role} \nname: {name}")
        model = "mistral-7b-instruct"
        payload = {
            "model": model,
        "messages": [
            {
            "content": content,
            "role": role,
            "name": "GPTService - Sequence"
            }
        ],
        "max_tokens": 500,
        "stream": True,
        "temperture": 123,
        "top_p": 0,
        "presence_penalty": 0,
        "logit_bias": {}
    }
        print(f"payload: {payload}")
        return payload
    


service = GPTService()
json_content = service.getResponse()
chat_completion = ChatCompletion(json)
