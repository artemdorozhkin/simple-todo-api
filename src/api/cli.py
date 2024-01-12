import os
import sys
import subprocess


docker_path = os.path.join(os.getcwd(), "docker", "docker-compose.yml")
app_path = os.path.join(os.getcwd(), "src", "app.py")
python_path = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")


def docker(action: str, detach: str = None):
    line = ["docker", "compose", "-f", docker_path, action]
    if detach:
        line.append(detach)
    subprocess.call(line)


def run():
    subprocess.call([python_path, app_path])


if __name__ == "__main__":
    if len(sys.argv) == 4:
        globals()[sys.argv[1]](sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        globals()[sys.argv[1]](sys.argv[2])
    else:
        globals()[sys.argv[1]]()
