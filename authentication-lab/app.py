from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyAOyhswTp176BeU-Xf4OvfnoX0fiN_V-x4",
  "authDomain": "authentictionlub.firebaseapp.com",
  "projectId": "authentictionlub",
  "storageBucket": "authentictionlub.appspot.com",
  "messagingSenderId": "928427556414",
  "appId": "1:928427556414:web:f5d6fc2d29103b29145b6f",
  "databaseURL": "https://authentictionlub-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



#@app.route('/', methods=['GET', 'POST'])
#def signin():
 #   return render_template("signup.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email":request.form["email"], "password":request.form['password']}
            db.child("Users").child(UID).set(user)

            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
#    redirect
    return render_template("signup.html")


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")



#    print("hi")
#   print("how are you")
#    print("i hope you're doing well")
#   return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
  #  error = ""
    if request.method == 'POST':
        try:
            UID = login_session['user']['localId']
            tweet = {"title":request.form['title'], "text":request.form['text'], "uid":UID}
            db.child("Tweets").child(UID).push(tweet)
            return (url_for(add_tweet))
        except:
    #        error = "Authentication failed"
            return render_template("add_tweet.html")
    else:
        return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("tweets.html", tweets = tweets)



   # user_email = ""
    # user_email = login_session["user"]["email"]
   # return render_template("add_tweet.html", email = user_email)





if __name__ == '__main__':
    app.run(debug=True)
