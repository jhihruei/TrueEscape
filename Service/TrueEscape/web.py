#-*- coding: UTF-8 -*- 
from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson.json_util import dumps
import json
import insert
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/latest")
def latest():
	mc = MongoClient()
	articleCol = mc.escapedb.articles
	articles = dumps(articleCol.find({},{"_id":0}).sort("_id",-1).limit(10))
	articles = json.loads(articles)
	mc.close()
	return render_template('latest.html',articleList=articles)

@app.route("/studio")
def studio():
	mc = MongoClient()
	studioCol = mc.escapedb.studios
	studio = dumps(studioCol.find({},{"_id":0}).sort("_id",-1))
	studio = json.loads(studio)
	mc.close()
	return render_template('studio.html',studioInfo=studio)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'GET' :
		return render_template('login.html')
	elif request.method == 'POST':
		form = dumps(request.form)
		return form
	return redirect(url_for('index')) 

@app.route("/newpost", methods=['GET', 'POST'])
def newpost():
	if request.method == 'GET':
		return render_template('newpost.html')
	elif request.method == 'POST':
		form = dumps(request.form)
		form = insert.insertPost(form)
		return form
	
@app.route("/article/<article_id>")
def article(article_id):
	mc = MongoClient()
	articleCol = mc.escapedb.articles
	article = dumps(articleCol.find_one({"id":article_id},{"_id":0}))
	article = json.loads(article)
	mc.close()
	return render_template('article.html',article=article)

@app.route("/user/<name>")
def user(name):
	return render_template('user.html',name=name)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

if __name__ == "__main__":
	app.debug=True
	app.run(host='0.0.0.0')

