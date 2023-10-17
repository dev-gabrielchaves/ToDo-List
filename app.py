from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__, template_folder='templates')

client = MongoClient('mongodb://localhost:27017')
database = client.tododatabase
collection = database.todos

@app.route('/')
def home():
    documents = collection.find()
    return render_template('home.html', documents= documents)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        title =  request.form['title']
        description = request.form['description']
        collection.insert_one({'Title':title, 'Description':description, 'Status': 'Undone'})
        return redirect('/')

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        return render_template('update.html', id= id)
    elif request.method == 'POST':
        title =  request.form['title']
        description = request.form['description']
        collection.update_one({'_id': ObjectId(str(id))}, {'$set': {'Title': title, 'Description': description}})
        return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    collection.delete_one({'_id': ObjectId(str(id))})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)