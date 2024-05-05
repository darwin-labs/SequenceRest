import json
from flask import Flask, request, jsonify



app = Flask(__name__)

@app.route('/')
def index(): 
	return "Hello Darwin Restful API"

@app.route('/api/', methods=['GET'])
def query_request():
    
    query = request.args.get('query')
    num_of_sources = request.args.get('num')
    print(query)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
    