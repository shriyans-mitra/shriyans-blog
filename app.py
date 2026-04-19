import re
import os 
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
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


# ── Helper ────────────────────────────────────────────────

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text


# ── Public Routes ─────────────────────────────────────────

@app.route('/')
def home():
    posts = Post.query.filter_by(published=True) \
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
    posts = Post.query.filter_by(category_id=cat.id, published=True) \
                      .order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('category.html', category=cat, posts=posts,
                           categories=categories)

@app.route('/about')
def about():
    categories = Category.query.all()
    return render_template('about.html', categories=categories)


# ── Admin Routes ──────────────────────────────────────────
@app.route('/reset-password/<secret>')
def reset_password(secret):
    if secret != os.environ.get('SETUP_SECRET'):
        return 'Forbidden', 403
    user = User.query.first()
    user.username = 'shriyans'
    user.set_password('Lamada22#1')
    db.session.commit()
    return 'Password reset!'

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password.')
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_dashboard():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('admin/dashboard.html', posts=posts,
                           categories=categories)

@app.route('/admin/new-post', methods=['GET', 'POST'])
@login_required
def admin_new_post():
    categories = Category.query.all()
    if request.method == 'POST':
        title   = request.form['title']
        content = request.form['content']
        excerpt = request.form.get('excerpt', '')
        category_id = request.form.get('category_id') or None
        published   = 'published' in request.form

        # Generate a unique slug from the title
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Post.query.filter_by(slug=slug).first():
            slug = f'{base_slug}-{counter}'
            counter += 1

        post = Post(title=title, slug=slug, content=content,
                    excerpt=excerpt, category_id=category_id,
                    published=published)
        db.session.add(post)
        db.session.commit()
        flash('Post published successfully!')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/post_form.html', post=None,
                           categories=categories)

@app.route('/admin/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_post(id):
    post = Post.query.get_or_404(id)
    categories = Category.query.all()
    if request.method == 'POST':
        post.title      = request.form['title']
        post.content    = request.form['content']
        post.excerpt    = request.form.get('excerpt', '')
        post.category_id = request.form.get('category_id') or None
        post.published  = 'published' in request.form
        db.session.commit()
        flash('Post updated successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/post_form.html', post=post,
                           categories=categories)

@app.route('/admin/delete-post/<int:id>', methods=['POST'])
@login_required
def admin_delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/categories', methods=['GET', 'POST'])
@login_required
def admin_categories():
    if request.method == 'POST':
        name = request.form['name'].strip()
        slug = slugify(name)
        if not Category.query.filter_by(slug=slug).first():
            db.session.add(Category(name=name, slug=slug))
            db.session.commit()
            flash('Category added!')
        else:
            flash('A category with that name already exists.')
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/delete-category/<int:id>', methods=['POST'])
@login_required
def admin_delete_category(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted.')
    return redirect(url_for('admin_categories'))


# ── Init DB ───────────────────────────────────────────────

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)