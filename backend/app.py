import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
    'SQLALCHEMY_TRACK_MODIFICATIONS'
)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, description):
        self.title = title
        self.description = description


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@ app.route('/articles', methods=["GET"])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)


@ app.route('/articles', methods=["POST"])
def add_article():
    title = request.json['title']
    description = request.json['description']

    articles = Articles(title, description)
    db.session.add(articles)
    db.session.commit()

    return article_schema.jsonify(articles)
