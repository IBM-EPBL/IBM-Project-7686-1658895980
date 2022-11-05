from flask import Flask,render_template,request,redirect,url_for,flash,session
import sqlite3 as sql
app=Flask(__name__)

def get_db():
    conn = sql.connect('client_details.db')
    return conn

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        uname = request.form['uname']
        password = request.form['pass']

        conn = get_db()
        curr = conn.cursor()

        curr.execute('INSERT INTO client_details (username, email, password) VALUES (?, ?, ? );', (uname, email, password )
        )

        conn.commit()
        return redirect(url_for("home"))
    
    return render_template("signup.html")

@app.route("/signin", methods=['POST','GET'])
def signin():
    error = None
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['pass']
        print("signin post")
        conn = get_db()
        conn.row_factory = sql.Row
        cur = conn.cursor()
        user = cur.execute('SELECT username FROM client_details WHERE password = ?',(password,)).fetchone()
        
        if user is None:
            error = 'Incorrect Username/Password.'
        if error is None:
            return redirect(url_for("home"))

    return render_template("signin.html")

if __name__ == "__main__":
    app.secret_key == "AJda0d09ajd0aw0djh92jepm21w=-0o90I(i"
    app.run(debug=True)