from flask import Flask
import subprocess
import os
import re

app = Flask(__name__)

def is_suspicious(param):
    # yeah we are about to run a command in the system, we don"t want to allow any funny business
    return not re.match(r"^[a-zA-Z0-9_-]+$", param)

@app.route("/pull/<string:repo>", methods=["POST",], defaults={"branch": "main"})
@app.route("/pull/<string:repo>/<string:branch>", methods=["POST"])
def pull(repo, branch):
    if is_suspicious(repo) or is_suspicious(branch):
        return "Invalid repo or branch name", 400
    subprocess.call(["sh", "push.sh", repo, "abfab-online-backup", "abfab", os.environ.get("PASSWORD")])
    subprocess.call(["sh", "pull.sh", repo, branch, "abfab", os.environ.get("PASSWORD")])
    return ""

@app.route("/push/<string:repo>", methods=["POST",], defaults={"branch": "main"})
@app.route("/push/<string:repo>/<string:branch>", methods=["POST"])
def push(repo, branch):
    if is_suspicious(repo) or is_suspicious(branch):
        return "Invalid repo or branch name", 400
    subprocess.call(["sh", "push.sh", repo, branch, "abfab", os.environ.get("PASSWORD")])
    return ""

app.run()
