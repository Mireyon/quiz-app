class Answer:
    def __init__(self, text, isCorrect) -> None:
        self.text = text
        self.isCorrect = isCorrect

class Question:
    def __init__(self, title, text, id, listAnswers, image = None) -> None:
        self.title = title
        self.text = text
        self.id = id
        self.listAnswers = listAnswers
        self.image = image

    def __init__(self, question) -> None:
        self.title = question["title"]
        self.text = question["text"]
        self.id = question["position"]
        self.listAnswers = question["possibleAnswers"]
        self.image = question["image"]

    def get_correctAnswer(self):
        pass

def json2python(question):
    return Question(question)

def python2json(question):
    return {"text": question.text,
            "title": question.title,
            "image": question.image,
            "position": question.id,
            "possibleAnswers": question.listAnswers}

    