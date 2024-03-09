from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid1
from datetime import datetime
from flask import Flask, render_template, flash, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date
from flask_login import UserMixin, login_user, login_required, LoginManager, logout_user, current_user

from webforms import UserForm, PostForm, LoginForm, NameForm, PasswordForm, SearchForm

# Create a flask instance
app = Flask(__name__)
# Add Database
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:taipei@localhost/users"

# Secret Key
app.config['SECRET_KEY'] = "my sECRet key blAh Blah blaH"
# Intialize the Database
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

# Flask_login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(user_id)

# JSON thing
@app.route('/date')
def get_current_date():
  favorite_pizza = {
    "john": "Pepperoni",
    "Mary": "Cheese",
    "Tim": "Mushroom"
  }
  return favorite_pizza, 200

# Pass Stuff to Navbar
@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)

# Create Search Function
@app.route('/search', methods=["POST"])
def search():
  form = SearchForm()
  posts = Posts.query
  if form.validate_on_submit():
    # Get data from submitted
    post.searched = form.searched.data
    # Query the Database
    posts = posts.filter(Posts.content.like(f"%{post.searched}%"))
    posts = posts.order_by(Posts.title).all()

    return render_template('search.html', form=form, searched=post.searched, posts=posts)
  
# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(username=form.username.data).first()
    if user:
      # check hash
      if check_password_hash(user.password_hash, form.password.data):
        login_user(user)
        flash('Login Successful')
        return redirect(url_for('dashboard'))
      else: 
        flash('Incorrect password')
    else:
      flash('Cannot find the user')

  return render_template('login.html', form=form)

# Create Logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  flash('You have been logged out!')
  return redirect(url_for('login'))

# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
  form = PostForm()

  if form.validate_on_submit():
    post = Posts(
      id=f"post{uuid1().hex}", 
      title=form.title.data,
      content=form.content.data,
      slug=form.slug.data,
      poster_id=current_user.id
    )
    form.title.data = ''
    form.content.data = ''
    form.slug.data = ''

    # Add post to database
    db.session.add(post)
    db.session.commit()

    flash("Blog Post Submitted Successfully")

  # Redirect to the webpage
  return render_template("add_post.html", form=form)

@app.route('/posts/<id>')
def post(id):
  post = Posts.query.get_or_404(id)

  return render_template('post.html', post=post)

@app.route('/posts')
def posts():
  posts = Posts.query.order_by(Posts.date_posted)
  return render_template('posts.html', posts=posts)

@app.route('/posts/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
  post = Posts.query.get_or_404(id)
  form = PostForm()

  if current_user.id == post.poster_id and form.validate_on_submit():
    post.title = form.title.data
    post.slug = form.slug.data
    post.content = form.content.data
    # Update Database
    db.session.add(post)
    db.session.commit()
    flash('Post Has Been Updated')
    return redirect(url_for('post', id=post.id))
 
  if current_user.id == post.poster_id:
    form.title.data = post.title
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)
  else:
    flash("Hey! You cannot edit other users' posts!")
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)

@app.route('/posts/delete/<id>')
@login_required
def delete_post(id):
  post_to_delete = Posts.query.get_or_404(id)

  id = current_user.id
  if id == post_to_delete.poster.id:
    try:
      db.session.delete(post_to_delete)
      db.session.commit()
      # Return a message
      flash("Blog Post was Deleted")
    except:
      flash("Oops there was problem delete post")
    
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)
  else:
    flash("Hey! You cannot delete other users' posts!")
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)

# Create Database Record
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
  name = None
  form = UserForm()
  
  # Validate Form
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email.data).first()
    if user is None:
      user = Users(
        id=f"user{uuid1().hex}", 
        username=form.username.data,
        name=form.name.data, 
        email=form.email.data, 
        favorite_color=form.favorite_color.data,
        password_hash=generate_password_hash(form.password_hash.data, method='pbkdf2:sha256')
      )
      db.session.add(user)
      db.session.commit()
    name = form.name.data
    form.username.data = ''
    form.name.data = ''
    form.email.data = ''
    form.favorite_color.data = ''
    form.password_hash.data = ''
    form.password_hash2.data = ''
    flash("User added Successfully")

  our_users = Users.query.order_by(Users.date_added)
  return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Update Database Record
@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
  form = UserForm()
  name_to_update = Users.query.get_or_404(id)
  if request.method == "POST":
    name_to_update.name = request.form['name']
    name_to_update.email = request.form['email']
    name_to_update.favorite_color = request.form['favorite_color']
    name_to_update.username = request.form['username']

    try:
      db.session.commit()
      flash("User Updated Successfully!")
      return render_template("dashboard.html", form=form)

    except:
      flash("Error! Please try again.")
      return render_template("update.html", 
        form=form,
        name_to_update=name_to_update
      )
  else:
    return render_template("update.html", 
      form=form,
      name_to_update=name_to_update, 
      id=id
    )

# Delete Database Record
@app.route('/delete/<id>')
def delete(id):
  form = UserForm()
  user_to_delete = Users.query.get_or_404(id)

  try:
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User Deleted Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)
  except:
    flash("User Deleted Failed!")
    return render_template("add_user.html", form=form, name=name, our_users=our_users)
  
# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
  form = UserForm()
  return render_template('dashboard.html', form=form)

# Create a route decorator
@app.route('/')
def index():
  first_name = "Johnny"
  stuff = "This is <b>a Bold<g> Text"
  favorite_pizza = ['gadogado', 'cheese', 'pepperoni', 41]
  return render_template("index.html", 
    first_name=first_name, 
    stuff=stuff,
    favorite_pizza=favorite_pizza
  )

@app.route('/user/<name>')
def user(name):
  return render_template("user.html", user_name=name)

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
  name = None
  form = NameForm()
  # Validate Form
  if form.validate_on_submit():
    name = form.name.data
    form.name.data = ''
    flash("Form Submitted Successfully")

  return render_template("name.html",
    name=name,
    form=form                       
  )

# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_tw():
  email = None
  password = None
  pw_to_check = None
  passed = None
  form = PasswordForm()

  # Validate Form
  if form.validate_on_submit():
    email = form.email.data
    password = form.password_hash.data
    #Clear the form
    form.email.data = ''
    form.password_hash.data = ''

    # Lookup user by email
    pw_to_check = Users.query.filter_by(email=email).first()
    
    # Check Hashed Password
    passed = check_password_hash(pw_to_check.password_hash, password)

  return render_template("test_pw.html",
    email=email,
    password=password,
    pw_to_check=pw_to_check,
    passed=passed,
    form=form                       
  )

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html"), 404

# Invalid URL
@app.errorhandler(500)
def page_not_found(e):
  return render_template("500.html"), 500


# Create a Blog Post Model
class Posts(db.Model):
  id = db.Column(db.String(200), primary_key=True)
  title = db.Column(db.String(255))
  content = db.Column(db.Text)
  date_posted = db.Column(db.DateTime, default=datetime.utcnow)
  slug = db.Column(db.String(255))
  # Foreign key to Link Users
  poster_id = db.Column(db.String(200), db.ForeignKey('users.id'))

# Create Model
class Users(db.Model, UserMixin):
  id = db.Column(db.String(200), primary_key=True)
  username = db.Column(db.String(200), nullable=False, unique=True)
  name = db.Column(db.String(200), nullable=False)
  email = db.Column(db.String(200), nullable=False, unique=True)
  favorite_color = db.Column(db.String(120))
  date_added = db.Column(db.DateTime, default=datetime.utcnow)
  # Do some password stuff
  password_hash = db.Column(db.String(128), nullable=False)
  #User can Have Many Posts
  posts = db.relationship('Posts', backref='poster')

  @property
  def password(self):
    raise AttributeError('Password is not a readable attribute')
  
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  # Create a String
  def __repr__(self):
    return '<Name %r>' % self.name


if __name__ == "__main__":
  app.run(use_reloader=True, debug=True)