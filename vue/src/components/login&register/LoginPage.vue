<template>
    <div class="login-page">
      <div class="login-container">
        <h2>欢迎使用CDZ电影购票系统!</h2>
        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="username">用户名/手机号</label>
            <input
              type="text"
              id="username"
              v-model="username"
              placeholder="请输入用户名或手机号"
              required
            />
          </div>
          <div class="input-group">
            <label for="password">密码</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="请输入密码"
              required
            />
          </div>
          <div class="input-group">
            <label>身份</label>
            <div class="role-options">
              <label for="user" class="role-label">
                <input type="radio" id="user" value="normal" v-model="role" />
                普通用户
              </label>
              <label for="admin" class="role-label">
                <input type="radio" id="admin" value="admin" v-model="role" />
                管理员
              </label>
            </div>
          </div>
          <div>
            <button type="submit">登录</button>
          </div>
        </form>
        <p>
          没有账号？
          <a href="#"  @click="goToRegister">注册</a>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import axios from 'axios';
  
  export default {
    name: "LoginPage",
    setup() {
      const username = ref("");
      const password = ref("");
      const role = ref("user");
      const router = useRouter();
  
      const handleLogin = async () => {
        try {
          const response = await axios.post("http://localhost:8001/login/", {
            username: username.value,
            password: password.value,
            role: role.value,
          });
  
          if (response.status === 201) {
            localStorage.setItem("username", username.value);
            localStorage.setItem("role", role.value);
            localStorage.setItem("uid", response.data.uid)
            
            if (role.value === "admin") {
              router.push("/AdminPage"); 
            } else {
              router.push("/"); 
            }
          } else {
            alert("用户名、密码或身份错误");
          }
        } catch (error) {
          console.error(error);
          alert("用户名、密码或身份错误");
        }
      };
  
      const goToRegister = () => {
        router.push("/RegisterPage"); // 跳转到注册页面
      };
  
      return {
        username,
        password,
        role,
        handleLogin,
        goToRegister,
      };
    },
  };
  </script>
  
  <style scoped>
  /* 登录页面整体样式 */
  .login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f9f9f9;
  }
  
  .login-container {
    padding: 3rem 2rem;
    background-color: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    width: 100%;
    max-width: 75vh;
  }
  
  h2 {
    font-size: 1.8rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .input-group {
    margin-bottom: 1.5rem;
    margin-right: 5vh;
  }
  
  label {
    display: block;
    font-size: 1rem;
    color: #555;
    margin-bottom: 0.5rem;
  }
  
  input {
    width: 100%;
    padding: 0.8rem;
    border-radius: 5px;
    border: 1px solid #ccc;
    font-size: 1rem;
    color: #333;
    margin-top: 0.5rem;
  }
  
  input[type="radio"] {
    margin-right: 0rem;
  }
  
  .role-options {
    display: flex;
    justify-content: flex-start;
    gap: 1rem;
    align-items: center;
  }
  
  .role-label {
    display: inline-flex;
    align-items: center;
  
  }
  
  button {
    width: 100%;
    padding: 1rem;
    background-color: #fecd79;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    font-size: 1.2rem;
    font-weight: bold;
    color: #fff;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #febc61;
  }
  
  p {
    text-align: center;
    margin-top: 1.5rem;
  }
  
  a {
    color: #fecd79;
    font-weight: bold;
    text-decoration: none;
  }
  
  a:hover {
    color: #febc61;
  }
  </style>
  