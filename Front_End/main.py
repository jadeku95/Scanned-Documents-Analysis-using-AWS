import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import boto3, botocore
import time
import fitz
import csv
import webbrowser


app=Flask(__name__)


app.config['S3_BUCKET'] = "trends-marketplace"
app.config['S3_KEY'] = "xxx"
app.config['S3_SECRET'] = "xxx"
app.config['S3_LOCATION'] = 'xxx')

session = boto3.Session(
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)

# s3 = boto3.client(
#    "s3",
#    aws_access_key_id=app.config['S3_KEY'],
#    aws_secret_access_key=app.config['S3_SECRET']
# )

s3 = session.resource('s3')

def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
OUTPUT_FOLDER = os.path.join(path, 'output')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
if not os.path.isdir(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


ALLOWED_EXTENSIONS = set(['pdf'])



def highlight_text(pdf_name, csv_name):
    
    print('highlight function started')

    # Open the pdf
    doc = fitz.open('uploads/{}'.format(pdf_name))

    #adding highlights
    with open('downloads/{}'.format(csv_name), 'r') as file:
        csvreader = csv.reader(file)
        one = True
        
        for row in csvreader:
            if one:
                one = False
            else:
                print(row)
                x1 = float(row[1])
                y1 = float(row[2])
                x2 = float(row[3])
                y2 = float(row[4])
                page = int(row[5])-1
                width  = doc[page].rect.width
                height = doc[page].rect.height
                doc[page].draw_rect([x1*width,y1*height,x2*width,y2*height],  color = (0, 1, 0), width = 2)

    #saving pdf
    doc.save('output/{}'.format(pdf_name))
    print('highlight function completed')


def download_file_s3(file_name):
    print ('download function started csv/{}'.format(file_name))
    try:
        s3.Bucket(app.config['S3_BUCKET']).download_file('csv/{}'.format(file_name),'downloads/{}'.format(file_name))
        # first_dir = s3.Bucket(app.config['S3_BUCKET']).objects.filter(Prefix="csv")
        # result = s3.Bucket(app.config['S3_BUCKET']).download_file('downloads/{}'.format(file_name),'csv/{}'.format(file_name))
    except:
        time.sleep(10)
        download_file_s3(file_name)
        
    print ('download tried')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('/upload.html')

@app.route('/pattern.png')
def background_image():
    return 

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        success = False

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.filename = secure_filename(file.filename)
            
            try:
                # s3.upload_fileobj(
                #     file,
                #     app.config['S3_BUCKET'],
                #     'files/{}'.format(file.filename),
                #     ExtraArgs={
                #         "ContentType": file.content_type
                #     }
                # )
                result = s3.Bucket(app.config['S3_BUCKET']).upload_file('uploads/{}'.format(filename),'files/{}'.format(file.filename))
                print(result)

                csv_filename = filename[:-3]+"csv" 
                download_file_s3(csv_filename)

                highlight_text(filename, csv_filename)
                flash('Changes Detected')


            except Exception as e:
                print("Something Happened: ", e)
                return e

            webbrowser.open_new_tab(app.config['OUTPUT_FOLDER']+'/'+str(file.filename))
            
            return redirect('/')

        if success:
            print(csv_filename)
            download_file_s3(csv_filename)  

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 5000, debug = False)
