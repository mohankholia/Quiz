from flask import Flask, render_template, request, redirect, url_for
from jinja2 import Environment

app = Flask(__name__)

# Create a Jinja environment with the built-in enumerate function
env = Environment()
@app.template_global()
def enumerate(sequence, start=0):
    return zip(range(start, len(sequence) + start), sequence)

app.jinja_env.globals.update(enumerate=enumerate)

# List of questions with options and correct answer
questions = [
    {
        "question": "What is the capital of India?",
        "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    {
        "question": "Which is the largest ocean in the world?",
        "options": ["Pacific", "Atlantic", "Indian", "Arctic"],
        "answer": "Pacific"
    },
    {
        "question": "Who wrote the book 'The Great Gatsby'?",
        "options": ["Ernest Hemingway", "F. Scott Fitzgerald", "William Faulkner", "John Steinbeck"],
        "answer": "F. Scott Fitzgerald"
    },
    {
        "question": "What is the currency of Japan?",
        "options": ["Yen", "Euro", "Dollar", "Pound"],
        "answer": "Yen"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["Blue Whale", "African Elephant", "Giraffe", "Hippopotamus"],
        "answer": "Blue Whale"
    }
]

# List of prize money for each question
prize_money = [1000, 2000, 5000, 10000, 20000]

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username and password are correct
    if username == 'admin' and password == 'password':
        # Redirect to the game page if the login is successful
        return redirect(url_for('game'))
    else:
        # Show an error message if the login is unsuccessful
        return render_template('login.html', message='Invalid username or password')
"""@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        message = 'Passwords do not match. Please try again.'
        return redirect(url_for('index', message=message))
    
    else:
        
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')
"""
@app.route('/game', methods=['GET', 'POST'])
def game():
    global prize
    prize = 0
    if request.method == 'POST':
        answers = request.form
        for i in range(len(questions)):
            question = questions[i]
            reply = answers.get(f'question{i}')
            if reply == question['answer']:
                prize = prize_money[i]
            else:
                break
    return render_template('game.html', questions=questions, prize_money=prize_money)
@app.route('/scores', methods=['GET', 'POST'])
def scores():
    global prize
    prize = 0
    score = 0  # initialize the score to zero
    if request.method == 'POST':
        answers = request.form
        for i in range(len(questions)):
            question = questions[i]
            reply = answers.get(f'question{i}')
            if reply == question['answer']:
                prize = prize_money[i]
                score += 1  # increment the score for each correct answer
            else:
                break
    return render_template('result.html', questions=questions, prize_money=prize_money, score=score)


@app.route('/result')
def result():
    return render_template('result.html', prize=prize)


if __name__ == '__main__':
    app.run(debug=True)
