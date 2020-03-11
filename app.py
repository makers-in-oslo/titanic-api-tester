from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import json
import requests
import os


app = Flask(__name__)

## Get connection details for APIs
titanic_staging_app_url = os.environ["TITANIC_STAGING_URL"]  # change to your app name
titanic_prod_app_url = os.environ["TITANIC_PROD_URL"]  # change to your app name


@app.route("/", methods=["POST", "GET"])
def index():

    # sample data
    data_sample = {
        "pclass": 1,
        "sex": "female",
        "age": 4.0,
        "sibsp": 1,
        "parch": 0,
        "fare": 7.25,
        "embarked": "S",
        "name": "Dr. D",
        "ticket": "Some 1234",
        "cabin": "KingPing",
        "passengerid": 123,
    }

    return render_template("index.html", data=data_sample)


@app.route("/production/", methods=["GET", "POST"])
def production_api():
    if request.method == "POST":

        headers = {"Content-Type": "application/json"}

        # sample data
        data = {
            "pclass": 1,
            "sex": "female",
            "age": 4.0,
            "sibsp": 1,
            "parch": 0,
            "fare": 7.25,
            "embarked": "S",
            "name": "Dr. D",
            "ticket": "Some 1234",
            "cabin": "KingPing",
            "passengerid": 123,
        }

        data_to_api = json.dumps(data)

        send_request_deployed = requests.request(
            "POST", titanic_prod_app_url, headers=headers, data=data_to_api
        )
        print(send_request_deployed)
        api_response = str(send_request_deployed.json())
        # print(len(api_response))
        print("API response")
        print(send_request_deployed.json())

        return render_template(
            "production.html",
            api_status=send_request_deployed,
            api_response=api_response,
            data=data,
        )


@app.route("/staging/", methods=["GET", "POST"])
def staging_api():
    if request.method == "POST":

        headers = {"Content-Type": "application/json"}

        # sample data
        data = {
            "pclass": 1,
            "sex": "female",
            "age": 4.0,
            "sibsp": 1,
            "parch": 0,
            "fare": 7.25,
            "embarked": "S",
            "name": "Dr. D",
            "ticket": "Some 1234",
            "cabin": "KingPing",
            "passengerid": 123,
        }

        data_to_api = json.dumps(data)

        send_request_deployed = requests.request(
            "POST", titanic_staging_app_url, headers=headers, data=data_to_api
        )
        print(send_request_deployed)
        api_response = str(send_request_deployed.json())
        # print(len(api_response))
        print("API response")
        print(send_request_deployed.json())

        return render_template(
            "staging.html",
            api_status=send_request_deployed,
            api_response=api_response,
            data=data,
        )


@app.route("/feature_engineering/")
def feature_engineering():
    print("Hei")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
