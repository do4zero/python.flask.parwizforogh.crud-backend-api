import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
    'SQLALCHEMY_TRACK_MODIFICATIONS'
)
db = SQLAlchemy(app)
ma = Marshmallow(app)
cors = CORS(app)

# Article Model
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    image = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, description, image):
        self.title = title
        self.description = description
        self.image = image

# Article Schema for format response
class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'image', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


# Article list data endpoint
@ app.route('/articles', methods=["GET"])
def get_articles():
    all_articles = Articles.query.order_by(Articles.date.desc()).all()
    results = articles_schema.dump(all_articles)
    return jsonify({"data": results})


# Article single data endpoint
@ app.route('/articles/<id>/', methods=["GET"])
def post_details(id):
    article = Articles.query.get(id)
    return {"data":article_schema.dump(article)}


# Article create data endpoint
@ app.route('/articles', methods=["POST"])
def add_article():
    title = request.json['title']
    description = request.json['excerpt']
    image = request.json['image']

    articles = Articles(title, description, image)
    db.session.add(articles) 
    db.session.commit()

    return jsonify({"data":article_schema.dump(articles)})


# Article update data endpoint
@ app.route('/articles/<id>/', methods=["PUT"])
def update_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    description = request.json['excerpt']
    image = request.json['image']

    article.title = title
    article.description = description
    article.image = image

    db.session.commit()

    return {"data":article_schema.dump(article)}


# Article delete data endpoint
@ app.route('/articles/<id>/', methods=["DELETE"])
def delete_article(id):
    article = Articles.query.get(id)

    db.session.delete(article)
    db.session.commit()

    return {"data":article_schema.dump(article)}
