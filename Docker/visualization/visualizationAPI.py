from flask import Flask, render_template  
import requests


# This sets up the application using the Flask object from the package flask.
app = Flask(__name__)


@app.route('/', methods=['GET'])  # Define http method
def home():
    return "Data collection visualization API"


@app.route('/user')
def getUsers():
    
    res = requests.get('http://t05-data-puller:80/pullUsers')

    sc = res.status_code

    if(sc >= 200 and sc < 300):
        data = res.json()
        return render_template("index.html", value=data["message"])
    else:
        return {"status code": sc}

    
    
    
    

    



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)