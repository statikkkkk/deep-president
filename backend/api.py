from flask import Flask


app = Flask(__name__)



@app.route('/generate_democrat_sentence', methods = ["GET"])
def generate_democrat_sentence():
	return 'This is the democrat speech'

@app.route('/generate_republican_sentence', methods = ["GET"])
def generate_republican_sentence():
	return ' And just so you know from the Secret Service, there are not too many people outside protesting, OK. That I can tell you. A lot of people in here, a lot of people pouring right now. They can get them in. Whatever you can do, fire marshals, we will appreciate it. And I want to thank our great vice president, Mike Pence, for the introduction. As well as my friend Dr. Ben Carson. And thank you to a very, very special man, Franklin Graham, Reverend Franklin Graham, for leading us in prayer. And thank you too Alveda King, the niece of the great Dr. Martin Luther King. It really shows you that America is indeed a nation of faith, we know that. Well, I\'m thrilled to be back in Phoenix, in the great state of Arizona. With so many thousands of hard-working American patriots. You know I\'d love it if the cameras could show this crowd, because it is rather incredible. It is incredible. It is incredible. As everybody here remembers, this was the scene of my first rally speech, right? The crowds were so big, almost as big as tonight, that the people said right at the beginning, you know, there\'s something special happening here. And we went to center stage almost from day one in the debates. We love those debates.'


if __name__ == '__main__':
	app.run(host='0.0.0.0')


