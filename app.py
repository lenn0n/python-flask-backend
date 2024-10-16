from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

import pandas as pd
import replicate

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def home():
  return "Python Flask API for Story Generation Page and Main Time in PH"

# Libs: PANDAS, CSV
@app.route('/api/v1/retrieve-time', methods=['POST', 'OPTIONS', 'HEAD'])
@cross_origin()
def retrieve_time():
  data = request.json
  area = data.get('area')

  df = pd.read_csv('data.csv')
  x = []
  y = []

  for rt in df['RUN_TIME']:
    x.insert(len(x), rt)

  for ar in df[area]:
    y.insert(len(y), ar)
  
  return { "data": { "x": x, "y": y} }


@app.route('/api/v1/stream', methods=['OPTIONS', 'HEAD', 'GET'])
@cross_origin()
def stream():
  def generate():
    for i in range(100):  # Adjust the number or content as per your logic
      yield f'Data chunk {i}\n'
  return Response(generate(), content_type='text/plain')

# Libs: REPLICATE
@app.route('/api/v1/generate-story', methods=['POST', 'OPTIONS', 'HEAD'])
@cross_origin()
def generate_story():
  data = request.json
  query = data.get('query')

  input_data = {
    'prompt': query,
    'max_tokens': 514,
    'min_tokens': 10,
  }

  def stream_response():
    for event in replicate.stream(
      "meta/meta-llama-3-8b",
      input=input_data,
    ):
      yield str(event)

  return Response(stream_response(), content_type='text/plain')

if __name__ == '__main__':
  app.run(debug=False)
