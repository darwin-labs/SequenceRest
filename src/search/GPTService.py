import requests 


class GPTService:

    
    def getResponse(self):
        api_key = "lo-kud2TUZah6y5zdqTo6cSx3AE9QGn526hxktpn4A9zvT3mwwr"
        url = "https://api.llmos.dev/v1/chat/completions"

        headers = {
         "Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json"
    }
        payload = self._getPayload("Test", "Assistant")

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

    def _getPayload(self, content, role="Assistant", name="GPTService"):
        print(f"content is: {content} \nrole is: {role} \nname: {name}")
        model = "mistral-7b-instruct"
        payload = {
            "model": model,
        "messages": [
            {
            "content": "Hello World!",
            "role": role,
            "name": name
            }
        ],
        "max_tokens": 5000,
        "stream": True,
        "temperture": 1,
        "top_p": 0,
        "presence_penalty": 0,
        "logit_bias": {},
        "frequency_penalty": 1,
        "false": 0
    }
        print(f"payload: {payload}")
        return payload
    


service = GPTService()
service.getResponse()  

   






