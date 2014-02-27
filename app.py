from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("user_id"):
        user_id = session.get("user_id")
        username = model.get_username_by_id(user_id)
        return "User %s is logged in!!!!" % username
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    model.connect_to_db()
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)
    if model.authenticate(username, password):
        flash("User authenticated")
        session['user_id'] = user_id
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")

    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/user/<username>")
def view_user(username):
    model.connect_to_db()
    posts = model.get_user_posts(username)
    print posts
    return render_template("wall.html", posts=posts, username=username)

@app.route("/logout")
def get_me_out_of_here():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug = True)


