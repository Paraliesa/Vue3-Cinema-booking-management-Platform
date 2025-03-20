import { defineStore } from 'pinia'

export const useHeaderStore = defineStore('header', {
  state: () => ({
    needHeader: sessionStorage.getItem('needheader') || '1',
  }),
  actions: {
    setNeedHeader(value) {
      this.needHeader = value;
      sessionStorage.setItem('needheader', value); 
    }
  }
});