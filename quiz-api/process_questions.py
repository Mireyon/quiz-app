import sqlite3
import json
from collections import defaultdict 

def pageNotFound(func):
    def wrapper(*args, **kwargs):
        position = kwargs['position'] if 'position' in kwargs else None
        id = kwargs['id'] if 'id' in kwargs else None
        db_connection, cur = connect_db()
        query = f'SELECT * FROM Question WHERE position="{position}"' if id is None else f'SELECT * FROM Question WHERE rowid ="{id}"'
        output = cur.execute(query)
        output = output.fetchone()
        close_connection(db_connection, cur)
        return func(*args, **kwargs) if output is not None else ("Page Not Found", 404)
    return wrapper

class Answer:
    def __init__(self, answers) -> None:
        self.text = answers["text"]
        self.isCorrect = answers["isCorrect"]==1

    def json(self):
        return json.loads(json.JSONEncoder().encode(self.__dict__))

class Question:
    def __init__(self, *args) -> None:
        if(len(args)==1):
            question = args[0]
            self.text = question["text"]
            self.title = question["title"]
            self.image = question["image"]
            self.position = question["position"]
            self.possibleAnswers = [Answer(element) for element in question["possibleAnswers"]]
        elif(len(args)==5):
            text, title, image, position, possibleAnswers = args
            self.text = text
            self.title = title
            self.image = image
            self.position = position
            self.possibleAnswers = [Answer(element) for element in possibleAnswers]

    def answers2json(self):
        return [answer.json() for answer in self.possibleAnswers]

    def tuple(self):
        return (self.text, self.title, self.image, self.position)

def json2python(question):
    return Question(question)

def python2json(question):
    return {"id": question.id,
            "text": question.text,
            "title": question.title,
            "image": question.image,
            "position": question.position,
            "possibleAnswers": question.answers2json()}

def connect_db():
    path = "./quiz.db"
    db_connection = sqlite3.connect(path)
    cur = db_connection.cursor()
    return db_connection, cur

def close_connection(db_connection, cur):
    db_connection.commit()
    cur.close()

def update_position(delete_pos = None, add_pos = None, previous_pos = None, current_pos = None):
    db_connection, cur = connect_db()
    #add
    if(add_pos is not None):
        change_pos = cur.execute(f'UPDATE Question SET position = position + 1 WHERE position>={add_pos}')
        change_pos = cur.execute(f'UPDATE Answer SET position = position + 1 WHERE position>={add_pos}')
        close_connection(db_connection, cur)
        return

    #delete
    if(delete_pos is not None):
        change_pos = cur.execute(f'UPDATE Question SET position = position - 1 WHERE position>{delete_pos}')
        change_pos = cur.execute(f'UPDATE Answer SET position = position - 1 WHERE position>{delete_pos}')
        close_connection(db_connection, cur)
        return

    #update
    if(previous_pos<int(current_pos)):
        change_pos = cur.execute(f'UPDATE Question SET position = position - 1 WHERE position>={previous_pos} AND position<={current_pos}')
        change_pos = cur.execute(f'UPDATE Answer SET position = position - 1 WHERE position>={previous_pos} AND position<={current_pos}')
    else:
        change_pos = cur.execute(f'UPDATE Question SET position = position + 1 WHERE position<={previous_pos} AND position>={current_pos}')
        change_pos = cur.execute(f'UPDATE Answer SET position = position + 1 WHERE position<={previous_pos} AND position>={current_pos}')

    close_connection(db_connection, cur)

def add_db(question):
    update_position(add_pos = question.position)
    db_connection, cur = connect_db()
    insert_question = cur.execute(f'INSERT INTO Question(text, title, image, position) VALUES (?,?,?,?)', question.tuple())
    list_answers = question.possibleAnswers
    id = cur.lastrowid
    data = [(id, question.position, answer.text, answer.isCorrect) for answer in list_answers]
    insert_answer = cur.executemany(f'INSERT INTO Answer values (?,?,?,?)', data)

    close_connection(db_connection, cur)
    return id

@pageNotFound
def get_db(position=None, id=None):
    db_connection, cur = connect_db()
    question_query = f'SELECT rowid, * FROM Question WHERE position="{position}"' if id is None else f'SELECT rowid, * FROM Question WHERE rowid ="{id}"'
    question_result = cur.execute(question_query)
    questionId, text, title, image, position = question_result.fetchone()

    answer_query = f'SELECT * FROM Answer WHERE position="{position}"' if id is None else f'SELECT * FROM Answer WHERE id ="{id}"'
    answer_result = cur.execute(answer_query)
    possibleAnswers = answer_result.fetchall()

    possibleAnswers = [{"text": element[2], "isCorrect": element[3]} for element in possibleAnswers]
    question = Question(text, title, image, position, possibleAnswers)
    question.id = questionId

    close_connection(db_connection, cur)
    return python2json(question)

@pageNotFound
def update_db(id, question):
    db_connection, cur = connect_db()
    previous_position = cur.execute(f'SELECT position FROM Question WHERE rowid="{id}"')
    previous_position, = previous_position.fetchone()
    update_position(previous_pos=previous_position, current_pos=question.position)

    update_question = cur.execute(f'UPDATE Question SET text=?, title=?, image=?, position=? WHERE rowid="{id}"', question.tuple())
    list_answers = question.possibleAnswers
    delete_prev_answers = cur.execute(f'DELETE FROM Answer WHERE id=?', (id,))
    data = [(id, question.position, answer.text, answer.isCorrect) for answer in list_answers]
    update_answers = cur.executemany(f'INSERT INTO Answer values (?,?,?,?)', data)
    close_connection(db_connection, cur)    
    return 'Ok', 204

@pageNotFound
def delete_db(id):
    db_connection, cur = connect_db()
    delete_position = cur.execute(f'SELECT position FROM Question WHERE rowid=?', (id,))
    delete_position, = delete_position.fetchone()
    update_position(delete_pos=delete_position)
    delete_question = cur.execute(f'DELETE FROM Question WHERE rowid=?', (id,))
    delete_answer = cur.execute(f'DELETE FROM Answer WHERE id=?', (id,))
    close_connection(db_connection, cur)
    return 'Ok', 204

def empty_db():
    db_connection, cur = connect_db()
    clear_question = cur.execute(f'DELETE FROM Question')
    clear_answer = cur.execute(f'DELETE FROM Answer')
    close_connection(db_connection, cur)
    return 'Ok', 204

def get_all_db():
    list_questions = []

    db_connection, cur = connect_db()
    question_query = f'SELECT rowid, * FROM Question'
    question_result = cur.execute(question_query)
    question_data = question_result.fetchall()

    answer_query = f'SELECT * FROM Answer'
    answer_result = cur.execute(answer_query)
    answer_data = answer_result.fetchall()

    for question_tuple in question_data:
        questionId, text, title, image, position = question_tuple
        list_answers = [x[2:] for x in answer_data if x[0] == questionId]
        possibleAnswers = [{"text": element[0], "isCorrect": element[1]} for element in list_answers]
        question = Question(text, title, image, position, possibleAnswers)
        question.id = questionId
        list_questions.append(python2json(question))
    
    list_questions = sorted(list_questions, key=lambda x: x["position"])

    close_connection(db_connection, cur)
    return list_questions 

def rebuild_db():
    db_connection, cur = connect_db()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

    for table_name, in cur.fetchall():
        cur.execute(f"DROP TABLE {table_name}")

    cur.execute(f'CREATE TABLE "Answer" ("id" INTEGER,"position" INTEGER,"text" TEXT,"isCorrect" INTEGER)')
    cur.execute(f'CREATE TABLE "Question" ("text" TEXT,"title" TEXT,"image" TEXT,"position" INTEGER)')
    close_connection(db_connection, cur)
    return 'Ok', 200

def get_correctAnswers(answers):
    db_connection, cur = connect_db()
    score = 0
    output = cur.execute(f'SELECT GROUP_CONCAT(isCorrect) FROM Answer GROUP BY position')
    output = output.fetchall()
    for element, answer in zip(output, answers):
        correct_answer = element[0].split(",").index('1')
        if(correct_answer==answer):
            score += 1
    close_connection(db_connection, cur)
    return score

class QuizInfo:
    scores = []
    @staticmethod
    def quiz_info():
        db_connection, cur = connect_db()
        nbr_questions = cur.execute(f'SELECT * FROM Question')
        nbr_questions = len(nbr_questions.fetchall())
        close_connection(db_connection, cur)
        return {"size": nbr_questions, "scores": QuizInfo.scores}, 200

    @staticmethod
    def add_participant(participant):
        QuizInfo.scores.append(participant)
        QuizInfo.scores.sort(key = lambda x: x['score'], reverse=True)

    @staticmethod
    def delete_participants():
        QuizInfo.scores.clear()
        return 'Participants removed', 204

def send_participation(payload):
    answers = payload['answers']
    info, _ = QuizInfo.quiz_info()
    size = info['size']
    if(len(answers)!=size):
        return "Number of answers doesn't match the number of questions", 400
    
    score = get_correctAnswers(answers)
    participant = {"playerName": payload['playerName'], "score": score}
    QuizInfo.add_participant(participant)
    return participant, 200
    

 