import json
import os

class APIKey_Loader:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.api_keys = self._load_api_keys()
        print(f'All api keys: {self.api_keys}')
        self.set_all_keys(self.api_keys)
    
    def _load_api_keys(self):
        if not os.path.exists(self.file_path):
            raise APIKeysFileNotExistent

        with open(self.file_path, 'r') as file:
            data  = json.load(file)
            return data.get('api_keys', {})

    def get_api_key(self, service_name):
        """
        Retrieve an API key for the specified service.
        
        Args:
            service_name (str): The name of the service (e.g., 'together_ai').
        
        Returns:
            str: The API key value if found, None otherwise.
        """
        return self.api_keys.get(service_name)
    
    def get_all_keys(self):
        """
        Get all existing api keys
        """
        return self.api_keys
    
    def set_all_keys(self, keys):
        for key in keys:
            os.environ[key] = keys[key]
            
    
class APIKeysFileNotExistent(Exception):
     error_log = 'API Key could not be fetched. JSON file which holds them is non existent'       
     

if __name__ == '__main__':
    service = APIKey_Loader(file_path='api_keys.json')
    