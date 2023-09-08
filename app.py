from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        post = Post(title=title, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return "В ходе добавления данных произошла ошибка"
    else:
        return render_template('create.html')


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/edit_post/<post_id>', methods=['POST', 'GET'])
def edit_post(post_id):
    if request.method == 'POST':
        try:
            post = Post.query.filter_by(id=post_id).one()
            post.title = request.form['title']
            post.text = request.form['text']
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return "В ходе изменения данных произошла ошибка"
    else:
        return render_template('edit_post.html')

@app.route('/delete_post/<post_id>', methods=['POST', 'GET'])
def delete_post(post_id):
    if request.method == 'GET':
        try:
            post = Post.query.filter_by(id=post_id).one()
            db.session.delete(post)
            db.session.commit()
            return redirect('/')
        except:
            return "В ходе удаления данных произошла ошибка"
    else:
        return 'Пост удалён'


@app.route('/post/<post_id>', methods=['POST', 'GET'])
def full_post(post_id):
    post = Post.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
