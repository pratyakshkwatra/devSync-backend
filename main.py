import database as db
import datetime
import os
import git
import platform
import subprocess
import g4f
import sys
import random


def getProjects() -> dict:
    session_db_main = db.sessionmaker(bind=db.engine, expire_on_commit=True)
    session_db = session_db_main()
    projects = session_db.query(db.Project).all()

    result = {"data": []}

    for project in projects:
        result["data"].append(
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "timestamp": project.timeStamp,
                "path": project.path,
                "last_used": project.last_used
            }
        )

    return result


def addProject(title: str, description: str, timeStamp: str, details: dict, path: str, last_used: str) -> int:
    session_db_main = db.sessionmaker(bind=db.engine, expire_on_commit=True)
    session_db = session_db_main()
    new_project = db.Project(
        title, description, timeStamp, details, path, last_used)

    session_db.add(new_project)

    try:
        session_db.commit()
    except Exception as e:
        session_db.rollback()
    finally:
        session_db.close()

    return 200


def deleteProject(id_rec: int) -> int:
    session_db_main = db.sessionmaker(bind=db.engine, expire_on_commit=True)
    session_db = session_db_main()
    project = session_db.query(db.Project).filter(
        db.Project.id == int(id_rec)).first()

    session_db.delete(project)

    try:
        session_db.commit()
    except Exception as e:
        session_db.rollback()
    finally:
        session_db.close()

    return 200


def updateProject(title: str, description: str, timeStamp: str, details: dict, path: str, last_used: str) -> int:
    session_db_main = db.sessionmaker(bind=db.engine, expire_on_commit=True)
    session_db = session_db_main()
    project = session_db.query(db.Project).filter(db.Project.id == id).first()

    project.title = title
    project.description = description
    project.timeStamp = timeStamp
    project.details = details
    project.path = path
    project.last_used = last_used

    try:
        session_db.commit()
    except Exception as e:
        session_db.rollback()
    finally:
        session_db.close()

    return 200


def openProjectInVSCode(id_rec: int) -> None:
    session_db_main = db.sessionmaker(bind=db.engine, expire_on_commit=True)
    session_db = session_db_main()
    project = session_db.query(db.Project).filter(
        db.Project.id == int(id_rec)).first()

    now = datetime.datetime.now()
    project.last_used = now.strftime("%H:%M/%d-%m-%Y")

    project_path = project.path
    platform = sys.platform
    if platform == "win32":
        command = f"code {project_path}"
    elif platform == "darwin":
        command = f"code {project_path}"
    elif platform.startswith("linux"):
        command = f"code {project_path}"

    os.system(command)
    try:
        session_db.commit()
    except Exception as e:
        session_db.rollback()
    finally:
        session_db.close()


def closeProject(id_rec: int) -> None:
    session_db_main = db.sessionmaker(bind=db.engine, expire_on_commit=True)
    session_db = session_db_main()
    project = session_db.query(db.Project).filter(
        db.Project.id == int(id_rec)).first()

    now = datetime.datetime.now()
    project.last_used = now.strftime("%H:%M/%d-%m-%Y")

    project_path = project.path
    git_dir = os.path.join(project_path, '.git')

    if os.path.exists(git_dir):
        repo = git.Repo(project_path)
        repo.index.add('*')
        repo.index.commit(f"Commit by DevSync: Summary of the commit")

    system = platform.system()

    if system == 'Windows':
        subprocess.run(['taskkill', '/f', '/im', 'Code.exe'], shell=True)
    elif system == 'Darwin':
        applescript_code = """
        tell application "Visual Studio Code"
            quit
        end tell
        """
        subprocess.run(['osascript', '-e', applescript_code])
    try:
        session_db.commit()
    except Exception as e:
        session_db.rollback()
    finally:
        session_db.close()


def getFiles(id_rec: int) -> list[db.File]:
    session_db_main = db.sessionmaker(bind=db.engine, expire_on_commit=True)
    session_db = session_db_main()
    project = session_db.query(db.Project).filter(
        db.Project.id == id_rec).first()

    files: list[db.File] = []

    for root, _, files_get in os.walk(project.path):
        for file_name in files_get:
            file_path = os.path.join(root, file_name)
            file_object = db.File(files_get.index(
                file_name), file_name, file_path)
            files.append(file_object)

    return files


def analyzeFile(id_rec: int) -> str:
    files = getFiles(id_rec)
    file = files[random.randint(0, len(files)-1)]
    file_content = ""

    with open(file.path, "r") as f:
        try:
            file_content = f.read()
        except:
            file_content = ""

    result = g4f.ChatCompletion.create(g4f.models.gpt_35_turbo, provider=g4f.Provider.You, messages=[{"role": "system", "content": f"""
You are an AI Based Code Analyzer. You have to analyze the file content and give a summary of whats happening. Explain the code.

Strictly Prohibited Content: Sure, here you go, Here is the data, Sorry, As an AI Model, I cannot.
If the code is empty, return that the file format isnt supported
                                                                                                      
Code: {file_content}

Analysis:"""}])

    print(result)

    return result


def analyzeErrorFile(id_rec: int) -> str:
    files = getFiles(id_rec)
    file = random.choice(files)
    file_content = ""

    with open(file.path, "r") as f:
        try:
            file_content = f.read()
        except:
            file_content = ""

    result = g4f.ChatCompletion.create(g4f.models.gpt_35_turbo, provider=g4f.Provider.You, messages=[{"role": "system", "content": f"""
You are an AI Based Code Error Analyzer. You have to analyze the file content and give a summary of whats happening. Explain the issues in the code.

Strictly Prohibited Content: Sure, here you go, Here is the data, Sorry, As an AI Model, I cannot.
If the code is empty, return that the file format isnt supported
                                                                                                      
Code: {file_content}

Error Analysis:"""}])

    print(result)

    return result
# addProject("Test Project", "This project prints out hello world using python", "23:10/05-10-2023",
#            {}, "/Users/pratyakshkwatra/Desktop/applications/devSync/project", "23:10/05-10-2023")
