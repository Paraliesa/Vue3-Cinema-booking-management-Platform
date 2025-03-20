<template>
    <section class="hero">
      <div class="hero-content">
        <h1 class="title">Cinema Distribution Zone</h1>
        <p class="subtitle">光影交错，一票在手，精彩世界任您游！</p>
        <div class="buttons">
          <button class="btn"  @click="gotoAllMovies">影片</button>
          <button class="btn"  @click="gotoManageCinemas">影院</button>
          <button class="btn"  @click="gotoMyOrders">我的订单</button>
          <button v-if="isAdmin" class="btn" @click="goToAdminPage">管理</button>
        </div>
      </div>
      <div class="triangle"></div>
    </section>
</template>
  
<script>
    import { computed } from 'vue';
    import { useRouter } from 'vue-router';

    export default {
    name: 'HeroSection',

    setup() {
        const router = useRouter();

        // 计算属性，判断是否是管理员
        const isAdmin = computed(() => localStorage.getItem('role') === 'admin');

        // 定义跳转方法
        const goToAdminPage = () => router.push('/AdminPage');
        const gotoAllMovies = () => router.push('/AllMovies');
        const gotoManageCinemas = () => router.push('/AllTheaters');
        const gotoMyOrders = () => router.push('/MyOrders');

        return {
        isAdmin,
        goToAdminPage,
        gotoAllMovies,
        gotoManageCinemas,
        gotoMyOrders
        };
    }
    };
</script>
  
<style scoped>
  body, html {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  .hero {
    display: block;
    background-color: #FEC979;
    padding: 10vh 0;
    position: relative;
    width: 100%; 
    margin: 0; /* 清除外边距 */
  }
  
  .hero-content {
    margin: 0 auto;
    max-width: 800px;
  }
  
  .title {
    font-size: 3rem;
    font-weight: 150; /* 使用较轻的字体 */
    font-family: 'BIZ UDPGothic'; 
    margin-bottom: 1rem;
    text-align: center; /* 使标题居中 */
  }
  
  .subtitle {
    font-size: 1.2rem;
    color: #555;
    margin-bottom: 2rem;
    text-align: right;
    margin-right: 1vh;
  }
  
  .buttons {
    display: flex;
    justify-content: right; 
    gap: 1rem;
    margin-right: 3vh;
  }
  
  .btn {
    padding: 0.8rem 1.5rem;
    border: none;
    background-color: #fff;
    color: #333;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }
  
  .btn:hover {
    background-color: #ddd;
  }
  
  .triangle {
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 10vh;
    height: 10vh;
    background-color: #FEC979;
    transform: translateX(-50%) rotate(45deg);
  }
  </style>
  