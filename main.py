from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def principal():
    return render_template('tienda.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)