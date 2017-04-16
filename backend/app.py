from flask import Flask, render_template, send_from_directory
import config
import controllers
import extensions
import logging
import sys

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.secret_key = "12345"

app.register_blueprint(controllers.login)
app.register_blueprint(controllers.logout)
app.register_blueprint(controllers.buy)
app.register_blueprint(controllers.sell)
app.register_blueprint(controllers.user)
app.register_blueprint(controllers.community)
app.register_blueprint(controllers.communities)
app.register_blueprint(controllers.rating)


extensions.Init()
#app.config["SSL"] = True
app.config["SECRET_KEY"] = "12345"
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == "__main__":
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
