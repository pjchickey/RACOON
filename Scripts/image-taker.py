# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import time
from pathlib import Path
import os
import subprocess
import re
import fnmatch

CAMERA_RESOLUTION = [600, 600]

RE_CURRENT_BRANCH = re.compile(
    r"^[*]"       # Leading "*" denotes the current branch from "git branch" 
    "\s{1}"       # Single space after "*"
    "(.*)",       # Group 1: current branch name 
    re.MULTILINE
)

categories = [
    #Recycleable
    "Paper-Newspapers",
    "Paper-Office",
    "Paper-Magazines",
    "Paper-Junk_Mail",
    "Plastic-Bottles",
    "Plastic-Other",
    "Cardboard-Boxes",
    "Cardboard-Other",
    "Steel_and_Tin",
    "Aluminum",
    "Glass",
    #NonRecycleable
    "Plastic_Bags",
    "Plastic_Wrap",
    "No_6_Plastics",
    "Plasticware",
    "Plastic_Straws",
    "Drink_Cartons",
    "Paper_Cups",
    "Food_Waste",
    "Styrofoam",
    "Pizza_Boxes",
    "Other"
]

HOME=f"""\
<html>
<head>
<title>RACOON Image Taker</title>
</head>
<body>
<button onclick="document.location='index.html'">Home</button>
<center><h1>Racoon Image Taker</h1></center>
<center><img src="stream.mjpg" width="{CAMERA_RESOLUTION[0]}" height="{CAMERA_RESOLUTION[1]}"></center>
<br>
<center><button onclick="document.location='take-picture.html'">Take Picture</button></center>
</body>
</html>
"""

SUCCESS = """\
<html>
<head>
<title>Success!</title>
</head>
<body>
<center><h1>Photo Saved</h1></center>
<center><button onclick="document.location='index.html'">Home</button></center>
</body>
</html>
"""

global error_text
global data
error_text = ""
data = ["", "", ""]


def get_current_branch():

    out = subprocess.check_output(["git", "branch"]).decode('utf-8')

    current_branch_full_match = re.search(RE_CURRENT_BRANCH, out)
    current_branch = current_branch_full_match.group(1)
    return current_branch

def upload_image(short_img_path):
    commit_info = short_img_path.split("/")
    print(subprocess.check_output(["git", "pull"]).decode('utf-8'))
    print(subprocess.check_output(["git", "add", "-A"]).decode('utf-8'))
    print(subprocess.check_output(["git", "commit", "-a", "-m", f"Upload {commit_info[1]} to {commit_info[0]}"]).decode('utf-8'))
    print(subprocess.check_output(["git", "push"]))


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    global camera
    global output
    global error_text
    global data
    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = HOME.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/take-picture.html':
            checked_cats = [""] * 22
            if data[2] != "":
                checked_cats[int(data[2])] = " checked"
            PICTURE=f"""\
            <html>
            <head>
            <title>Take Picture</title>
            </head>
            <body>
            <button onclick="document.location='index.html'">Home</button>
            <center><h1>Racoon Image Taker</h1></center>
            <center><p>Note: Please wait until Image Loads to Submit</p></center>
            <center><img src="img.png" width="{CAMERA_RESOLUTION[0]}" height="{CAMERA_RESOLUTION[1]}"></center>
            <center><button onclick="document.location='index.html'">Retake</button></center>
            <center><h2>Specify Image Info</h3></center>
            <center><form action="/take-picture.html" method="post" id="dataForm">
                <input type="button" onclick="myFunction()" value="Clear Values"><br><br>
                Object Name (ex: pepsi can): <input type="text" id="myText" name="desc" value="{data[0]}"><br>
                Weight (Lbs) (Ex: 1.5): <input type="text" id="weightText" name="weight" value="{data[1]}"><br>
                <h4>Recycleable</h4>
                {categories[0]}: <input type="radio" name="category" value="0"{checked_cats[0]}><br>
                {categories[1]}: <input type="radio" name="category" value="1"{checked_cats[1]}><br>
                {categories[2]}: <input type="radio" name="category" value="2"{checked_cats[2]}><br>
                {categories[3]}: <input type="radio" name="category" value="3"{checked_cats[3]}><br>
                {categories[4]}: <input type="radio" name="category" value="4"{checked_cats[4]}><br>
                {categories[5]}: <input type="radio" name="category" value="5"{checked_cats[5]}><br>
                {categories[6]}: <input type="radio" name="category" value="6"{checked_cats[6]}><br>
                {categories[7]}: <input type="radio" name="category" value="7"{checked_cats[7]}><br>
                {categories[8]}: <input type="radio" name="category" value="8"{checked_cats[8]}><br>
                {categories[9]}: <input type="radio" name="category" value="9"{checked_cats[9]}><br>
                {categories[10]}: <input type="radio" name="category" value="10"{checked_cats[10]}><br>
                <h4>NonRecycleable</h4>
                {categories[11]}: <input type="radio" name="category" value="11"{checked_cats[11]}><br>
                {categories[12]}: <input type="radio" name="category" value="12"{checked_cats[12]}><br>
                {categories[13]}: <input type="radio" name="category" value="13"{checked_cats[13]}><br>
                {categories[14]}: <input type="radio" name="category" value="14"{checked_cats[14]}><br>
                {categories[15]}: <input type="radio" name="category" value="15"{checked_cats[15]}><br>
                {categories[16]}: <input type="radio" name="category" value="16"{checked_cats[16]}><br>
                {categories[17]}: <input type="radio" name="category" value="17"{checked_cats[17]}><br>
                {categories[18]}: <input type="radio" name="category" value="18"{checked_cats[18]}><br>
                {categories[19]}: <input type="radio" name="category" value="19"{checked_cats[19]}><br>
                {categories[20]}: <input type="radio" name="category" value="20"{checked_cats[20]}><br>
                {categories[21]}: <input type="radio" name="category" value="21"{checked_cats[21]}><br>
                <br>
                <input type="submit" name="submit" value="Submit">
            </form></center>
            <script>
            function myFunction() {{
                document.getElementById("dataForm").reset();
            }}
            </script>

            </body>
            </html>
            """
            content = PICTURE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/success.html':
            content = SUCCESS.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/error.html':
            ERROR = f"""\
            <html>
            <head>
            <title>Error</title>
            </head>
            <body>
            <center><h1>Well Shit.</h1></center>
            <p>{error_text}</p><br>
            <br>
            <br>
            <br>
            <p>Image Not Saved. Please Retake.</p>
            <center><button onclick="document.location='index.html'">Home</button></center>
            </body>
            </html>
            """
            content = ERROR.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/img.png':
            camera.stop_recording()
            #camera.resolution = (1920,1080)
            time.sleep(2)   # Camera warm-up time
            camera.capture(output, 'png')
            camera.capture("img.png")
            frame = output.frame
            self.send_response(200)
            self.send_header('Content-Type', 'img/png')
            self.send_header('Content-Length', len(frame))
            self.end_headers()
            self.wfile.write(frame)
            camera.resolution=(CAMERA_RESOLUTION[0],CAMERA_RESOLUTION[1])
            camera.start_recording(output, format='mjpeg')
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()
    
    def do_POST(self):
        """ do_POST() can be tested using curl command 
            'curl -d "submit=On" http://server-ip-address:port' 
        """
        global error_text
        global data
        dir_made = False
        content_length = int(self.headers['Content-Length'])    # Get the size of data
        post_data = bytes.decode(self.rfile.read(content_length))   # Get the data
        data = post_data.split("&")[:3]
        data[0] = data[0].replace("desc=", "").lower().replace("+", "").replace("-", "").replace("_", "")
        data[1] = data[1].replace("weight=", "").lower().replace("+", "").replace("-", "").replace("_", "")
        weight = data[1].replace(".", "_")
        data[2] = data[2].replace("category=", "")
        category = categories[int(data[2])]
        folder_path= "/home/pi/RACOON/Images/" + str(category)   #Folder category
        if not(os.path.isdir(folder_path)):
            os.mkdir(folder_path)
            dir_made = True
        img_path = folder_path + f"/{data[0]}"
        dirs = os.listdir(folder_path)
        try:
            image_indx = max([int(x.split("--")[0].replace(f"{data[0]}", "")) for x in fnmatch.filter(dirs, f"{data[0]}[0123456789]*.png")]) + 1 #Get number for filename that isn't taken
        except ValueError:
            image_indx = 0
        img_path += f"{str(image_indx)}--{str(weight)}.png" #Add img no. and weight to filename
        Path("/home/pi/RACOON/Scripts/img.png").rename(img_path)
        try:
            out = upload_image(img_path.replace("/home/pi/RACOON/Images/", ""))
            self._redirect('/success.html')
        except subprocess.CalledProcessError as e:
            error_text = e.output.decode('utf-8')
            os.remove(img_path)
            if dir_made:
                os.rmdir(folder_path)
            self._redirect('/error.html')
        

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if get_current_branch() != "main":
    print(get_current_branch())
    raise OSError("Not on Main branch! Commit any unsaved changes and switch to main using git checkout main and run this program again :)")

global camera
global output
camera = picamera.PiCamera(resolution=f'{CAMERA_RESOLUTION[0]}x{CAMERA_RESOLUTION[1]}', framerate=24)
camera.awb_mode = 'off'
rg, bg = (3.5, 0.9)
camera.awb_gains = (rg, bg)
camera.rotation = 90
output = StreamingOutput()
camera.start_recording(output, format='mjpeg')
try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    camera.stop_recording()
