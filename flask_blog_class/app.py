import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'


# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

#FUnction to retrieve a post from the database
def get_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if post is None:
        abort(404)
    return post


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #get connection to database
    conn = get_db_connection()
    
    #excecute query to read all posts from post table
    posts = conn.execute('SELECT * FROM posts').fetchall()
    
    #close the connection
    conn.close()
    # send the posts to the index.html template to be displayed
    
    
    return render_template('index.html', posts=posts)


# route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    #Determine if post is being requested with a post or get request
    if request.method == 'POST':
        #get title and content that was submitted
        title = request.form['title']
        content = request.form['content']
        #display error message if title or conten is not submitted
        if not title:
            flash("Title is required")
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            #insert data into database
            conn.execute('Insert INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        #else makje a db connection and insert the content blog post
    return render_template('create.html')

# Create a route to edit a post. Load page with the get or post method
#pass the post id as a url parameter

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    #get the post from the database with a select query for the post with that id
    post = get_post(id)
    
    #Determine if the pafe was requested with GET or POST
    if request.method == 'POST':
        # get the title and conten
        title = request.form['title']
        content = request.form['content']
        
        #if no title or content, flash an error message
        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            
            #Redirect to homepage
            
            return redirect(url_for('index'))
    
    #if post process the form data. Get data and validate. Update the post and redirect to the home page
      
    # If GET then display page
    return render_template('edit.html', post=post)

#create a route to delete a post
#Delete page will only be processed with a POST method

## the post id is the url parameter
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    #get the post 
    post = get_post(id)
    # connect to db
    conn = get_db_connection()
    #execute delete query
    conn.execute('DELETE from posts WHERE id = ?', (id,))
    #commit and close connection
    conn.commit()
    conn.close()
    
    #flash success message
    flash('"{}" was successfully deleted!'.format(post['title']))
    #Redirect homepage
    
    
    return redirect(url_for('index'))
    
    

app.run(port=5008)