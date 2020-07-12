from flask import session
from functools import wraps

#---------------------------------------------------#
#   Checks if user is authenticated
#---------------------------------------------------#
def authenticated():
    # If there is an user in session, returns true
    return ('user' in session)

#---------------------------------------------------#
#   Logs user by google profile data
#---------------------------------------------------#
def authenticate_by_google(user):
    #Session variables
    session['user'] = user
    return True
