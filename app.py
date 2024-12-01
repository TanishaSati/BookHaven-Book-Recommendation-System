from flask import Flask, render_template, request, redirect, url_for, flash, session
import pickle
import numpy as np
import os
import zipfile

# Ensure necessary .pkl files are extracted
def ensure_pkl_files_exist():
    zip_files = {
        'popular.zip': 'popular.pkl',
        'pt.zip': 'pt.pkl',
        'books.zip': 'books.pkl',
        'similarity_scores.zip': 'similarity_scores.pkl',
    }
    for zip_file, pkl_file in zip_files.items():
        if not os.path.exists(pkl_file) and os.path.exists(zip_file):
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall()

ensure_pkl_files_exist()
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# User credentials (for demo purposes)
users = {}

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=[round(r, 2) for r in popular_df['avg_rating'].values]
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Check if the user input exists in the pt.index
    if user_input in pt.index:
        # Find the index of the user input book in pt
        index = np.where(pt.index == user_input)[0][0]

        # Get similar books based on similarity scores
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:9]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)

        return render_template('recommend.html', data=data)
    else:
        # If the book is not found in pt.index, show a message and redirect back
        flash('Sorry, the book you entered is not in our database. Please try again with a valid book title.', 'danger')
        return redirect(url_for('recommend_ui'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            flash('Username already exists. Please log in.', 'danger')
            return redirect(url_for('login'))
        users[username] = password
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

