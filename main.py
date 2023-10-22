from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

# Bootstrap and Flask is initialized
app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp_key'

Bootstrap5(app)


# Website routes
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
