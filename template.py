import os

dirs = [
    os.path.join("data", "raw"),
    os.path.join("data", "processed"),
    "notebooks",
    "saved_models",
    "src",
    "report",
    "data_given",
    "tests",
    os.path.join("prediction_service", "model"),
    os.path.join("webapp", "static", "css"),
    os.path.join(".github", "workflows")
]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass

files = [
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    "tox.ini",
    "requirements.txt",
    "setup.py",
    os.path.join("src", "__init__.py"),
    "app.py",
    os.path.join("prediction_service", "__init__.py"),
    os.path.join("prediction_service", "prediction.py"),
    os.path.join("workflows", "ci-cd.yaml"),
    "Procfile"
]

for file_ in files:
    with open(file_, "w") as f:
        pass