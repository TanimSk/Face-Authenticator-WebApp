
import face_recognition
import urllib.request

url1 = 'https://upload.wikimedia.org/wikipedia/commons/8/8a/Hilary_Duff_Vogue_2019_2.png'
url2 = 'https://api.time.com/wp-content/uploads/2015/03/hillary-duff.jpg'
url3 = 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Helene_Fischer_2016.jpg'

response1 = urllib.request.urlopen(url1)
response2 = urllib.request.urlopen(url3)

known_image = face_recognition.load_image_file(response1)
unknown_image = face_recognition.load_image_file(response2)

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

print(results)