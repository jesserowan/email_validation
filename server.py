from flask import Flask, request, redirect, flash, session, render_template
import re, datetime
from mysqlconnection_copy import connectToMySQL
app = Flask(__name__)
app.secret_key="keep it secret keep it safe"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_email', methods=["POST"])
def process():
    mysql = connectToMySQL('email_val')

    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email format")

    if '_flashes' in session.keys():
        return redirect('/')
    else:
        mysql = connectToMySQL('email_val')

        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"

        data = {
            "email": request.form['email']
        }
        new_email = mysql.query_db(query, data)
        session['id'] = new_email
        return redirect('/success')

@app.route('/success')
def success():
    mysql = connectToMySQL('email_val')

    query = "SELECT * FROM emails;"

    select_all = mysql.query_db(query)

    return render_template('success.html', emails=select_all)


if __name__ == "__main__":
    app.run(debug=True)