
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/getalluser')
def get_all_user():
	from mydatabase import fire
	path = 'apigee'

	json_data = fire.call(path)
	return jsonify(json_data)


@app.route('/getuserbyid/<unique_ID>')
def get_user_by_id(unique_ID):

	from mydatabase import fire
	path = f'apigee/{unique_ID}'

	json_data = fire.call(path)
	return jsonify(json_data)


@app.route('/getuserbyid')
def get_user_by_id_form():

	from mydatabase import fire
	path = 'apigee'

	json_data = fire.call(path)
	lst = list(json_data.keys())

	return render_template('getuserbyid.html',
							lst=lst,
						)
		

@app.route('/postrow')
def post_row():
	from mydatabase import fire
	import random

	ran = random.randint(1000, 9999)
	data = {
		'unique_ID' : ran,
		'first name' : f'first_name_{ran}',
		'last name' : f'last_name_{ran}',
		'age' : f'age_{ran}',
	}

	path = f'apigee/{ran}'
	fire.send(path, data)
	return render_template('posted.html', data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
					 e='Page not Found'), 404


if __name__ == '__main__':
	app.run(debug = True)
