from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import logging

logger = logging.getLogger("flask.application")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/' , methods = ["GET" , "POST"])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title , desc = desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html' , allTodo = allTodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:sno>")
def update(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.update(todo)
    db.session.commit()
    return redirect('/')

    
@app.route('/show')
def Products():
    alltodo = Todo.query.all()
    print(alltodo)
    print(type(alltodo[0]))
    logger.info(f"{alltodo}")
    return "This is products page"

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    # debug = true means koi bhi error aaye toh  ujhe browser me dikh jaaye 
    app.run(debug=True, port=8000)