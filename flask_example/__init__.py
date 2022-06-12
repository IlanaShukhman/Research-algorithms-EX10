from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


from flask_example import routes