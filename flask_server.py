from flask import Flask, send_file
import os

app = Flask(__name__)

FILES_DIR = 'files'

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    return send_file(os.path.join(FILES_DIR, filename))

if __name__ == '__main__':
    app.run(port=5000)