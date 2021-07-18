import { postApi } from './api';

const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };

export const auth = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ commit }, user) {
      return login(user).then(
        user => {
          console.log('login success');
	  commit('loginSuccess', user);
          return Promise.resolve(user);
        },
        error => {
	  console.log('login failre');
          commit('loginFailure');
          return Promise.reject(error);
        }
      );
    },
    logout({ commit }) {
      logout();
      commit('logout');
    },
    register({ commit }, user) {
      return register(user).then(
        response => {
          commit('registerSuccess');
          return Promise.resolve(response.data);
        },
        error => {
          commit('registerFailure');
          return Promise.reject(error);
        }
      );
    }
  },
  mutations: {
    loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    }
  }
};

async function login(user) {
  await postApi("token", user)
    .then((response) => response.json())
    .then((data) => {
      if (data.access_token) {
        localStorage.setItem('user', JSON.stringify(data));
      }
    });
}

async function logout() {
  localStorage.removeItem('user');
}
