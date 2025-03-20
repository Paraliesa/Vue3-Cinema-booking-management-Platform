<template>
  <div v-if="needHeader == '1'">
    <header :class="[isTop ? 'header-top' : 'header-not-top', 'header']">
      <div class="logo" :class="{ 'small-logo': !isTop }"></div>
      <nav>
        <a href="#" @click.prevent="goToHomePage">首页</a>
        <a href="#" @click.prevent="goToMovies">影片</a>
        <a href="#" @click.prevent="goToCinemas">影院</a>
        <button v-if="!username" @click="goToLogin">登录</button>
        <div v-else class="user-info" @click="toggleDropdown">
          欢迎您：{{ username }} ▼
          <div v-if="isDropdownVisible" class="dropdown-menu">
            <a href="#" @click.prevent="goToProfile">个人资料</a>
            <a href="#" @click.prevent="goToLogout">退出登录</a>
          </div>
        </div>
      </nav>
    </header>
  </div>  
</template>
  
  <script>
  import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
  import { useRouter } from 'vue-router';
  import { useHeaderStore } from '../../stores/header';
  
  export default {
    name: 'TopHeader',
    setup() {
      const store = useHeaderStore();
      const headerColor = ref('#FEC979');
      const isTop = ref(true);
      const username = ref(null);
      const router = useRouter();
      const isDropdownVisible = ref(false);
      const needHeader = ref(store.needHeader);

      watch(() => store.needHeader, (newValue, oldValue) => {
        if (newValue !== oldValue) {
          needHeader.value = newValue;
        }
      });
  
      const handleScroll = () => {
        headerColor.value = window.scrollY === 0 ? '#FEC979' : '#fff';
        isTop.value = window.scrollY === 0;
      };
  
      const toggleDropdown = () => {
        isDropdownVisible.value = !isDropdownVisible.value; 
      };
  
  
      const goToLogin = () => {
        router.push('/LoginPage'); 
      };
  
      const goToProfile = () => {
        router.push('/ProfilePage'); 
      };
  
  
      const goToLogout = () => {
        localStorage.removeItem('username');
        username.value = null;
        localStorage.removeItem('password');
        localStorage.removeItem('role');
        localStorage.removeItem('cid')
        localStorage.removeItem('uid')
        router.push('/LoginPage');
      };
  
      const goToHomePage = () => {
        router.push('/'); 
      };
  
      const goToCinemas = () => {
        router.push('/ManageCinemas/'); 
      };
  
      const goToMovies = () => {
        router.push('/AllMovies/'); 
      };
  
  
      onMounted(() => {
        window.addEventListener('scroll', handleScroll);
        handleScroll();
        const storedUsername = localStorage.getItem('username');
        if (storedUsername) {
          username.value = storedUsername; 
        }
      });
  
      onBeforeUnmount(() => {
        window.removeEventListener('scroll', handleScroll);
      });
  
      return {
        isTop,
        headerColor,
        username,
        isDropdownVisible,
        goToLogin,
        goToProfile,
        goToLogout,
        toggleDropdown,
        goToHomePage,
        goToCinemas,
        goToMovies,
        needHeader
      };
    }
  };
  </script>
  
  <style scoped>
  
  .user-info {
    margin-right: 5vw;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    color: #333;
    position: relative; 
    transition: color 0.3s ease;
  }
  
  .user-info:hover {
    color: #ff6767; 
  }
  
  .dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: #fff;
    border: 1px solid #ccc;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    padding: 10px 0;
    width: 200px;
    z-index: 100;
  }
  
  .dropdown-menu a {
    padding: 8px 16px;
    text-decoration: none;
    color: #333;
    font-size: 1.1rem;
    transition: background-color 0.3s ease, color 0.3s ease;
    width: 160px;
  }
  
  .dropdown-menu a:hover {
    background-color: #FEC979;
    color: #fff;
  }
  
  .header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
    transition: height .3s ease, padding .3s ease, background-color .3s ease;
    border-bottom: 1px solid #ccc;
  }
  
  .header, .header * {
    font-family: 'Microsoft YaHei', '黑体', sans-serif; 
    font-weight: 500; 
  }
  
  .header-top {
    background-color: #FEC979;
    height: 15vh;
    border-bottom: none;
  }
  
  .header-not-top {
    background-color: #fff;
    height: 10vh;
  }
  
  .logo {
    background-image: url('../../assets/logo2.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    height: 20vh; 
    width: 40vh;
    margin-right: 2vw;
    transition: height 0.3s ease;
  }
  
  .small-logo {
    background-image: url('../../assets/logo2.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    height: 10vh; 
    width: 20vh;
    margin-right: 2vw;
    transition: height 0.3s ease;
  }
  
  nav {
    display: flex;
    align-items: center;
  }
  
  nav a {
    margin-right: 3vw;
    text-decoration: none;
    color: #333;
    font-size: 1.3rem; 
    font-weight: 600; 
    transition: color 0.3s ease;
  }
  
  nav a:hover {
    color: #ff6767;
  }
  
  nav button {
    margin-right: 5vw;
    padding: 10px 15px; 
    border: none;
    background-color: #333;
    color: #fff;
    font-size: 1.2rem; 
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s ease;
  }
  
  nav button:hover {
    background-color: #FEC979; 
  }
  .user-info {
    margin-right: 5vw;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    color: #333;
  }
  </style>
  