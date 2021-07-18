function apiUrl() {
  return 'http://192.168.37.8:8080/';
}

export function postApi(pathToResource, data) {
  return fetch(apiUrl() + pathToResource, {
    method: 'POST',
    mode: 'cors',
    body: new URLSearchParams(data),
  });
}
