import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.user import User, db
from models.post import Post
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
db.init_app(app)
jwt = JWTManager(app)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    user = User(username=username)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'Invalid username'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

@app.route('/compose', methods=['POST'])
@jwt_required()
def compose():
    content = request.json.get('content')
    user = User.query.filter_by(username=get_jwt_identity()).first()

    if not content:
        return jsonify({'message': 'Content is required'}), 400

    post = Post(content=content, user_id=user.id)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'}), 201

@app.route('/follow/<int:followee_id>', methods=['POST'])
@jwt_required()
def follow(followee_id):
    follower = User.query.filter_by(username=get_jwt_identity()).first()
    followee = User.query.get(followee_id)

    if not followee:
        return jsonify({'message': 'Followee not found'}), 404

    follower.following.append(followee)
    db.session.commit()

    return jsonify({'message': 'Now following'}), 200

@app.route('/unfollow/<int:followee_id>', methods=['POST'])
@jwt_required()
def unfollow(followee_id):
    follower = User.query.filter_by(username=get_jwt_identity()).first()
    followee = User.query.get(followee_id)

    if not followee:
        return jsonify({'message': 'Followee not found'}), 404

    follower.following.remove(followee)
    db.session.commit()

    return jsonify({'message': 'Unfollowed successfully'}), 200

@app.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    user = User.query.filter_by(username=get_jwt_identity()).first()
    following_ids = [user.id] + [u.id for u in user.following]
    posts = Post.query.filter(Post.user_id.in_(following_ids)).order_by(Post.created_at.desc()).limit(10).all()

    feed = []
    for post in posts:
        feed.append({
            'post_id': post.id,
            'content': post.content,
            'author': post.user.username,
            'created_at': post.created_at
        })

    return jsonify(feed), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
