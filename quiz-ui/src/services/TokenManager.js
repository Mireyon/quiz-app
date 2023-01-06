export default {
  clear() {
    window.sessionStorage.removeItem('token');
  },
  saveToken(token) {
    window.sessionStorage.setItem('token', token);
  },
  getToken() {
    return window.sessionStorage.getItem('token');
  },
}