from flask import Flask
from apps.test.test_route import blueprint_test

app = Flask(__name__)

app.register_blueprint(blueprint_test)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
