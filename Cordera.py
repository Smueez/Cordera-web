import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, render_template, request, redirect, url_for
import uuid
from datetime import date, datetime

# init flask app

app = Flask(__name__)
# Use the application default credentials
cred = credentials.Certificate('G:\cookie tech\Cordera py\chordera-e5018-firebase-adminsdk-yuuwi-9dde0cce45.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'chordera-e5018',
    'storageBucket': 'chordera-e5018.appspot.com'
})

db = firestore.client()
# bucket = storage.bucket()
print('running...')


def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list


collectionList = []


@app.route("/")
def index():
    collection = []
    collectionList.clear()
    doc_ref = db.collection('collections')

    docs = doc_ref.stream()
    for doc in docs:
        collectionElements = {doc.id: doc.to_dict()}
        collection.append(collectionElements)

    for doc in collection:
        keyx = getList(doc)
        for key in keyx:
            listElement = {'id': key, 'value': doc[key]['collection_name']}
            collectionList.append(listElement)
    #for doc in collectionList:
        #print(doc['id'])

    return render_template("home.html", collection=collectionList)


@app.route("/data", methods=['POST'])
def valueFromHTML():
    id = uuid.uuid1()
    #print(id.hex)
    if request.method == "POST":
        if request.form.get("submit"):
            songname = request.form["songName"]
            artistName = request.form["artistName"]
            collection = request.form["collection"]
            songDuration = request.form["songDuration"]
            songChords = request.form["songChords"]
            youtubeLink = request.form["youtubeLink"]
            keyWords = request.form["keyWords"]
            imageUpload = request.form["imageUpload"]

            doc_ref = db.collection('song_data').document(id.hex)
            doc_ref.set({
                'data': songChords
            })
            for names in collectionList:
                if names["id"] == collection:
                    genre = names["value"]
                    break
            #print(genre)
            songID = uuid.uuid1()
            doc_ref = db.collection('songs').document(songID.hex)
            doc_ref.set({
                'artist_name': artistName,
                'collections': collection,
                'download_count': 0,
                'genre': genre,
                'image_url': imageUpload,
                'search_keyword': keyWords,
                'song_data': id.hex,
                'song_duration': songDuration,
                'song_name': songname,
                'update_date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')+' '+date.today().strftime('%B %d, %Y'),
                'views': 0,
                'youtube_id': youtubeLink
            })
            doc_ref = db.collection('collections').document(collection)
            doc_ref.set({
                'song_id': songID.hex
            })

            #print("collection: " + collection)
            return "Upload completed!"

        if request.form.get("submitCollection"):
            print("collection adding...")
            id = uuid.uuid1()
            collectionName = request.form["CollectionName"]
            collectionImage = request.form["imageUploadCollection"]
            collectionKey = request.form["keyWordsCollection"]
            doc_ref = db.collection('collections').document(id.hex)
            doc_ref.set({
                'collection_name': collectionName,
                'image_url': collectionImage,
                'search_keyword': collectionKey,
                'views': 0
            })
            return redirect(url_for('index'))
            # return index
    elif request.method == "GET":
        print('this ia a get method')
        return 'this ia a get method'
    # return render_template("home.html")


@app.route("/collection", methods=['POST'])
def collectionNew():
    print('collection function')
    if request.method == "POST":
        if request.form.get("submitCollection"):
            print("collection adding...")
            id = uuid.uuid1()
            collectionName = request.form["CollectionName"]
            collectionImage = request.form["imageUploadCollection"]
            collectionKey = request.form["keyWordsCollection"]
            doc_ref = db.collection('collections').document(id.hex)
            doc_ref.set({
                'collection_name': collectionName,
                'image_url': collectionImage,
                'search_keyword': collectionKey,
                'views': 0
            })
            return redirect(url_for('index'))
    elif request.method == "GET":
        print('this ia a get method')
        return 'this ia a get method'

if __name__ == "__main__":
    #app.debug = True
    app.run()
