from flask import session
from functools import wraps

#---------------------------------------------------#
#   Checks if user is authenticated
#---------------------------------------------------#
def authenticated():
    # If there is an Id in session, returns true
    return ('user' in session)

#---------------------------------------------------#
#   Logs user by google profile data
#---------------------------------------------------#
def authenticate_by_google(user):
    #Variables de sesion
    session['user'] = user
    # session['name'] = user['name']
    # session['email'] = user['email']
    # session['picture'] = user['picture']
    return True
