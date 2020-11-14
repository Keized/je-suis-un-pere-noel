from flask import Flask, request, jsonify

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape App.config['MY_VARIABLE']


@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)

