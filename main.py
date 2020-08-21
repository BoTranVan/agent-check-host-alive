# -*- coding: utf-8 -*-

import flask
import subprocess


from flask import request


from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = flask.Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash(
        "admin"),
    "ministry": generate_password_hash(
        "ministry")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


# Define a function for the thread
def do_ping(hostname):
    try:
        args = ['/bin/ping', '-c', '3', '-W', '1', str(hostname)]
        p_ping = subprocess.Popen(
            args,
            shell=False,
            stdout=subprocess.PIPE
        )
        # save ping stdout
        p_ping_out = p_ping.communicate()[0]
        p_ping.wait()

        result = {
            'ping_out': p_ping_out.decode("utf-8"),
            'ping_wait': p_ping.wait()
        }
        app.logger.info("Hello, {}! Checking host {}: {}".format(
            auth.current_user(), hostname, result))
        return result
    except:
        app.logger.info("Hello, {}! Checking host {}: {}".format(
            auth.current_user(), hostname, {}))
        return {
            'ping_out': "",
            'ping_wait': 2
        }


@app.route('/ping')
@auth.login_required
def ping():
    hostname = request.args.get("hostname")

    ping_result = do_ping(hostname)
    return ping_result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
