from flask import Flask, render_template, request, redirect, flash
import sqlite3
from flask_mail import Mail, Message
import os

app = Flask(__name__, static_folder='static')
app.secret_key = "a88176a7ae237bbbf52d0bf0e523314b"

# --- Email Config ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'chakrabortyabhinavo@gmail.com'
app.config['MAIL_PASSWORD'] = 'ffsx jtey kvrt zkdi'

mail = Mail(app)

# --- Database Function ---
def insert_enquiry(name, phone, email, course, query):
    conn = sqlite3.connect('academy.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO enquiries (name, phone, email, course, query)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, phone, email, course, query))
    conn.commit()
    conn.close()

# --- Route for Contact Page ---
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        course = request.form.get("course")
        query = request.form.get("query")

        # Save to DB
        insert_enquiry(name, phone, email, course, query)

        # Send Email to Admin
        msg = Message(
            subject="New Admission Enquiry",
            sender=app.config['MAIL_USERNAME'],
            recipients=["chakrabortyabhinavo@gmail.com"],
            body=f"Name: {name}\nPhone: {phone}\nEmail: {email}\nCourse: {course}\nQuery: {query}"
        )
        mail.send(msg)

        flash("Enquiry submitted successfully, We will get in touch with you shortly!", "success")
        return redirect("/contact")

    return render_template("contact.html")


# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Courses Page
@app.route('/courses')
def courses():
    return render_template('courses.html')

# Faculty Page
@app.route('/faculty')
def faculty():
    return render_template('faculty.html')

# Testimonials Page
@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

# Gallery Page
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

# Contact Page
# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
