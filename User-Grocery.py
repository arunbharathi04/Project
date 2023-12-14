import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, jsonify, render_template, request, redirect, session, url_for
import pymysql
app = Flask(__name__)
try:
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="p@ssw0rd"
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS grocery_mart")
    cursor.close()
    db.close()
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="p@ssw0rd",
        database="grocery_mart"
    )
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(15) NOT NULL,
            dob DATE NOT NULL,
            password VARCHAR(100) NOT NULL,
            address VARCHAR (100) NOT NULL,
            picture VARCHAR(255) Not Null
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shop_owner (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(15) NOT NULL,
            dob DATE NOT NULL,
            password VARCHAR(100) NOT NULL,
            shopName VARCHAR(100) NOT NULL,
            productName VARCHAR(100) NOT NULL,
            shopAddress VARCHAR(255) NOT NULL,
            shopCanact VARCHAR(255) NOT NULL,
            productPrice VARCHAR(100) NOT NULL,
            productPic VARCHAR(255) Not Null
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_data LONGBLOB NOT NULL
        )
    """)
    print("Connected to MySQL and database is ready.")
except Exception as e:
    print("Error connecting to MySQL:", e)


@app.route('/', methods=['GET'])
def home():
    # Render the home page
    return render_template('home.html')


@app.route('/', methods=['POST'])
def images():
    # Get the ID from the request data
    data = request.get_json()
    id = data['id']

    # Use the ID to query the database
    db = pymysql.connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM images WHERE id = %s", (id,))
    image_data = cursor.fetchone()[0]

    # Send the image data back to the frontend
    return jsonify(image_data=image_data)


@app.route('/login')
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Admin' and password == 'P@ssw0rd':
            return render_template('admin_page.html')
        else:
            flash("invalid login", "danger")
            return render_template('admin_login.html')
    return render_template('admin_login.html')


@app.route('/admin')
def admin():
    conn = pymysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images WHERE id = 11")
    images_data = cursor.fetchall()
    return render_template('admin_page.html', images_data=images_data)

# List Shop owner list


@app.route('/admin/owner')
def owner():
    conn = pymysql.connect()
    cursor = conn.cursor()
    # select from shop owner to show
    cursor.execute("SELECT * FROM shop_owner")
    shop_owner = cursor.fetchall()
    return render_template('admin_owner.html', owner=shop_owner)

# Admin Page to list shop owner list to accept or decline


@app.route('/admin/owner/<id>')
def accept(id):
    conn = pymysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE shop_owner SET status='reject' WHERE id=%s", (id,))
    # status reject remove the user list in db
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    return redirect(url_for('admin_page.html'))

# Admin/user route to show users


@app.route('/admin/users')
def admin_users():
    conn = pymysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.commit()
    return render_template('admin_page.html', rows=rows)

# Get images from form field to store Bacground pictures


@app.route('/admin/upload', methods=['POST'])
def upload_image():
    # check if the post request has the file part
    file = request.files['upload']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('/path/to/save/images', filename)
        file.save(file_path)
        with open(file_path, 'rb') as f:
            image_data = f.read()
        conn = pymysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO images (image_data) VALUES (%s)", (image_data,))
        conn.commit()
    return render_template('admin_page.html')

# User signin


@app.route('/signup', methods=['GET', 'POST'])
def signin():
    # check owner checkbox checked if not gather user information
    if request.method == 'POST':
        if 'owner' not in request.form:
            if request.method == 'POST':
                Name = request.form['Name']
                phone = request.form['Phone']
                email = request.form['email']
                dob = request.form['dob']
                username = request.form['Username']
                password = request.form['password']
                # get profile picture
                file = request.files['profile']
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join('/path/to/save/images', filename)
                    file.save(file_path)
                    with open(file_path, 'rb') as f:
                        image_data = f.read()
            conn = pymysql.connect()
            cursor = conn.cursor()
            # Insert data into users table
            cursor.execute("INSERT INTO users (Name, phone, email, dob, username, password, picture) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (Name, phone, email, dob, username, password, image_data))
            conn.commit()
            return render_template('login.html')
        else:
            # get form data and store into shop_owner table
            Name = request.form['Name']
            phone = request.form['Phone']
            email = request.form['email']
            dob = request.form['dob']
            username = request.form['Username']
            password = request.form['password']
            shopname = request.form['shopname']
            productname = request.form['productname']
            productprice = request.form['productprice']
            shopaddress = request.form['shopaddress']
            shopcontact = request.form['shopcontact']
            # get product image
            file = request.files['productpic']
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join('/path/to/save/images',
                                         filename)
                file.save(file_path)
                with open(file_path, 'rb') as f:
                    image_data = f.read()
            # Insert into shop_owner table
            conn = pymysql.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO shop_owner(name, phone, email, dob, username, password, shopName, productName, productPrice, shopAddress, shopContact, productPic) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (Name, phone, email, dob, username, password, shopname, productname, productprice, shopaddress, shopcontact, image_data))
            conn.commit()
            return render_template('login.html')
    return render_template('login.html')

# User page logon


@app.route('/userlogin', methods=['GET', 'POST'])
def login():
    db = pymysql.connect()
    cursor = db.cursor()
    username = request.form['uname']
    password = request.form['pass']
    is_owner = 'owner' in request.form
    cursor.execute(
        "GRANT ALL PRIVILEGES ON *grocery_mart* TO 'arunbharathi'@'localhost' WITH GRANT OPTION;")

    if is_owner:
        # Check the owner table for the user
        cursor.execute("SELECT * FROM shop_owner WHERE username = %s AND password = %s",
                       (username, password))
        user = cursor.fetchone()
        if user:
            return render_template("owner_dashboard.html")
    elif not is_owner:
        # Check the regular user table for the user
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                       (username, password))
        user = cursor.fetchone()
        if user:
            return render_template("user_dashboard.html")
    else:
        # Invalid login
        flash('Invalid username or password')
        return render_template("login.html")
    return render_template("login.html")

# user dashboard with route name '/<username>dashboard'


@app.route('/<username>/dashboard')
def dashboard(username):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    # else show user dashboard with user information
    else:
        conn = pymysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        rows = cursor.fetchall()
        # get 2 element as a username and 9 element as a profile picture
        user = rows[0]
        profile = rows[8]
    return render_template('dashboard.html', username=username, profile=profile)

# show products page


@app.route('/products')
def products():
    # Show products page data from shop_owner table shop name, Product name, product prize
    conn = pymysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT shop_name, product_name, product_prize FROM shop_owner")
    rows = cursor.fetchall()
    return render_template('products.html', rows=rows)

# Show Username profile page


@app.route('/<username>/profile')
def profile(username):
    conn = pymysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    rows = cursor.fetchall()
    return render_template('user_dashboard.html', rows=rows)

# logout session


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
