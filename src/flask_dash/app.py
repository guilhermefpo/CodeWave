from flask import Flask, render_template, url_for
import dash
from dash_app import create_dash_apli


app=Flask(__name__)


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/indicadores")
def indicadores():
    return render_template("principais_indicadores.html", )


create_dash_apli(app)



if __name__=="__main__":
    app.run(debug=True)


