from flask import Flask, request
import subprocess
import os
import re

app = Flask(__name__)

@app.route("/pull/<string:repo>", methods=["POST",], defaults={"branch": "main"})
@app.route("/pull/<string:repo>/<string:branch>", methods=["POST"])
def pull(repo, branch):
    subprocess.call(["sh", "push.sh", repo, "abfab-online-backup", "abfab", os.environ.get("PASSWORD"), "Save online changes before deploying " + branch])
    subprocess.call(["sh", "pull.sh", repo, branch, "abfab", os.environ.get("PASSWORD")])
    return ""

@app.route("/push/<string:repo>", methods=["POST",], defaults={"branch": "main"})
@app.route("/push/<string:repo>/<string:branch>", methods=["POST"])
def push(repo, branch):
    content = request.get_json() or {}
    commit = content.get("commit", "Sync online changes")
    subprocess.call(["sh", "push.sh", repo, branch, "abfab", os.environ.get("PASSWORD"), commit])
    return ""

app.run()
