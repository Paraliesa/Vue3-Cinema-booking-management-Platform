<template>
    <div class="manage-cinemas">
      <!-- 影院列表 -->
      <div class="cinema-list">
        <div 
          v-for="cinema in cinemas" 
          :key="cinema.cid" 
          class="cinema-card" 
          @click="goToCinemaDetails(cinema.cid)"
        >
          <h3>{{ cinema.cname }}</h3>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'AllTheaters',
    setup() {
      const router = useRouter();
      const cinemas = ref([]);
  
      const fetchCinemas = async () => {
        try {
          const response = await axios.get('http://127.0.0.1:8001/cinemascontroller/'); 
          cinemas.value = response.data; 
        } catch (error) {
          console.error('获取影院信息失败:', error);
        }
      };
  
      const goToCinemaDetails = (cinemaId) => {
        localStorage.setItem("cid", cinemaId);
        router.push(`/SingleTheater/`);
      };
  
      onMounted(() => {
        fetchCinemas();
      });
  
      return {
        cinemas,
        goToCinemaDetails,
      };
    },
  };
  </script>
  
  <style scoped>
  .manage-cinemas {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    background-color: #f0f4f8;
    margin-top: 20vh;
  }
  
  .cinema-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    width: 100%;
    margin-top: 2rem;
  }
  
  .cinema-card {
    background-color: #ffffff;
    color: #333;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
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
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  }
  
  .cinema-card h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
    color: #2c3e50;
  }
  </style>
  