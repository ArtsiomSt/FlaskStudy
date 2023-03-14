import datetime
from flask import Flask, render_template, make_response, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_script import Manager
from flask_restful import Resource, Api, reqparse
from api.SimpleApi import apiapp
from serializer import Serializer



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sanya24071998@localhost/flask'
db = SQLAlchemy(app)
manager = Manager(app)
app.register_blueprint(apiapp, url_prefix='/api')
api = Api(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    pws = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    profs = db.relationship('Profile', uselist=False)

    def __str__(self):
        return self.username


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    old = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    posts = db.relationship('Post', backref='cat')


post_tags = db.Table('post_tags',
db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    datecreated = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    category = db.Column(db.Integer(), db.ForeignKey('category.id'))
    tags = db.relationship('Tag', secondary=post_tags, backref='posts')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)



    def __repr__(self):
        return f'tag {self.id}'



@app.route('/')
def index():
    objects = User.query.all()
    context = {
        'users': objects,
    }
    return render_template('index.html', **context)


@app.route('/add', methods=['GET', "POST"])
def add():
    if request.method == 'POST':
        user_cur = User(email=request.form['email'], pws=generate_password_hash(request.form['psw']),
                        username=request.form['username'])
        db.session.add(user_cur)
        prof = Profile(title=request.form['username'], old=request.form['old'], user_id=user_cur.id)
        db.session.add(prof)
        db.session.commit()
        return redirect(url_for('index'))
    res = make_response(render_template('adduser.html'))
    return res



class AddPot(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('category')
        parser.add_argument('tags', action='append')
        new_post = Post(title=parser.parse_args().get('title'), category=parser.parse_args().get('category'))
        tags = list(map(int, parser.parse_args().get('tags')))
        for tag in tags:
            cur_tag = Tag.query.get(tag)
            if cur_tag is not None:
                new_post.tags.append(cur_tag)
        db.session.add(new_post)
        db.session.commit()
        print(parser.parse_args())
        return {'message': 'success'}

class GetUpdateDeletePost(Resource):
    def put(self, post_id):
        post = Post.query.get(post_id)
        if post is None:
            return {"message": "There is not such post"}
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('category')
        parser.add_argument('tags', action='append')
        fileds_for_iter = post.__dict__.items()
        for key, value in fileds_for_iter:
            if key in parser.parse_args().keys() and parser.parse_args()[key] is not None:
                post.__dict__[key] = parser.parse_args()[key]
        print(post.__dict__)
        ser = Serializer(post, ['title', 'category', 'id'])
        resp = ser.tojson()
        db.session.add(post)
        db.session.commit()
        return resp

    def get(self, post_id):
        post = Post.query.get(post_id)
        if post is None:
            return {"message": "There is not such post"}
        ser = Serializer(post, ['title', 'category'])
        return ser.tojson()



api.add_resource(AddPot, '/addpost')
api.add_resource(GetUpdateDeletePost, '/post/<int:post_id>')


with app.test_request_context('/dsfas'):
    c = Post.query.get(3)
    print(c.__dict__)

if __name__ == '__main__':
    manager.run()
