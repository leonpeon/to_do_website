"""
TO DO:
1. Create an empty database.
2. Create a text field where the user can type in a task.
3. Enter the text into the database.
4. If the user crosses out an item, present the task as crossed out.
5. If all tasks are done, show a funny gif.
6. Find way to edit the title of the list when the title is pressed.
"""


from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from datetime import date

app = Flask(__name__)

# DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///to_do.db"
db = SQLAlchemy()
db.init_app(app)

class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    todo_item: Mapped[str] = mapped_column(String(150), nullable=False)
    complete: Mapped[bool] = mapped_column(Boolean, nullable=False)
    date_created: Mapped[date] = mapped_column(nullable=False)

with app.app_context():
    db.create_all()

# PAGES
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        new_todo = Todo(
            todo_item=request.form["task"],
            complete=False,
            date_created=date.today()
        )
        db.session.add(new_todo)
        db.session.commit()
        
    return render_template("index.html", date=date.today().strftime("%d/%m"))



if __name__ == "__main__":
    app.run(debug=True)

