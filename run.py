from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///to-do.db"
db = SQLAlchemy(app)

with app.app_context():
        db.create_all()

#Data Class
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    content = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String, default='active')

    def __repr__(self):
        return f'ToDo{self.id}'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_todo = ToDo(content=content)
            db.session.add(new_todo)
            db.session.commit()
    tasks = ToDo.query.filter_by(status='active').all()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id:int):
    todo = ToDo.query.get_or_404(id)
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"ERROR {e}"
    
@app.route('/complete/<int:id>')
def complete(id: int):
    todo = ToDo.query.get_or_404(id)
    todo.status = 'completed'
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id:int):
    item = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        item.content = request.form.get('content')
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', item=item)

@app.route('/completed')
def completed():
    tasks = ToDo.query.filter_by(status='completed').all()
    return render_template('completed.html', tasks=tasks)

# Initialize database after models are defined
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)






