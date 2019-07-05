from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml
import os
	
app = Flask(__name__, template_folder='public')
config = yaml.load(open('database.yaml'))
client = MongoClient(config['uri'])
db = client['flask_app']
CORS(app)

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
PUBLIC_PATH = os.path.join(ROOT_PATH, 'angular1')
API_VERSION= 'v1'
API_SLUG= '/api/'


@app.route(API_SLUG+API_VERSION+'/ping', methods=['GET'])
def dummy_endpoint():
    """ Testing endpoint """
    return jsonify({'status': 'success'})

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    return jsonify({'status': '404'}), 404

	
@app.route('/')
def index():
    """ static files serve """
    return send_from_directory(PUBLIC_PATH, 'index.html')
	
@app.route('/<path:path>')
def static_proxy(path):
    """ static folder serve """
    file_name = path.split('/')[-1]
    dir_name = os.path.join(PUBLIC_PATH, '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)
	
	
@app.route(API_SLUG+API_VERSION+'/data', methods=['POST', 'GET'])
def data():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        first_name = body['first_name']
        last_name = body['last_name']

        # db.users.insert_one({
        db['users'].insert_one({
            "first_name": first_name,
            "last_name": last_name
        })
        return jsonify({
			'message': 'Kayıt Başarılı',
            'status': 'success',
            'first_name': first_name,
            'last_name': last_name
        })
    
    # GET all data from database
    if request.method == 'GET':
        allData = db['users'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            first_name = data['first_name']
            last_name = data['last_name']
            dataDict = {
                'id': str(id),
                'first_name': first_name,
                'last_name': last_name
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

@app.route(API_SLUG+API_VERSION+'/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = db['users'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        first_name = data['first_name']
        last_name = data['last_name']
        dataDict = {
            'id': str(id),
            'first_name': first_name,
            'last_name': last_name
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        db['users'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({
		'status': 'success',
		'message': 'Kullanıcı silindi'
		})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        first_name = body['first_name']
        last_name = body['last_name']

        db['users'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "first_name":first_name,
                    "last_name":last_name
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'success', 'message': 'Güncelleme başarılı'})

if __name__ == '__main__':
    app.debug = True
    app.run()
