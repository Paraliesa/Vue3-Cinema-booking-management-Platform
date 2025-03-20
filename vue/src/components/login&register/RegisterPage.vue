<template>
    <div class="register-page">
      <div class="register-container">
        <h2>欢迎注册CDZ电影购票系统!</h2>
        <form @submit.prevent="handleRegister">
          <div class="input-group">
            <label for="username">用户名</label>
            <input
              type="text"
              id="username"
              v-model="username"
              placeholder="请输入用户名"
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
            <label for="confirmPassword">确认密码</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="请确认密码"
              required
            />
          </div>
  
          <div class="input-group">
            <label for="gender">性别</label>
            <div class="gender-options">
              <label>
                <input type="radio" v-model="gender" value="男" /> 男
              </label>
              <label>
                <input type="radio" v-model="gender" value="女" /> 女
              </label>
              <label>
                <input type="radio" v-model="gender" value="保密" /> 保密
              </label>
            </div>
          </div>
  
          <div class="input-group">
            <label for="phone">手机号</label>
            <input
              type="text"
              id="phone"
              v-model="phone"
              placeholder="请输入手机号"
              maxlength="11"
              pattern="^[0-9]{11}$"
              required
            />
          </div>
  
          <div>
            <button type="submit">注册</button>
          </div>
        </form>
        <p>
          已有账号？
          <a href="#" @click="goToLogin">登录</a>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import axios from "axios";
  
  export default {
    name: "RegisterPage",
    setup() {
      const username = ref("");
      const password = ref("");
      const confirmPassword = ref("");
      const gender = ref(""); 
      const phone = ref("");  
      const router = useRouter();

      const handleRegister = async () => {
        if (password.value !== confirmPassword.value) {
          alert("两次输入的密码不一致");
          return;
        }
  
        // 校验手机号格式
        const phoneRegex = /^[0-9]{11}$/;
        if (!phone.value.match(phoneRegex)) {
          alert("请输入有效的手机号");
          return;
        }
  
        const data = {
          username: username.value,
          password: password.value,
          gender: gender.value,
          phone: phone.value,
        };
  
        try {
          const response = await axios.post("http://localhost:8001/register/", data);
  
          if (response.status === 201) {
            alert("注册成功！");
            router.push("/LoginPage/"); // 注册成功后跳转到首页
          }
          else {
            alert(response.data.error);
          }
        } catch (error) {
          console.error("注册失败", error);
          alert("注册失败，请稍后再试！");
        }
      };
  
      const goToLogin = () => {
        router.push("/LoginPage"); // 跳转到登录页面
      };

  
      return {
        username,
        password,
        confirmPassword,
        gender,
        phone,
        handleRegister,
        goToLogin,
      };
    },
  };
  </script>
  
  <style scoped>
  /* 注册页面整体样式 */
  .register-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f9f9f9;
  }
  
  .register-container {
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
    margin-right: 0.5rem;
  }
  
  .gender-options {
    display: flex;
    gap: 1rem;
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
  