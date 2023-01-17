from flask import Flask,send_from_directory,flash,render_template,request
from pymongo import MongoClient
from flask_cors import CORS , cross_origin
import os
from flask import make_response
from flask import send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'C:\\Users\\sarra\\Junior-Project\\server\\uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'b\x85\xc9\x99\xc3\xb1\x81\x86\x96\xf3t\x91\xbb\rQ\xce\x18$\xd5\xa8\x10w$sR'
app.config["MONGO_URI"]="mongodb+srv://sarra:1234@cluster0.p6dxnn8.mongodb.net/?retryWrites=true&w=majority"
app.config['CONTENT_TYPE']='Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS']= True
app.config['CORS_RESOURCES']= {r"/manifest.json": {"origins":["*","https://icsa2023.netlify.app", "https://icsa2023-m1ct.onrender.com","https://*.netlify.app"] }}

cors=CORS(app , resources={r"/manifest.json": {"origins":"*"}})

client = MongoClient("mongodb+srv://sarra:1234@cluster0.p6dxnn8.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('Uploads')

@app.route('/')
@cross_origin(origin='https://icsa2023.netlify.app', allow_headers=['Content-Type', 'Authorization'])
def entry_point():

    return render_template('home.html')

@app.route('/upload', methods=['POST'])
@cross_origin(origin='*', allow_headers=['Content-Type', 'Authorization'])
def upload():
     if request.method == 'POST':
        if (request.files):
            file=request.files['file']
            if file.filename == '':
                flash('No selected file')
            if file:
                try:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))
                    return ({"file":"uploaded"})
                except RequestEntityTooLarge :
                    return  'File too large'
            else:
                return ('error no file detected')

@app.route('/Upload', methods=['POST', 'GET'])
@cross_origin(origin='https://icsa2023.netlify.app', allow_headers=['Content-Type', 'Authorization'])
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
        return ('here')

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
        print(dataJson)
        return dataJson

@app.route('/download/<path:filename>',methods=['GET'])
@cross_origin(origin='https://icsa2023.netlify.app', allow_headers=['Content-Type', 'Authorization'])
def download_file(filename):
    binary_pdf = send_from_directory(directory=app.config['UPLOAD_DIRECTORY'],path=filename)
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
                'yourfilename'
    return response

if __name__ == "__main__":
    app.run(debug=True)



