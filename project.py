# Setup needed for the flask framework and connecting to the DB
from flask import (Flask,
                   render_template,
                   url_for,
                   request,
                   redirect,
                   jsonify,
                   flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database import (Base,
                      Categories,
                      subCategories,
                      CategoryItem,
                      User)
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import os
# Test
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder='templates')

# --Flask Setup--#
# loads a json file that retrieves all the
# information needed from the google Oauth 2.0 API,
# such as client_id, client_secret, username etc..
Client_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///categorymenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Google Oauth 0.2 beginning #
# This decorator redirects the user to the login page
@app.route('/login')
def showLogin():
    '''generate a random string of size 32 (in order to deal with tokens)'''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# This method deals with communicating with
# google in order to authenticate the given user
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        '''the login state was not found'''
        response = make_response(json.
                                 dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        print "login state was not found!"
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.
                                 dumps(
                                       '''failed to exchange
                                       authorization code'''), 401)
        response.headers['Content-Type'] = 'application/json'
        print "we couldn't exchange the token :/"
        return response

    # check for valid access token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        print "Error!"
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token did not match!"), 401)
        response.headers['Content-Type'] = 'application/json'
        print "token did not match"
        return response

    if result['issued_to'] != Client_ID:
        response = make_response(json.dumps("Client ID does not match!"), 401)
        response['Content-Type'] = 'application/json'
        print "client_id did not match"
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if (stored_credentials
        is not None and
            gplus_id == stored_gplus_id):
        response = make_response(json.
                                 dumps('''Current user is
                                 already logged in'''), 200)
        print "The access token is " + str(access_token)
        response.headers['Content-Type'] = 'application/json'
        print "user already logged in"
        return response

    # if reached here we have a valid access token
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # get more information of the user from google
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['picture'] = data["picture"]

    if getUserId(login_session['email']) is None:
        userId = createNewUser(login_session)
    else:
        userId = getUserId(login_session['email'])

    login_session['user_id'] = userId

    return "User successfully logged in"


# A funtion that handles the logging out of user.
# this function detectes the user,
# makes sure that it's the intended user and deletes
# the users information from the global variable "Login_session"
@app.route('/gdisconnect')
def logOut():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not logged in'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('User logged out'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Something went wrong :/'), 400)
        response.headers['Content-type'] = 'application/json'
        return response


# google Oauth 2.0 ending
# API endpoints using JSON
@app.route('/catalog/JSON')
def showCategoriesJSON():
    items = session.query(Categories).all()
    return jsonify(Categories=[i.serialize for i in items])


@app.route('/catalog/<int:category>/items/JSON')
def showCategoriesItemsJSON(category):
    items = session.query(subCategories).filter_by(category_id=category).all()
    return jsonify(subCategories=[i.serialize for i in items])


@app.route('/catalog/<int:category>/items/<int:content_id>/content/JSON')
def showContentJSON(category, content_id):
    items = session.query(CategoryItem).filter_by(category_id=content_id)
    return jsonify(CategoryItem=[i.serialize for i in items])


# Website routing and decoraters
# This function shows all the main Category items,
# the Categories are stored in the Database
# in a table called "Categories"
@app.route('/')
@app.route('/catalog')
def showCategories():
    items = session.query(Categories).all()
    return render_template('catalog.html',
                           items=items,
                           login_session=login_session)


# This function leads to the child of the (/catalog) url.
# it contains the subCategories that are relevant to the parent
# url (/catalog) and is also connected to
# the Categories table with a Foreign key.
@app.route('/catalog/<int:category>/items/')
def showCategoryItems(category):
    items = session.query(subCategories).filter_by(category_id=category).all()
    mainItems = session.query(Categories).filter_by(id=category).one()
    return render_template('catalogItem.html',
                           category=category,
                           items=items,
                           mainItems=mainItems)


# This is where the leaf child is shown,
# the items that the user adds and edits.
# this function grabs all the items from the
# (CategoryItem) table and handles user's authorization
# to view content based on the content he added.
@app.route('/catalog/<int:category>/items/<int:content_id>/content')
def showContent(category, content_id):
    # Make sure that there is a user logged in
    if 'username' not in login_session:
        return redirect('/')
    content = session.query(
                            CategoryItem).filter_by(
                            category_id=content_id).all()
    # ParentItems is used to show the parent
    # subCategory of the content choosen by the user
    parentItems = session.query(subCategories).filter_by(id=category).one()
    # Check if there is any content added,
    # if not go through the content and obtain the ID in order
    # to retrieve user's info based on the content.
    # after all that use show the appropriate content
    # that this specific user is authorized to see
    if content != []:
        for i in content:
            creator = getUserInfo(i.user_id)
        if creator.id != login_session['user_id']:
            items = session.query(
                    CategoryItem).filter_by(
                    user_id=creator.id).all()
            return render_template('content.html',
                                   category=category,
                                   content_id=content_id,
                                   items=items,
                                   parentItems=parentItems)

    # if there was items already,
    # retrieve content based on the user id and show it
    tempContent = session.query(
        CategoryItem).filter_by(
        user_id=login_session['user_id']).all()
    # This statement insures that the content
    # shown will be for the logged in user.
    # And also handles any add request given by the user
    # "Since the content list will no longer be empty"
    userContent = [x for x in tempContent if x.category_id == content_id]
    return render_template('content.html',
                           category=category,
                           content_id=content_id,
                           userContent=userContent,
                           parentItems=parentItems)


# This function handles the Add functionality,
# it checks the appropriate subCategory
# to add the content based on the user's choice
@app.route('/catalog/<int:category>/items/<int:content_id>/content/add',
           methods=['GET', 'POST'])
def addContentItem(category, content_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newContent = CategoryItem(name=request.form['contentName'],
                                  description=request.
                                  form['contentDescription'],
                                  category_id=content_id,
                                  user_id=login_session['user_id'])
        session.add(newContent)
        session.commit()
        flash(str(newContent.name) + " Added!")
        return redirect(url_for('showContent',
                                category=category,
                                content_id=content_id,
                                newContent=newContent))
    else:
        return render_template('addContent.html',
                               category=category,
                               content_id=content_id)


# this function edit's the item that the user chooses to edit
@app.route('''/catalog/items/<int:category>/content
           /<int:content_id>/edit/<int:some_id>''',
           methods=['GET', 'POST'])
def editContentItem(category, content_id, some_id):
    if 'username' not in login_session:
        return redirect('/login')
    editItem = session.query(CategoryItem).filter_by(id=some_id).one()
    parentItem = session.query(subCategories).filter_by(id=category).one()

    # this if statement prevent any unauthorized user to edit the item
    if editItem.user_id != login_session['user_id']:
        return """<script>function alertFunction()
        {alert('You are not authorized to edit this item!');}
        </script><body onload='alertFunction()''></body>"""
    if request.method == 'POST':
        editItem.name = request.form['name']
        editItem.description = request.form['desc']
        session.add(editItem)
        session.commit()
        flash("Item edited successfully")
        return redirect(url_for('showContent',
                                category=category,
                                content_id=content_id,
                                editItem=editItem,
                                parentItem=parentItem))
    else:
        return render_template('editCatalog.html',
                               category=category,
                               content_id=content_id,
                               some_id=some_id,
                               editItem=editItem)


# As the name states this function is for
# deleting items based on the user's choice
@app.route('''/catalog/items/<int:category>/content/
           <int:content_id>/delete/<int:item_id>''',
           methods=['GET', 'POST'])
def deleteContentItem(category, content_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    deleteItem = session.query(CategoryItem).filter_by(id=item_id).one()
    # this if statement prevents
    # any unauthorized user
    if deleteItem.user_id != login_session['user_id']:
        return """<script>function alertFunction()
        {alert('You are not authorized to delete this item!');}
        </script><body onload='alertFunction()''></body>"""
    if request.method == 'POST':
        session.delete(deleteItem)
        flash(str(deleteItem.name + " deleted!"))
        session.commit()
        return redirect(url_for('showContent',
                                category=category,
                                content_id=content_id,
                                deleteItem=deleteItem))
    else:
        return render_template('deleteContent.html',
                               category=category,
                               content_id=content_id,
                               item_id=item_id,
                               deleteItem=deleteItem)

# Helper functions for user authorization and navigation.


# Takes user's email and returns user's id
def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        pass


# Takes user's id and return all the user info from the user table
def getUserInfo(user_id):
    userInfo = session.query(User).filter_by(id=user_id).one()
    return userInfo


def createNewUser(login_session):
    user = User(username=login_session['username'],
                email=login_session['email'],
                picture=login_session['picture'])
    session.add(user)
    session.commit()
    userId = session.query(User).filter_by(email=login_session['email']).one()
    return userId.id


if __name__ == '__main__':
    app.secret_key = "Some_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
