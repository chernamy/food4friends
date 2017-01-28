from flask import Flask, render_template
import config
import controllers

app = Flask(__name__)

app.register_blueprint(controllers.login)
app.register_blueprint(controllers.logout)

if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
