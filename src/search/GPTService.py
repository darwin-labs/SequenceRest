import requests 


class GPTService():


    def getResponse(self, content, role):
        api_key = "lo-kud2TUZah6y5zdqTo6cSx3AE9QGn526hxktpn4A9zvT3mwwr"
        url = "https://api.llmos.dev/v1/chat/completions"

        headers = {
         "Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json"
    }
        payload = self._getPayload(content, role)

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

    def _getPayload(content, role="Assistant", name="GPTService"):
        model = "mistral-7b-instruct"
        payload = {
            "model": model,
        "messages": [
            {
            "content": content,
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
        "frequency_penalty": "<string>",
        "false": 0
    }
        print(f"payload: {payload}")
        return payload
    


service = GPTService()

service.getResponse("Hello World", "Assistant")    

   






