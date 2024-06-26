from firebase_admin import firestore, credentials, initialize_app

cred = credentials.Certificate("./classof2024ssSDK.json")
initialize_app(cred)

db = firestore.client()
alumni_col_ref = db.collection('alumnis')
students_col_ref = db.collection('students')

def addWishes(alumniID, student_doc_id,  message):
    alumni_doc_ref = alumni_col_ref.document(f"{alumniID}")
    student_doc_ref = students_col_ref.document(f"{student_doc_id}")
    wishesArray = list(alumni_doc_ref.get().to_dict()['wishes'])
    givenWishesArray = list(student_doc_ref.get().to_dict()['givenWishes'])
    
    alumni_doc_ref.update({
    'wishes': [message] + wishesArray
    })

    student_doc_ref.update({
    'givenWishes': [message] + givenWishesArray
    })

def isUserExist(document_id):
    doc_ref = students_col_ref.document(f"{document_id}")

    return doc_ref.get().exists
def setupStudentAccount(document_id):
    data = {
        'id': document_id,
        'givenWishes': [],
    }

    students_col_ref.add(data, data['id'])
def followingList(userID): 
    return alumni_col_ref.document(f"{userID}").get().to_dict()['follows']

def unFollow(userID, toRemove):
    doc_ref = alumni_col_ref.document(f"{userID}")
    doc_ref.update({
        'follows': firestore.firestore.ArrayRemove([toRemove])
    })


def addFollowing(userID, followTo):
    doc_ref = alumni_col_ref.document(f"{userID}")
    followsArray = list(doc_ref.get().to_dict()['follows'])
    
    # adds new follow to follows property in the document
    doc_ref.update({
    'follows': [followTo] + followsArray
    })