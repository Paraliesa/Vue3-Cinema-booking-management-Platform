import { defineStore } from 'pinia'

export const useHeaderStore = defineStore('header', {
  state: () => ({
    needHeader: 1,
  }),
  actions: {
    setNeedHeader(value) {
      this.needHeader = value;
    }
  }
});