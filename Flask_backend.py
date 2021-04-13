from flask import Flask, render_template,request
import pywhatkit
from datetime import datetime
from threading import Thread
from os import system
from testfolder.config import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'raj'

@app.route('/upload_image', methods=['POST', 'GET'])
def upload_image():
    if request.method=="POST":
        if "image" not in request.files:
            print("No image file")
            return {"status":"failed"}
        system("cd image_bin")
        system(f"git pull f{repo_path}")
        f=request.files['image']
        f.save(secure_filename(f.filename))
        command_list = ["git add --all", 'git commit -m "images added"', f"git push --set-upstream {repo_path} master"]
        for command in command_list:
            system(command)


@app.route('/get_image_list', methods=['POST', 'GET'])
def image_list():
    pass

@app.route('/contact_message', methods=['POST', 'GET'])
def send_contact_message():
    # number , message must be strings and numbr must be country code format "+91xxxxxxxxxx"
    # example call
    # post("http://127.0.0.1:5000/contact_message", {"message": "Hello", "number": "+919629902359"})
    if request.method=="POST":
        try:
            print(request.data)
            number=request.form["number"]
            message=request.form["message"]
            min = int(datetime.now().minute) + 1
            hr = str(int(datetime.now().hour) + (1 if min > 60 else 0))
            min = min % 60
            print(hr, min)
            t=Thread(target=lambda :pywhatkit.sendwhatmsg(phone_no=str(number), message=message, time_min=min, time_hour=int(hr)))
            t.start()
            print("out of loop")
            return {"request_status":"Success"}
        except(Exception) as e:
            print(e)
            return {"request_status": "Failed"}




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
