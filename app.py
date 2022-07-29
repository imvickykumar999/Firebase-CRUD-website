
from flask import Flask, jsonify, request, render_template
import ast, json, urllib.request as ur
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


@app.route("/ipynb")
def ipynb():
    return render_template("ipynb.html", infolist = [["Output"]])

@app.route('/converted_ipynb', methods=['POST'])
def convert_ipynb():

    def ipynbinfo(info, file_name):
        def call(file_name):

            if 'http' == file_name[0:4]:
                print('\nPlease WAIT, content is loading from URL...\n')
                su = ur.urlopen(str(file_name)).read().decode('ascii')

            elif '{' == file_name[0]:
                su = file_name

            elif '\\' or '/' in file_name:
                su = open(file_name).read()

            try:
                y = json.loads(str(su))
            except:
                y = su
            return ast.literal_eval(str(y))

        def recdict(d):
            try:
                box.append(d[info])
            except Exception as e:
                pass

            for i in list(d.values()):
                if type(i) == list:
                    for j in i:

                        if type(j) == dict:
                            recdict(j)

                if type(i) == dict:
                    recdict(i)
            return box
        return recdict(call(file_name))

    n, box = 130, []
    file_name = request.form['ipynb']

    if file_name == '':
        file_name = 'https://raw.githubusercontent.com/imvickykumar999/vixtor/master/vixtor.ipynb'

    infolist = ipynbinfo('source', file_name)
    # for i in infolist:
    #     for j in i:
    #         print(j)
    #     print('='*n, end='\n\n')

    return render_template('ipynb.html', infolist = infolist, range = range(40))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
					 e='Page not Found'), 404


if __name__ == '__main__':
	app.run(debug = True)
