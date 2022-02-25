from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return {}

@app.route("/ping")
def ping_demo():
  return {"statusCode":200,"status":"Connected","message":"Live!!!"}