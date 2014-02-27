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
        return redirect(url_for("view_user", username=request.form.get("username")))
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")
        return redirect(url_for("index"))

@app.route("/register")
def register():
    if session.get("user_id"):
        username = model.get_username_by_id(session.get("user_id"))
        return redirect(url_for('view_user', username=username))
    return render_template("register.html")

@app.route("/user/<username>")
def view_user(username):
    model.connect_to_db()
    posts = model.get_user_posts(username)
    print posts
    return render_template("wall.html", posts=posts, username=username, session=session)

@app.route("/user/<username>", methods=["POST"])
def post_to_wall(username):
    model.connect_to_db()
    content = request.form.get("content")
    author_id = session['user_id']
    owner_id = model.get_user_by_name(username)
    model.create_new_post(owner_id, author_id, content)
    # redirect_string = "/user/%s" % username
    return redirect(url_for('view_user', username=username))

@app.route("/create_account", methods=["POST"])
def create_account():  
    model.connect_to_db()
    username = request.form.get("username")
    
    user_id = model.get_user_by_name("username")
    if user_id == None:
        print 'there is no user id.'
        username = request.form.get("username")
        password = request.form.get("password")
        flash('Account successfully created.')
        model.create_new_account(username,password)
        return redirect(url_for("index"))
    else:
        flash('User already exists.')
        return redirect(url_for('register'))



@app.route("/logout")
def get_me_out_of_here():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug = True)


