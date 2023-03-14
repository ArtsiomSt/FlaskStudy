from flask import Flask, url_for, make_response, render_template, request, Blueprint
from flask_restful import Resource, Api, reqparse
import pickle


apiapp = Blueprint('apiapp', __name__,  template_folder='templates', static_folder='static')
api = Api(apiapp)

class TestSer(Resource):
    def get(self):
        return {'hello': "test"}

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True, help='Need some data to exist')
        with open('dbtest.bin', 'rb') as file:
            goto = pickle.load(file)
            print(goto)
        if goto.get(name,None) is None:
            with open('dbtest.bin', 'wb') as file:
                goto[name] = parser.parse_args().get('data', None)
                print(goto)
                pickle.dump(goto, file)
        return goto

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('data')
        with open('dbtest.bin', 'rb') as file:
            goto = pickle.load(file)
        if goto.get(name, None) is None:
            return {'message': "Use /POST/ to add"}
        with open('dbtest.bin', 'wb') as file:
            goto[name] = parser.parse_args().get('data', None)
            pickle.dump(goto, file)
        return goto


class AddPost(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', 'category', 'tags')
        return {'message':'success'}


# api.add_resource(TestSer, '/h')
api.add_resource(TestSer,'/h/<string:name>')
api.add_resource(AddPost,'/addpost')


if __name__ == "__main__":
    apiapp.run()
