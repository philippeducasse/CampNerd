import { createStore } from 'vuex';

export default createStore({
  state: {
    selectedCampingSite: null,
    startDate: '',
    endDate: ''
  },
  mutations: {
    setSelectedCampingSite(state, site) {
      state.selectedCampingSite = site;
    },
    setStartDate(state, date) {
      state.startDate = date;
    },
    setEndDate(state, date) {
      state.endDate = date;
    }
  },
  actions: {
    updateCampingSite({ commit }, site) {
      commit('setSelectedCampingSite', site);
    },
    updateStartDate({ commit }, date) {
      commit('setStartDate', date);
    },
    updateEndDate({ commit }, date) {
      commit('setEndDate', date);
    }
  },
  getters: {
    getSelectedCampingSite: (state) => state.selectedCampingSite,
    getStartDate: (state) => state.startDate,
    getEndDate: (state) => state.endDate
  }
});
