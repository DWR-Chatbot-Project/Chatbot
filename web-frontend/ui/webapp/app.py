import json

from botRespond import generate_response
from flask import Flask, flash, render_template, request
from predict import predict

app = Flask(__name__)

app.secret_key = 'asdf'

AVERAGE_SQUARE_FOOTAGE = 1827
AVERAGE_PRICE_PER_SQUARE_FOOT = 195
NON_DISCLOSURE_STATES = ['AK', 'ID', 'KS', 'LA', 'MI', 'MO', 'MN', 'MT', 'NM', 'ND', 'TX', 'UT', 'WY']

@app.route('/', methods=['GET', 'POST'])
# def home():
# 	if request.method == 'POST':
# 			form_dict = request.form
# 			try:
# 					if form_dict['state'] in NON_DISCLOSURE_STATES:
# 						flash("Non-disclosure state. No transtractions in this state.")
# 					prediction = predict(form_dict)
# 			except Exception as e:
# 					print(e)
# 					flash('We weren\'t able to make a prediction. Maybe check your input and try again?')
# 					prediction = None
# 	else:
# 			form_dict = {}
# 			prediction = None
			
# 	states = json.load(open('states.json'))
# 	print(form_dict)
# 	return render_template('index.html', states=states, prediction=prediction, form_dict=form_dict)
def home():
    response = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = generate_response(user_input)
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)