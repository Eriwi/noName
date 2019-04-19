from server import app, login, db
from flask import render_template, jsonify, request
from server.forms import ContactForm, LoginForm, RegistrationForm, ArticleForm
from flask_login import current_user, login_user, logout_user, login_required
from server.models import User, Article


@app.route('/')
def start():
    return render_template("start.html")


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/articles')
def articles_view():
    articles = Article.query.order_by(Article.timestamp.desc()).all()
    return render_template("articles.html", articles=articles)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'GET':
        return render_template("contact.html", form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            return jsonify({'message': 'Thank you for your message'})
        else:
            return jsonify({'message': 'Please make sure the email you have entered is correct.'})


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'You are now registered!'})
        else:
            msg = ""
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    msg += (fieldName + ": " + err + " ")
            return jsonify({'message': msg})


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                return jsonify({'message': 'Invalid password or username'})
            login_user(user)
            return jsonify({'message': 'logged in'})
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('index.html')
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'message': 'logged out'})


@app.route('/createarticle', methods=['GET', 'POST'])
@login_required
def create_article():
    form = ArticleForm()
    if request.method == 'GET':
        return render_template('createarticle.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            article = Article(text=form.text.data, title=form.title.data, author_id=current_user.id)
            article.create_desc()
            db.session.add(article)
            db.session.commit()
            return jsonify({'message': 'Your article is now added'})
        else:
            msg = ""
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    msg += (fieldName + ": " + err + " ")
            return jsonify({'message': msg})


@app.route('/article/<int:article_id>')
def article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if article is not None:
        return jsonify(article.serialize())


@app.route('/delete/<int:article_id>', methods=['POST'])
@login_required
def delete(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if article is not None:
        db.session.delete(article)
        db.session.commit()
        return jsonify({'message':'The article has been deleted.'})
    return jsonify({'message':'Something went wrong, please try again.'})