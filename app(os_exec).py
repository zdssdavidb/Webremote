from flask import Flask, render_template, request
import subprocess, os
print(os.getcwd())
app = Flask(__name__)

@app.route('/')         # when client connects to address - do what follows this line
def index():
    return render_template('index.html')

@app.route('/execute-command', methods=['POST'])        # when client requests this function via html - do what follows this line
def execute_command():
    command = request.form['command']
    result = subprocess.check_output(command, shell=True)
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
