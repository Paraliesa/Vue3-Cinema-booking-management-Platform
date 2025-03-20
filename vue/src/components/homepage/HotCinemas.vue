<template>
    <section class="section">
      <h2>热门影院</h2>
  
  
      <!-- 影院列表展示 -->
      <div class="cinema-list">
        <div 
          v-for="cinema in topCinemas" 
          :key="cinema.cid" 
          class="cinema-card" 
          @click="goToCinemaDetails(cinema.cid)"
        >
          <h3>{{ cinema.cname }}</h3>
        </div>
      </div>
  
      <!-- 查看更多按钮 -->
      <div class="view-more">
        <button @click="viewMoreCinemas">查看更多</button>
      </div>
    </section>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'HotCinemas',
    setup() {
      const router = useRouter();
      const topCinemas = ref([]);
  
      const fetchTopCinemas = async () => {
        try {
          const response = await axios.get('http://127.0.0.1:8001/cinemascontroller/'); 
          topCinemas.value = response.data.slice(0, 3); 
        } catch (error) {
          console.error('获取热门影院失败:', error);
        }
      };
  
      // 跳转到影院详情页
      const goToCinemaDetails = (cinemaId) => {
        router.push(`/SingleCinema/`);
        localStorage.setItem("cid", cinemaId);
      };
  
      // 查看更多影院
      const viewMoreCinemas = () => {
        router.push(`/ManageCinemas/`);
      };
  
      onMounted(() => {
        fetchTopCinemas();
      });
  
      return {
        topCinemas,
        goToCinemaDetails,
        viewMoreCinemas,
      };
    },
  };
  </script>
  
  <style scoped>
  .section {
    padding: 2rem;
    background-color: #f9f9f9;
  }
  
  h2 {
    font-size: 2rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 1rem;
  }
  
  p {
    font-size: 1rem;
    color: #7f8c8d;
    margin-bottom: 2rem;
  }
  
  .cinema-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .cinema-card {
    background-color: #ffffff;
    color: #333;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    border: 1px solid #e1e4e8;
  }
  
  .cinema-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }
  
  .cinema-card h3 {
    font-size: 1.4rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
  }
  
  .view-more {
    text-align: center;
    margin-top: 2rem;
  }
  
  .view-more button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 0.8rem 1.6rem;
    font-size: 1rem;
    border-radius: 25px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .view-more button:hover {
    background-color: #2980b9;
  }
  </style>
  