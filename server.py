from flask import Flask, render_template

# Create a flask instance

app = Flask(__name__)

#Create a route decorator
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

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html"), 404

if __name__ == "__main__":
  app.run(use_reloader=True, debug=True)