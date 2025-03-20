<template>
    <div class="profile-page">
      <h2>个人信息</h2>
      <p>用户名: {{ username }}</p>
      <button @click="logout">退出登录</button>
    </div>
  </template>
  
  <script>
  import { ref} from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'ProfilePage',
    setup() {
      const username = ref(localStorage.getItem('username'));
      const router = useRouter();
      const logout = () => {
        localStorage.removeItem('username'); // 移除登录状态
        router.push('/LoginPage'); // 退出后跳转到登录页
      };
  
      return {
        username,
        logout,
      };
    },
  };
  </script>
  
  <style scoped>
  .profile-page {
    text-align: center;
    padding: 2rem;
    margin-top: 20vh;
  }
  
  button {
    padding: 0.5rem 2rem;
    background-color: #fecd79;
    border: none;
    cursor: pointer;
    border-radius: 4px;
  }
  
  button:hover {
    background-color: #febc61;
  }
  </style>
  