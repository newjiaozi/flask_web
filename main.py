from flask import Flask
from apps.test.test_route import blueprint_test
from apps.wechat.wechat_route import blueprint_wechat
from apps.logger.logger import handler

app = Flask(__name__)
app.register_blueprint(blueprint_test)
app.register_blueprint(blueprint_wechat)
app.logger.addHandler(handler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
