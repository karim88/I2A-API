from flask import Flask, request
from flask_cors import CORS
from helpers.helpers import convertImageToAscii

app = Flask(__name__)
CORS(app)


# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@%#*+=-:. '


# Routes
@app.route("/api")
def default():
    return {
        "image": "",
        "ascii": "",
        "status": "200"
    }


@app.route("/api/convert", methods=["GET", "POST"])
def convertToAscii():
    try:
        if request.method == "GET":
            imgFile = request.args.get('file', '')
            scale = request.args.get('scale', '0.43')
            cols = request.args.get('cols', '80')
            moreLevels = request.args.get('moreLevels', '')
        elif request.method == "POST":
            imgFile = request.files["file"]
            scale = request.form["scale"] if request.form.get(
                "scale") else '0.43'
            cols = request.form["cols"] if request.form.get("cols") else '80'
            moreLevels = request.form["moreLevels"] if request.form.get(
                "moreLevels") else ''
        else:
            return {
                "ascii": "",
                "message": "Please use only 'POST' or 'GET' methods to send data.",
                "status": "400"
            }
        # set output file
        outFile = 'out.txt'
        # set scale default as 0.43 which suits
        # a Courier font

        print('generating ASCII art...')
        # convert image to ascii txt
        aimg = convertImageToAscii(imgFile, cols, scale, moreLevels, gscale1, gscale2)
        if aimg == None:
            return {
            "ascii": "",
            "message": "Image too small for specified cols!",
            "status": "500"
        }
        # open file
        with open(outFile, 'w') as f:
            # write to file
            for row in aimg:
                f.write(row + '\n')

            print("ASCII art written to %s" % outFile)
    except BaseException as err:
        return {
            "ascii": "",
            "message": err,
            "status": "500"
        }
    return {
        "ascii": aimg,
        "message": "Your Image is ready.",
        "status": "200"
    }
