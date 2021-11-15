from flask import Flask, render_template  

# This sets up the application using the Flask object from the package flask.
app = Flask(__name__)


@app.route('/', methods=['GET'])  # Define http method
def home():
    return "Data collection visualization API"


@app.route('/visuals')
def getUsers():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)