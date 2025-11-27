import os
from flask import Flask, jsonify
import requests
import environs

app = Flask(__name__)
env = environs.Env()

githubUsername = env.str("githubUsername")
githubRepository = env.str("githubRepository")
commitSha = os.environ.get("VERCEL_GIT_COMMIT_SHA")
url = f"https://api.github.com/repos/{githubUsername}/{githubRepository}/commits/{commitSha}"
r = requests.get(url)
repoData = r.json()
commitData = repoData["commit"]
buildData = { 'sha': repoData['sha'], 'timestamp': commitData['author']['date'] }
@app.route("/")
def home():
    return jsonify(buildData)

if __name__ == "__main__":
    app.run(debug=True)