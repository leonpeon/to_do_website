"""
TO DO:
1. Create an empty database.
2. Create a text field where the user can type in a task.
3. Enter the text into the database.
4. If the user crosses out an item, present the task as crossed out.
5. If all tasks are done, show a funny gif.
6. Find way to edit the title of the list when the title is pressed.
"""


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from datetime import datetime

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///to_do.db"
# db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html", date=datetime.today().strftime("%d/%m"))



if __name__ == "__main__":
    app.run(debug=True)

