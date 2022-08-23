import face_recognition
import numpy as np

# import urllib.request

# url1 = 'https://upload.wikimedia.org/wikipedia/commons/8/8a/Hilary_Duff_Vogue_2019_2.png'
# url2 = 'https://api.time.com/wp-content/uploads/2015/03/hillary-duff.jpg'
# url3 = 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Helene_Fischer_2016.jpg'
# response1 = urllib.request.urlopen(url1)
# response2 = urllib.request.urlopen(url3)

def compare(face1, face2):

    known_image = np.array(face1.convert('RGB'))
    unknown_image = np.array(face2.convert('RGB'))

    known_encoding = face_recognition.face_encodings(known_image)
    unknown_encoding = face_recognition.face_encodings(unknown_image)

    if len(known_encoding) != 0 and len(unknown_encoding) != 0:
        known_encoding = known_encoding[0]
        unknown_encoding = unknown_encoding[0]

        results = face_recognition.compare_faces([known_encoding], unknown_encoding)

        print(results[0])

        return results[0]
    
    else:
        return False
