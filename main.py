from datetime import date

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor

from forms import CreatePostForm, EditPostForm

# Bootstrap, SQLAlchemy and Flask is initialized
app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"
db = SQLAlchemy()
db.init_app(app)
Bootstrap5(app)
ckeditor = CKEditor(app)


# Configure table classes
class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer, unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


# Website routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects/computer_science')
def computer_science():
    results = db.session.execute(db.select(BlogPost).where(BlogPost.category == 'Computer Science'))
    posts = results.scalars().all()
    return render_template('projects_base.html',
                           topic='Computer Science',
                           all_posts=posts,
                           color='#48cae4')


@app.route('/projects/electronics')
def electronics():
    results = db.session.execute(db.select(BlogPost).where(BlogPost.category == 'Electronics'))
    posts = results.scalars().all()
    return render_template('projects_base.html',
                           topic='Electronics',
                           all_posts=posts,
                           color='#00b4d8')


@app.route('/projects/robotics')
def robotics():
    results = db.session.execute(db.select(BlogPost).where(BlogPost.category == 'Robotics'))
    posts = results.scalars().all()
    return render_template('projects_base.html',
                           topic='Robotics',
                           all_posts=posts,
                           color='#0096c7')


@app.route('/projects/new_post', methods=['GET', 'POST'])
def add_new_post():
    cat = request.args.get('cat')
    form = CreatePostForm()

    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            date=date.today().strftime('%B %d, %Y'),
            category=cat
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('create_post.html', topic=cat, form=form)


@app.route('/projects/<cat>')
def show_post(cat):
    post_id = int(request.args.get('post_id'))
    post = db.get_or_404(BlogPost, post_id)
    return render_template('post.html', post=post)


@app.route('/delete_post', methods=['POST', 'GET'])
def delete_post():
    post_id = request.args.get('id')
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/edit_post', methods=['POST', 'GET'])
def edit_post():
    id_ = request.args.get('id')
    post = db.get_or_404(BlogPost, id_)
    form = EditPostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body,
        category=post.category
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        post.category = form.category.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form, is_edit=True)


if __name__ == '__main__':
    app.run(debug=True)
