from flask import Flask


app = Flask(__name__)



@app.route('/generate_sentence', methods = ["GET"])
def generate_sentence():
	return 'And just so you know from the Secret Service, there are not too many people outside protesting, OK. That I can tell you. A lot of people in here, a lot of people pouring right now. They can get them in. Whatever you can do, fire marshals, we will appreciate it. And I want to thank our great vice president, Mike Pence, for the introduction. As well as my friend Dr. Ben Carson. And thank you to a very, very special man, Franklin Graham, Reverend Franklin Graham, for leading us in prayer.'


if __name__ == '__main__':
	app.run(host='0.0.0.0')


