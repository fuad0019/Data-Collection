from flask import Flask, render_template  
import datapuller

# This sets up the application using the Flask object from the package flask.
app = Flask(__name__)


@app.route('/', methods=['GET'])  # Define http method
def home():
    return "Data collection visualization API"


@app.route('/user')
def getUsers():
    var = str(datapuller.get_users())
    print("Var is: " + var)
    if var == "Updated Users":
        return render_template("index.html", value=var)
    elif var == "Users is up to date":
        return render_template("index.html", value=var)
    else:
        return var


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)