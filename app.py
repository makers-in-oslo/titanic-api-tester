from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import json
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

## Get connection details for APIs
dataprep_api_url = os.environ['DATAPREP_API_URL'] # change to your app name
titanic_staging_app_url = os.environ['TITANIC_STAGING_URL'] # change to your app name
titanic_prod_app_url = os.environ['TITANIC_PROD_URL'] # change to your app name




class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/production/', methods=['GET', 'POST'])
def production_api():
    if request.method == 'POST':
        
        # sample data
        data = {'Pclass': 3
              , 'Age': 3
              , 'SibSp': 1
              , 'Fare': 50}

        data_to_api = json.dumps(data)

        #try:
        send_request_deployed = requests.post(titanic_prod_app_url, data_to_api)
        print(send_request_deployed)
        api_response = str(send_request_deployed.json())
        #print(len(api_response))
        print("API response")
        print(send_request_deployed.json())

        #ages = Todo.query.order_by(Todo.date_created).all()
        return render_template('production.html', api_status=send_request_deployed, api_response=api_response)
        #except:
        #    return 'There was a problem accessing the prediction API'


@app.route('/staging/', methods=['GET', 'POST'])
def staging_api():
    if request.method == 'POST':
        
        # sample data
        data = {'Pclass': 3
              , 'Age': 3
              , 'SibSp': 1
              , 'Fare': 50}

        data_to_api = json.dumps(data)

        #try:
        send_request_deployed = requests.post(titanic_staging_app_url)
        print(send_request_deployed)
        api_response = str(send_request_deployed.json())
        #print(len(api_response))
        print("API response")
        print(send_request_deployed.json())

        return render_template('staging.html', api_status=send_request_deployed, api_response=api_response)
        #except:
        #    return 'There was a problem accessing the prediction API'

    
@app.route('/feature_engineering/')
def feature_engineering():
    print('Hei')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
