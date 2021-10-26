from flask import Flask, request, jsonify
from markupsafe import escape

# This sets up the application using the Flask object from the package flask.
app = Flask(__name__)

@app.route('/', methods=['GET']) # Define http method
def home():
    return 'It lives!'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)