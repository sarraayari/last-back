from flask import Flask,send_file ,flash,request,jsonify,send_from_directory,make_response
from pymongo import MongoClient
from flask_cors import CORS , cross_origin
import os
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

app = Flask(__name__)
#app.config['UPLOAD_DIRECTORY'] = 'C:\\Users\\sarra\\Junior-Project\\server\\public\\uploads\\'
app.config['UPLOAD_DIRECTORY'] = 'https://last-back-here.onrender.com/public/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'b\x85\xc9\x99\xc3\xb1\x81\x86\x96\xf3t\x91\xbb\rQ\xce\x18$\xd5\xa8\x10w$sR'
app.config["MONGO_URI"]="mongodb+srv://sarra:1234@cluster0.p6dxnn8.mongodb.net/?retryWrites=true&w=majority"
app.config['CONTENT_TYPE']='Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS']= True ###
@app.after_request
def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '86400'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Length'
    return response
CORS(app)
#cors=CORS(app ,resources={r"*": {"origins": 'https://last-front.netlify.app./*'}},supports_credentials=True)

client = MongoClient("mongodb+srv://sarra:1234@cluster0.p6dxnn8.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('Uploads')

# @app.route('/')
# #@cross_origin(origin='*', allow_headers=['Content-Type', 'Authorization'])
# def entry_point():
#     return ('home.html')#######

# @cross_origin(origin='https://last-front.netlify.app/*', allow_headers=['Content-Type', 'Authorization'])
# def add_header(response):
#     response.headers['Access-Control-Allow-Origin'] = ['52*']
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
#     response.headers['Access-Control-Allow-Headers'] = {'access-control-allow-origin': '*'}
#     return ('response')


# @app.errorhandler(RequestEntityTooLarge)
# def handle_file_size_exceeded(error):
#     return jsonify({"error": "File size exceeded maximum limit of 5MB"}), 400
#     #############################
# @app.route('/upload', methods=['POST'])
# # @cross_origin(origins='https://last-front.netlify.app/AbstractSubmission', allow_headers=['Content-Type', 'Authorization'])
# def upload():
#     if request.method == 'POST':
#         if (request.files):
#             file=request.files['file']
#             if file.filename == '':
#                 flash('No selected file')
#             if file:
#                 filename=secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_DIRECTORY'],filename))
#                 return 'file uploaded'

@app.after_request
@app.route('/Upload', methods=['POST', 'GET'])
# @cross_origin(origins=['https://last-front.netlify.app/AbstractSubmission','https://last-front.netlify.app/TTable'], allow_headers=['Content-Type', 'Authorization'])
def Upload():
    if request.method == 'POST':
        FirstName=request.get_json()['FirstName']
        LastName=request.get_json()['LastName']
        Email=request.get_json()['Email']
        db['Uploads'].insert_one({
            "FirstName": FirstName,
            "LastName": LastName,
            "Email":Email,
            })
        return ('added to data base')
    if request.method == 'GET':
        allData = db['Uploads'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            FirstName = data['FirstName']
            LastName = data['LastName']
            Email = data['Email']
            dataDict = {
                '_id': str(id),
                'FirstName': FirstName,
                'LastName': LastName,
                'Email': Email
            }
            dataJson.append(dataDict)
        return dataJson


# @app.after_request
# @app.route('/download/<path:filename>',methods=['GET'])
# # @cross_origin(origin='https://last-front.netlify.app/TTable', allow_headers=['Content-Type', 'Authorization'])
# def download_file(filename):
#     filename='saeeaajjjjjjjjjjjjjjjjj.pdf'
#     #binairy=send_file(app.config['UPLOAD_DIRECTORY']+'/'+filename, as_attachment=True)
#     binairy=send_from_directory(directory=app.config['UPLOAD_DIRECTORY'],path=filename,as_attachment=True)
#     response=make_response(binairy)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers ['Content-Type'] = 'application/pdf'
#     response.headers ['Content-Disposition']= \
#                         'inline;filename=%s.pdf' % 'yourfilename'
#     response.headers ['CORS_SUPPORTS_CREDENTIALS'] =True
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     response.headers['Access-Control-Expose-Headers'] = 'Content-Length'

#     return response
if __name__ == "__main__":
    app.run(debug=True)



