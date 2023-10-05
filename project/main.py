from flask import Flask, request
import main

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return "Hello!"


@app.route('/get_projects', methods=["GET"])
def get_projects():
    result = main.getProjects()
    return result


@app.route('/open_in_vscode/', methods=["GET"])
def open_in_vscode():
    id_rec = request.args.get("id")
    main.openProjectInVSCode(id_rec)
    return "200"


@app.route('/close_and_commit/', methods=["GET"])
def close_and_commit():
    id_rec = request.args.get("id")
    main.closeProject(id_rec)
    return "200"


@app.route('/analyze_code/', methods=["GET"])
def analyze_code():
    id_rec = request.args.get("id")
    result = main.analyzeFile(id_rec)
    return result


@app.route('/error_analyze/', methods=["GET"])
def analyze_error_code():
    id_rec = request.args.get("id")
    result = main.analyzeErrorFile(id_rec)
    return result


@app.route('/delete_project/', methods=["GET"])
def delete_project():
    id_rec = request.args.get("id")
    main.deleteProject(id_rec)
    return 200


@app.route('/add_project/', methods=["GET"])
def add_project():
    import datetime
    title = request.args.get("title")
    description = request.args.get("description")
    path = request.args.get("path")

    now = datetime.datetime.now()

    main.addProject(title, description, now.strftime(
        "%H:%M/%d-%m-%Y"), {}, path, now.strftime(
        "%H:%M/%d-%m-%Y"))
    return 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
