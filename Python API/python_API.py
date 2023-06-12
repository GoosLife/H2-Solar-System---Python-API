from application import app
import router

import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if __name__ == '__main__':
    app.run(host="0.0.0.0")