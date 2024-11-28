from flask import Blueprint, flash, render_template, request, redirect, url_for
from .models import User, Movie, Review
from . import db

main = Blueprint('main', __name__)



# ----- Index -----

@main.route('/')
def index():
    return redirect(url_for('main.movies'))



# -------------- Authorization routes -----------------

# Register
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username and email and password:
            if not (len(username) >= 8):
                flash('Username must be at least 8 characters')
                return render_template('register.html')

            if '@' not in email or '.' not in email:
                flash('Please enter a valid email address')
                return render_template('register.html')

            if not (len(password) >= 8):
                flash('Password must be at least 8 characters')
                return render_template('register.html')

            new_user = User(username=username, email=email)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('main.login'))

        flash('Please enter all fields')
        return render_template('register.html')

    return render_template('register.html')

# Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            user = User.query.filter_by(username=username).first()

            if user is None:
                # User not found
                flash('User not found')
                return render_template('login.html')
            else:
                # User found
                correct_password = user.check_password(password)

                if correct_password:
                    # Correct password
                    return redirect(url_for('main.movies'))
                else:
                    # Incorrect password
                    flash('Incorrect password')
                    return render_template('login.html')
        flash('Please enter all fields')

    return render_template('login.html')

# Logout
@main.route('/logout')
def logout():
    return render_template('logout.html')



# ---------------------------- Movie review routes ----------------------------------

# Browse movies
@main.route('/movies')
def movies():
    return render_template('movies.html', Movies=Movie.query.all())

# Page for a specific movie
@main.route('/movie/<movie_id>')
def movie(movie_id):
    selected_movie = Movie.query.get(movie_id)
    reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.id.desc()).all()

    return render_template('movie.html', movie=selected_movie, reviews=reviews)

# Create review
@main.route('/movie/<movie_id>/write-review', methods=['POST', 'GET'])
def write_review(movie_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        rating = request.form['rating']

        new_review = Review(review_title=title, review_content=content, rating=rating, user_id=1, movie_id=movie_id)

        db.session.add(new_review)

        db.session.commit()

        return redirect(url_for('main.movie', movie_id=movie_id))
    return render_template('write-review.html', Movie=Movie.query.get(movie_id))

# Delete review TODO: Revise this
@main.route('/movie/<movie_id>/delete-review/<review_id>', methods=['POST', 'GET'])
def delete_review(movie_id, review_id):
    if request.method == 'POST':
        # POST request deletes the review
        db.session.delete(Review.query.get(review_id))
        db.session.commit()
        # Redirect to main movie page
        return redirect(url_for('main.movie', movie_id=movie_id))

    # GET request to this route returns the 'delete review' page
    return render_template('delete-review.html', movie_id=movie_id, review_id=review_id)