from flask import Flask, session, render_template, redirect, url_for
# Authentication helper
from flask_app.helpers import auth
# Google auth with OAuth
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
# OS: For env accessing
import os

#---------------------------------------------------#
#   App Setup
#---------------------------------------------------#
app = Flask(__name__)

#---------------------------------------------------#
#   Session setup
#---------------------------------------------------#
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'

#---------------------------------------
#   OAuth setup
#---------------------------------------
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

#---------------------------------------
#   Home route
#---------------------------------------
@app.route('/')
def home():
    if auth.authenticated():
        return render_template('home.html', user=session['user'])
    else:
        return render_template('welcome.html')

#---------------------------------------
#   Google login page
#---------------------------------------
@app.route('/google_login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

#---------------------------------------
#   Google authorization
#---------------------------------------
@app.route('/authorize')
def authorize():
    # Create google oauth client
    google = oauth.create_client('google')
    # Google access token
    google.authorize_access_token()
    # User info response
    response = google.get('userinfo')
    user_info = response.json()
    # User authentication
    auth.authenticate_by_google(user_info)
    # Redirection
    return redirect('/')

#---------------------------------------
#   Logout route
#---------------------------------------
@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

#---------------------------------------
#   404 Handle
#---------------------------------------
@app.errorhandler(404)
def error404(error):
    return render_template('error404.html')
