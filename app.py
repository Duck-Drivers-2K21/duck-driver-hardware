from flask import Flask
import git


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/update', methods=['POST'])
def update():
    print("trying")
    g = git.cmd.Git("C:/Users/sgavr/PycharmProjects/test")
    print("connected")
    g.pull()
    print("received it")
    return "Updating"


@app.route('/check')
def check_repo():

    return


if __name__ == '__main__':
    app.run()