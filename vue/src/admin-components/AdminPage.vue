<template>
    <div class="admin-page">
      <div class="admin-actions">
        <button class="action-button" @click="viewAllOrders">查看所有订单</button>
        <button class="action-button" @click="manageMovies">电影信息管理</button>
        <button class="action-button" @click="manageScheduling">排片管理</button>
        <button class="action-button" @click="manageCinemas">影院管理</button>
      </div>
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';


  export default{
    name: 'AdminPage',
    setup() {
    const router = useRouter();
    const viewAllOrders = () => {
      // 可以在这里处理查看所有订单的逻辑
      router.push('/AdminCheckOrders');
    };

    const manageMovies = () => {
      // 跳转到电影信息管理页面
      router.push('/AdminManageMovies');
    };

    const manageScheduling = () => {
      // 跳转到排片管理页面
      router.push('/AdminManageScheduling');
    };

    const manageCinemas = () => {
      // 跳转到影院管理页面
      router.push('/AdminManageCinemas');
    };

    return {
      viewAllOrders,
      manageMovies,
      manageScheduling,
      manageCinemas,
    };
  },
};
  </script>
  
  <style scoped>
  .admin-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    background-color: #f9f9f9;
  }
  
  .admin-actions {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    max-width: 500px;
    margin-top: 20vh;
  }
  
  .action-button {
    background-color: #fec979;
    color: white;
    padding: 1rem;
    font-size: 1.2rem;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 100%;
  }
  
  .action-button:hover {
    background-color: #febc61;
  }
  
  .action-button:focus {
    outline: none;
  }
  
  h2 {
    font-size: 2rem;
    color: #333;
    font-weight: 600;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  </style>
  