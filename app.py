from flask import Flask, url_for, request, redirect, render_template, session
import bcrypt

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
