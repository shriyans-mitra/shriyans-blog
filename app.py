from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User, Post, Category

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ─── Public Routes ────────────────────────────────────────

@app.route('/')
def home():
    posts = Post.query.filter_by(published=True)\
                      .order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('index.html', posts=posts, categories=categories)

@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    categories = Category.query.all()
    return render_template('post.html', post=post, categories=categories)

@app.route('/category/<slug>')
def category(slug):
    cat = Category.query.filter_by(slug=slug).first_or_404()
    posts = Post.query.filter_by(category_id=cat.id, published=True)\
                      .order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('category.html', category=cat, posts=posts, categories=categories)

@app.route('/about')
def about():
    categories = Category.query.all()
    return render_template('about.html', categories=categories)

# ─── Init DB ──────────────────────────────────────────────

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)