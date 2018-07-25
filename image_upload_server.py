from flask import Flask
from flask import request
from flask import send_from_directory

#Need to verify that this works
UPLOAD_FOLDER = 'images/testing/'

app = Flask(__name__)
app.config

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename);

if __name__ == "__main__":
        app.run()
