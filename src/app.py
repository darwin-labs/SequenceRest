# Copyright (c) 2024 Darwin and Timon Harz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from SearchService import SearchService
import socket
from queue import Queue
from dotenv import load_dotenv
import threading
import socketio
from credentials import APIKeyLoader
from celery import Celery

app = Flask(__name__)

#Initialize a queue to store UDP data
upd_data_queue = Queue()

def udp_server(host='0.0.0.0', port=5005):
    MAX_BUFFER_SIZE = 1024
    
    sock = socket.socket(socket.AF_INET, sock.SOCK_DGRAM)
    sock.bind((host, port))
    
    print(f'Listening to UDP data on {host}: {port}')
    
    while True:
        data, addr = sock.recvform(MAX_BUFFER_SIZE)
        print(f'Received message: {data} from {addr}')
        udp_data_queue.put(data)

@app.route('/')
def index(): 
	return "Darwin Restful API"

@app.route('/api/', methods=['GET'])
def query_request():
    search_service = SearchService()
    query = request.args.get('query')
    print(f"Query: {query}")
    num_of_sources = request.args.get('num')
    print(f"Number of sources: {num_of_sources}")
    model = request.args.get('model')
    print(f"Requested model: {model}")
    
    completion = search_service.handle_request(query=query, num_results=3)
    
    print(completion)
    return json.dumps({
        'query': query,
        'num_of_results': num_of_sources,
        'completion': completion
    })
    
@app.route('/api/stream/, methods=['GET']')
def udp_stream():
    if not upd_data_queue.empty():
        data = udp_data_queue.get()
        return "Not available"
    else:
        return "Not available"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
    