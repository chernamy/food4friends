from flask import Flask, render_template
import config
import controllers
import extensions

app = Flask(__name__)

app.register_blueprint(controllers.login)
app.register_blueprint(controllers.logout)
app.register_blueprint(controllers.buy)
app.register_blueprint(controllers.sell)
app.register_blueprint(controllers.user)
app.register_blueprint(controllers.community)
app.register_blueprint(controllers.communities)

if __name__ == '__main__':
    # listen on external IPs
    extensions.Init()
    #app.config["SSL"] = True
    app.config["SECRET_KEY"] = "12345"
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
