from flask import Flask
from flask import request
from flask import send_from_directory

#FOLDER NEEDS TO CHANGE
UPLOAD_FOLDER = '/mnt/c/users/t-toyang/Pictures/'

app = Flask(__name__)
app.config

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename);

if __name__ == "__main__":
        app.run()

