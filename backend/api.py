from flask import Flask


app = Flask(__name__)



@app.route('/generate_sentence', methods = ["GET"])
def generate_democrat_sentence():
	return 'Put all the money in the pot and then everybody can take 2 dollars.'

def generate_republican_sentence():
	return 'Build a wall and kick out all the brown people.'


if __name__ == '__main__':
	app.run(host='0.0.0.0')


