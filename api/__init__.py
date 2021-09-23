from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = '415d9fdfcc2175c2e8bd7bdb2729befc1e788b88799c46d41d2c1ac4fb11b7ec'

@app.route("/")
def home():
    return render_template("home.html")