"""
TO DO:
1. Create an empty database.
2. Create a text field where the user can type in a task.
3. Enter the text into the database.
4. If the user crosses out an item, present the task as crossed out.
5. If all tasks are done, show a funny gif.
6. Find way to edit the title of the list when the title is pressed.
"""


from flask import Flask, render_template, request, redirect
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

# Deletes old tasks
    db.session.execute(db.delete(Todo).where(Todo.date_created != date.today()))
    db.session.commit()

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

    # Gets list of task from the database
    task_list = db.session.execute(db.select(Todo).order_by(Todo.id)).scalars().all()

    # If all tasks are done, show a gif
    show_gif = False
    if len(task_list) > 0:
        task_done = []
        for task in task_list:
            task_done.append(task.complete)
        if 0 not in task_done:  
            show_gif = True
    
    return render_template("index.html", date=date.today().strftime("%d/%m"), tasks=task_list, show_gif=show_gif)

@app.route('/cross/<int:post_id>', methods=["GET", "POST"])
def complete_task(post_id):
    requested_task = db.get_or_404(Todo, post_id)
    requested_task.complete = True
    db.session.commit()
    return redirect("/")

@app.route('/delete/<int:post_id>', methods=["GET", "POST"])
def delete_task(post_id):
    requested_task = db.get_or_404(Todo, post_id)
    db.session.delete(requested_task)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

