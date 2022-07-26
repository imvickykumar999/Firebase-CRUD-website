
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

	if json_data == None:
		return jsonify({
			'error' : {
				'description' : f'Unique ID {unique_ID} not Found in Database.'
			}
		})
	else:
		return jsonify(json_data)


@app.route('/getuserbyid')
def get_user_by_id_select():

	from mydatabase import fire
	path = 'apigee'
	json_data = fire.call(path)

	if json_data == None:
		lst = []
	else:
		lst = list(json_data.keys())

	return render_template('getuserbyid.html',
							lst=lst,
						)
		

@app.route('/deleteuserbyid/<unique_ID>')
def delete_user_by_id(unique_ID):

	from mydatabase import fire
	path = f'apigee/{unique_ID}'
	data = {
		'unique_ID' : unique_ID,
		'first name' : f'first_name_{unique_ID}',
		'last name' : f'last_name_{unique_ID}',
		'age' : f'age_{unique_ID}',
	}
	json_data = fire.call(path)

	if json_data != None:
		fire.send(path)
		
		return jsonify({
			'deleted' : {
				'data' : data,
				'description' : f'Unique ID {unique_ID} has been Deleted from Database.'
			}
		})

	else:
		return jsonify({
			'error' : {
				'message' : "Couldn't Delete Data.",
				'description' : f'Unique ID {unique_ID} Not Found in Database.',
			}
		})


@app.route('/deleteuserbyid')
def delete_user_by_id_select():

	from mydatabase import fire
	path = 'apigee'
	json_data = fire.call(path)

	if json_data == None:
		lst = []
	else:
		lst = list(json_data.keys())

	return render_template('deleteuserbyid.html',
							lst=lst,
						)
		


@app.route('/createuser')
def create_user():
	return render_template('createuser.html',
							submitted = False,
						)


@app.route('/createduser', methods=['GET', 'POST'])
def created_user():
	if request.method == 'POST':
		from mydatabase import fire
		import random 

		fname = request.form['fname']
		lname = request.form['lname']
		age   = request.form['age']
		ran   = random.randint(1000, 9999)

		print(fname, lname, age)
		data = {
			'unique_ID'  : ran,
			'first name' : fname if fname != '' else f'fname_{ran}',
			'last name'  : lname if lname != '' else f'lname_{ran}',
			'age'        : age   if age   != '' else f'age_{ran}',
		}

		path = f'apigee/{ran}'
		fire.send(path, data)
		return render_template('createuser.html',
							submitted = True,
							data=data
							)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
					 e='Page not Found'), 404


if __name__ == '__main__':
	app.run(debug = True)
