from app import app
from flask import Flask, current_app, jsonify, flash, render_template, json, request, redirect, session, url_for
import pyrebase
import pandas as pd
import ast
import json

config = {
    "apiKey": "AIzaSyBVojd4HVQdliJRPH2FjinEZF4YUlRSxwI",
    "authDomain": "kaggledashboard-1556d.firebaseapp.com",
    "databaseURL": "https://kaggledashboard-1556d.firebaseio.com",
    "projectId": "kaggledashboard-1556d",
    "storageBucket": "kaggledashboard-1556d.appspot.com",
    "serviceAccount": "app/kaggledashboard-1556d-firebase-adminsdk-brhoj-e4d59e3d2d.json",
    "messagingSenderId": "33015475582"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/')
def main():
    return "Hello world"

@app.route('/getData', methods=['GET'])
def getData():
    db_response = db.child("athlete_events").get().val()
    df = pd.DataFrame(db_response)
    converted_json = df.to_json(orient="index")
    response_result = json.loads(converted_json)
    return response_result

@app.route('/getDataSorted', methods=['GET', 'POST'])
def getDataSorted():
    sortCol = ast.literal_eval(request.args.get("sortCol"))
    sortType = ast.literal_eval(request.args.get("ascending"))
    print(sortCol, sortType)
    db_response = db.child("athlete_events").get().val()
    df = pd.DataFrame(db_response)
    df.sort_values(by=sortCol, ascending=sortType, inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns=["index"], inplace=True)
    converted_json = df.to_json(orient="index")
    response_result = json.loads(converted_json)
    return response_result

@app.route('/getDataFiltered', methods=['GET', 'POST'])
def getDataFiltered():
    filterCol = request.args.get("filterCol")
    colType = "number"
    startVal = request.args.get("startVal")
    endVal = request.args.get("endVal")
    print(filterCol, colType, startVal, endVal)
    db_response = db.child("athlete_events").get().val()
    df = pd.DataFrame(db_response)
    df = df[df[filterCol]!="NA"]
    df.drop_duplicates(inplace=True)
    if colType == "number":
        df[filterCol] = pd.to_numeric(df[filterCol])
        df = df[(df[filterCol] >= int(startVal)) & (df[filterCol] <= int(endVal))]
        df.sort_values(by=filterCol, inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns=["index"], inplace=True)
    converted_json = df.to_json(orient="index")
    response_result = json.loads(converted_json)
    return response_result