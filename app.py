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


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/prediction/', methods=['GET', 'POST'])
def dataprediction():
    if request.method == 'POST':
        age_content = request.form['age']
        new_age_id = Todo(content=age_content)
        print(age_content)
        try:
            db.session.add(new_age_id)
            db.session.commit()
            #return redirect('/')
        except:
            return 'There was an issue adding your task'

        # sample data
        data = {'Pclass': 3
              , 'Age': age_content
              , 'SibSp': 1
              , 'Fare': 50}

        data_to_api = json.dumps(data)

        try:
            send_request_deployed = requests.post(dataprep_api_url, data_to_api)
            print(send_request_deployed)
            api_response = send_request_deployed.json()
            print(send_request_deployed.json())

            ages = Todo.query.order_by(Todo.date_created).all()
            return render_template('prediction.html', tasks=ages, data=data, api_status=send_request_deployed, api_response=api_response)
        except:
            return 'There was a problem accessing the prediction API'

    else:
        ages = Todo.query.order_by(Todo.date_created).all()
        return render_template('prediction.html', tasks=ages, data=data)

@app.route('/feature_engineering/')
def feature_engineering():
    print('Hei')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
