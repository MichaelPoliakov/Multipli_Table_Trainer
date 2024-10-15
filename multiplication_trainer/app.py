from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Define important squares and cubes for SAT
important_squares = {i: i ** 2 for i in range(1, 13)}  # Squares until 12^2
important_cubes = {i: i ** 3 for i in range(1, 5)}  # Cubes until 4^3

# Initialize performance tracker
performance_tracker = {
    (i, j): {'correct': 0, 'incorrect': 0} for i in range(1, 21) for j in range(i, 21)
}
for i in range(1, 14):
    performance_tracker[(i, 'square')] = {'correct': 0, 'incorrect': 0}
for i in range(1, 6):
    performance_tracker[(i, 'cube')] = {'correct': 0, 'incorrect': 0}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_question', methods=['GET'])
def get_question():
    """Generate random multiplication or power question."""
    r = random.random()
    if r < 0.6:
        num1, num2 = random.randint(13, 20), random.randint(1, 20)
    elif r < 0.9:
        num1, num2 = random.randint(7, 12), random.randint(1, 20)
    elif r < 0.95:
        num1, num2 = random.randint(1, 12), random.randint(1, 12)
    else:
        if random.random() < 0.5:
            num1, num2 = random.choice(list(important_squares.keys())), 'square'
        else:
            num1, num2 = random.choice(list(important_cubes.keys())), 'cube'

    return jsonify({'num1': num1, 'num2': num2})


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Check the user's answer and update performance."""
    data = request.json
    num1 = data.get('num1')
    num2 = data.get('num2')
    user_answer = int(data.get('answer'))

    if num2 == 'square':
        correct_answer = important_squares[num1]
        pair = (num1, 'square')
    elif num2 == 'cube':
        correct_answer = important_cubes[num1]
        pair = (num1, 'cube')
    else:
        correct_answer = num1 * num2
        pair = tuple(sorted([num1, num2]))

    if user_answer == correct_answer:
        performance_tracker[pair]['correct'] += 1
        return jsonify({'result': 'correct', 'correct_answer': correct_answer})
    else:
        performance_tracker[pair]['incorrect'] += 1
        return jsonify({'result': 'incorrect', 'correct_answer': correct_answer})


@app.route('/performance', methods=['GET'])
def performance():
    """Show performance stats."""
    performance_data = [{'pair': pair, 'correct': data['correct'], 'incorrect': data['incorrect']}
                        for pair, data in performance_tracker.items()
                        if data['correct'] + data['incorrect'] > 0]
    return jsonify(performance_data)


if __name__ == '__main__':
    app.run(debug=True)