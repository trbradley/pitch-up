from flask import url_for, request
from flask.ext.restful import Resource, fields, marshal, reqparse
from server import api, db, session
from server.models.user import User
from server.helpers.sessions import current_user

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}


class SessionsAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username')
        self.reqparse.add_argument('password')
        super(SessionsAPI, self).__init__()

    def get(self):
        if 'user_id' in session:
            return {'user': marshal(current_user(), user_fields)}
        return 'No session set', 200

    def post(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        session.clear()
        if user:
            if User.verify_password(user, args['password']):
                session['user_id'] = user.id
                return {'user_id': user.id, 'message': 'Logged in successfully'}, 201
        return 'Invalid username or password', 400

    def delete(self):
        if 'user_id' in session:
            session.clear()
            return 'Logged out successfully', 200
        return 'You are not logged in', 400

api.add_resource(SessionsAPI, '/sessions', endpoint='sessions')
