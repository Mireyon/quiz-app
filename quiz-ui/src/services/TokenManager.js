import QuizApiService from "./QuizApiService";

export default {
  clear() {
    window.sessionStorage.removeItem('token');
  },
  saveToken(token) {
    window.sessionStorage.setItem('token', token);
  },
  async getToken() {
    var token = window.sessionStorage.getItem('token');
    var response = await QuizApiService.checkToken(token);
    // console.log(response);
    if (response.status == 401) {
      token = null;
    }
    return token;
  },
}