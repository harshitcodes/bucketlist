# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response
from functools import wraps
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
auth = HTTPBasicAuth()


def required_roles(*roles):
   def wrapper(f):
      @wraps(f)
      def wrapped(*args, **kwargs):
         if get_current_user_role() not in roles:
            flash('Authentication error, please check your details and try again','error')
            return redirect(url_for('index'))
         return f(*args, **kwargs)
      return wrapped
   return wrapper
 
def get_current_user_role():
   return g.user.role


def create_app(config_name):
    from app.models import Bucketlist, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # @app.route('/register/', methods=['POST'])
    # def new_user():
    #     username = request.data.get('username')
    #     email = request.data.get('email')        
    #     print(username)
    #     password = request.data.get('password')
    #     pwd_hash = pwd_context.encrypt(password)
    #     urole = request.data.get('role')
    #     if username is None or password is None:
    #         abort(400) # missing arguments
    #     if User.query.filter_by(username = username).first() is not None:
    #         abort(400) # existing user
    #     user = User(username = username, urole=urole, email=email, pwd_hash = pwd_hash)
    #     db.session.add(user)
    #     db.session.commit()
    #     return jsonify({ 'username': user.username,
    #                      'urole': user.urole }
    #                 ), 201,{'Location': url_for('get_user', id = user.id, _external = True)}

    # @app.route("/login", methods=["GET", "POST"])
    # def login():
    #     if request.method == 'POST':
    #         username = request.data.get('username')
    #         password = request.data.get('password')
    #         if password == username + "_secret":
    #             id = username.split('user')[1]
    #             user = User(id)
    #             login_user(user)
    #             return redirect(request.args.get("next"))
    #         else:
    #             return abort(401)
    #     else:
    #         return Response('''
    #         <form action="" method="post">
    #             <p><input type=text name=username>
    #             <p><input type=password name=password>
    #             <p><input type=submit value=Login>
    #         </form>
    #         ''')


    @app.route('/customer/<int:id>', methods=['GET'])
    def new_user():
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        pwd_hash = pwd_context.encrypt(password)
        urole = request.data.get('role')
        if username is None or password is None:
            abort(400) # missing arguments
        if User.query.filter_by(username = username).first() is not None:
            abort(400) # existing user
        user = User(username = username, urole=urole, email=email, pwd_hash = pwd_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({ 'username': user.username, 'urole': user.urole }), 
        201, {'Location': url_for('get_user', id = user.id, _external = True)}

    @app.route('/bucketlists/', methods=['POST', 'GET'])    
    def bucketlists():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated

                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    if name:
                        bucketlist = Bucketlist(name=name, created_by=user_id)
                        bucketlist.save()
                        response = jsonify({
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET all the bucketlists created by this user
                    bucketlists = Bucketlist.query.filter_by(created_by=user_id)
                    results = []

                    for bucketlist in bucketlists:
                        obj = {
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': bucketlist.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
        # get the access token from the authorization header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "DELETE":
                    # delete the bucketlist using our delete method
                    bucketlist.delete()
                    return {
                        "message": "bucketlist {} deleted".format(bucketlist.id)
                    }, 200

                elif request.method == 'PUT':
                    # Obtain the new name of the bucketlist from the request data
                    name = str(request.data.get('name', ''))

                    bucketlist.name = name
                    bucketlist.save()

                    response = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    }
                    return make_response(jsonify(response)), 200
                else:
                    # Handle GET request, sending back the bucketlist to the user
                    response = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    }
                    return make_response(jsonify(response)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app