from flask import Flask, request
from flask_cors import CORS
import jwt_utils
from process_questions import json2python, add_db, get_db, empty_db, update_db, delete_db, QuizInfo, send_participation, rebuild_db, get_all_db

app = Flask(__name__)
CORS(app)

@app.route('/')
def API_test():
	return f"The API is working !"

@app.route('/token', methods=['POST'])
def PostToken():
    token = request.headers.get('Authorization')
    if(token):
        try:
            jwt_utils.decode_token(token.split(" ")[1])
            return 'Ok', 200
        except:
            return 'Unauthorized', 401
    return 'Unauthorized', 401

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return QuizInfo.quiz_info()

@app.route('/login', methods=['POST'])
def PostLogin():
    payload = request.get_json()
    if(payload["password"]=="flask2023"):
        return {"token": jwt_utils.build_token()}
    return 'Unauthorized', 401

@app.route('/questions', methods=['POST'])
def PostQuestion():
    token = request.headers.get('Authorization')
    if(token):
        if(jwt_utils.decode_token(token.split(" ")[1]) == "quiz-app-admin"):
            payload = request.get_json()
            id = add_db(json2python(payload))
            return {"id" : id}
    return 'Unauthorized', 401

@app.route('/questions', methods=['GET'])
def GetQuestionByPosition():
    position = request.args.get('position')
    if(position=="all"):
        return get_all_db()
    return get_db(position=position)

@app.route('/questions/<questionId>', methods=['GET'])
def GetQuestionById(questionId):
    return get_db(id=questionId)

@app.route('/questions/<questionId>', methods=['PUT'])
def UpdateQuestion(questionId):
    token = request.headers.get('Authorization')
    if(token):
        payload = request.get_json()
        return update_db(id=questionId, question=json2python(payload))
    return 'Unauthorized', 401

@app.route('/questions/<questionId>', methods=['DELETE'])
def DeleteQuestion(questionId):
    token = request.headers.get('Authorization')
    if(token):
        if(questionId=="all"):
            return empty_db()
        return delete_db(id=questionId)
    return 'Unauthorized', 401

@app.route('/participations/all', methods=['DELETE'])
def DeleteParticipation():
    token = request.headers.get('Authorization')
    if(token):
        return QuizInfo.delete_participants()
    return 'Unauthorized', 401

@app.route('/participations', methods=['POST'])
def PostParticipation():
    payload = request.get_json()
    return send_participation(payload)

@app.route('/rebuild-db', methods=['POST'])
def RebuildDatabase():
    token = request.headers.get('Authorization')
    if(token):
        return rebuild_db()
    return 'Unauthorized', 401

if __name__ == "__main__":
    app.run(debug=True)