from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

# Set up the database
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    # Insert a demo user (username: admin, password: password)
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'password')")
    c.execute("INSERT INTO users (username, password) VALUES ('rohithash', 'rohithash')")
    conn.commit()
    conn.close()

# Run the database setup
init_db()

# HTML template with login form
login_form = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    <form method="POST" action="/">
        <label>Username:</label><br>
        <input type="text" name="username"><br>
        <label>Password:</label><br>
        <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # WARNING: Vulnerable query (for educational purposes only)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            return "Login successful! Welcome, " + username
        else:
            return render_template_string(login_form, error="Invalid credentials!")

    return render_template_string(login_form)

if __name__ == "__main__":
    app.run(debug=True)