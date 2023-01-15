import axios from "axios";

const instance = axios.create({
	baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        return {status:error.response.status, data:error.response.data};
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    return this.call("get", 'questions?position='+position);
  },
  sendParticipation(payload){
    return this.call("post", 'participations', payload);
  },
  sendLogin(payload){
    return this.call("post", 'login', payload);
  },
  deleteQuestion(questionId, token){
    return this.call("delete", 'questions/'+questionId, null, token);
  },
  sendQuestion(payload, token){
    return this.call("post", 'questions', payload, token);
  },
  updateQuestion(questionId, payload, token){
    return this.call("put", 'questions/'+questionId, payload, token);
  },
  checkToken(token){
    return this.call("post", 'token', null, token);
  }
};