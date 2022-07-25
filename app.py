
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/getalluser', methods = ['GET', 'POST'])
def getalluser():
	if(request.method == 'GET'):
		from mydatabase import fire
		path = 'apigee'

		json_data = fire.call(path)
		return jsonify(json_data)


if __name__ == '__main__':
	app.run(debug = True)
