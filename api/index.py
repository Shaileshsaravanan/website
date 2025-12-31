from flask import Flask, jsonify, render_template
from environs import Env
env = Env()
env.read_env()
import requests

GITHUB_USERNAME = "shaileshsaravanan"
GITHUB_TOKEN = env.str("GITHUB_TOKEN")
githubData = {'mechanica': [], 'scriptorium': []}
page = 1

while True:
    r = requests.get(
        f"https://api.github.com/users/{GITHUB_USERNAME}/repos",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        params={"per_page": 100, "page": page}
    )

    data = r.json()
    if not data:
        break

    for repo in data:
        repo_name = repo['name']
        check_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/.website/data.json"
        check = requests.get(
            check_url,
            headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
        )
        if check.status_code == 200:
            raw_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{repo_name}/main/.website/data.json"
            raw = requests.get(
                raw_url,
                headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
            )
            if raw.status_code == 200:
                info = raw.json()
                repo_type = info.get("type")
                if repo_type == "mechanica":
                    githubData['mechanica'].append(repo_name)       
                elif repo_type == "scriptorium":
                    githubData['scriptorium'].append(repo_name)

    page += 1

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html", githubData=githubData)

if __name__ == "__main__":
    app.run(debug=True, port=8000)