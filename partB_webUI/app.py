# https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
# https://stackoverflow.com/questions/52162882/set-flask-environment-to-development-mode-as-default
from flask import Flask
from flask import render_template, request, url_for, flash, redirect
import subprocess, os, json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=('GET', 'POST'))
def formandTable():
    if request.method == 'POST':
        userQuery = request.form['content']

        if userQuery == "":
            flash('Query is required!')
        else:
            command = f'python3 queryParser.py index \"{userQuery}\"'
            cwd = os.getcwd()
            process = subprocess.Popen(command, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                result = stdout.decode('utf-8')
                # print(result)
            else:
                print(stderr.decode('utf-8'))
        # return redirect(url_for('index')) # sp query doesnt show in url
    return render_template('index.html', userQuery=userQuery, user_Clicked=True, result=json.loads(result))

if __name__ == '__main__':
    app.run(debug=True)