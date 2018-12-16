from flask import request, jsonify, render_template
from flask.helpers import send_file
from PIL import Image
from io import BytesIO


PEOPLE_FOLDER = os.path.join('static', 'people_photo')
CSS_FOLDER = os.path.join('static', 'css')


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['UPLOAD_FOLDER2'] = CSS_FOLDER

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

# get data from db
db = mysql.connector.connect(user='root', password='CYWe!k@WC2CF§%~7',
                              host='localhost',
                              database='planeten')

sql1='select * from fragen'
cursor=db.cursor(dictionary=True)
cursor.execute(sql1)
data=cursor.fetchall()

print(data)

full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg')
test10=os.path.join(app.config['UPLOAD_FOLDER2'], 'button2.css')
print(test10)
@app.route('/', methods=['GET'])
def home():
    if 'id' in request.args:
        id = int(request.args['id'])
        score = int(request.args['score'])
        return render_template('Richi.html', Frage=data[id]['Frage'], Antwort=data[id]['Antwort'],
                               Option1=data[id]['Option1'], Option2=data[id]['Option2'], Option3=data[id]['Option3'],
                               Bild=full_filename, score=score, durchgang=id, CSS=test10)
    else:
        return render_template('Richi.html', Frage=data[0]['Frage'], Antwort=data[0]['Antwort'] ,Option1=data[0]['Option1'], Option2=data[0]['Option2'], Option3=data[0]['Option3'], Bild=full_filename, score=0, durchgang=0,CSS=test10)


@app.route('/api/v1/resources/fragen/all', methods=['GET'])
def api_all():
    return jsonify(data)


@app.route('/api/v1/resources/fragen', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for Zeile in data[:,1:]:
        if Zeile['ID'] == id:
            results.append(Zeile)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


@app.route('/final', methods=['GET'])
def final():
    if 'score' in request.args:
        score = int(request.args['score'])
        return render_template('final.html', score=score,CSS=test10)

    else:
        return "Error: No score field provided. Please specify a score."

app.run()
