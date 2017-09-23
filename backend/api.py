from flask import Flask


app = Flask(__name__)



@app.route('/generate_democrat_sentence', methods = ["GET"])
def generate_democrat_sentence():
	return 'This is the democrat speech'

@app.route('/generate_republican_sentence', methods = ["GET"])
def generate_republican_sentence():
	return 'This is the republican speech'


if __name__ == '__main__':
	app.run(host='0.0.0.0')


