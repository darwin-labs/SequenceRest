import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import SearchService

app = Flask(__name__)

@app.route('/')
def index(): 
	return "Hello Darwin Restful API"

@app.route('/api/', methods=['GET'])
def query_request():
    search_service = SearchService()
    query = request.args.get('query')
    print(f"Query: {query}")
    num_of_sources = request.args.get('num')
    print(f"Number of sources: {num_of_sources}")
    model = request.args.get('model')
    print(f"Requested model: {model}")
    
    completion = search_service.handle_request(query=query, num_of_sources=num_of_sources, model=model)
    
    
    
    print(completion)
    return f"Completion: {completion}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
    