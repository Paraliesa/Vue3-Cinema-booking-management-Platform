<template>
    <div class="single-cinema">
      <!-- 影院信息展示 -->
      <section v-if="cinema" class="part">
        <h2>{{ cinema.cname }} 影厅信息</h2>
        <div class="hall-list">
          <div 
            v-for="hall in halls" 
            :key="hall.hid" 
            class="hall-card" 
            @click="goToHallDetails(hall.hid)"
          >
            <h3>{{ hall.hname }}</h3>
            <p>近期排片安排:</p>
            <ul>
                <li v-for="arrangement in hall.arrangements" :key="arrangement.fid">
                    <strong>{{ arrangement.mname }}</strong> - 
                    <span>{{ formatDate(arrangement.fstarttime) }} ~ {{ formatDate(arrangement.fendtime) }}</span>
                </li>
            </ul>
          </div>
        </div>
      </section>
  
      <!-- 加载中 -->
      <p v-if="loading" class="part">正在加载...</p>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'SingleTheater',
    setup() {
      const router = useRouter();
      const cinema = ref(null); // 影院信息
      const halls = ref([]); // 影厅列表
      const loading = ref(true); // 加载状态
  
      const fetchCinemaData = async () => {
        const cid = localStorage.getItem('cid');
        try {
          // 请求影院信息及影厅数据
          const cinemaResponse = await axios.post(`http://127.0.0.1:8001/get_cinema/`,cid);
          cinema.value = cinemaResponse.data;
  
          const hallsResponse = await axios.post(`http://127.0.0.1:8001/get_halls/`,cid);
          halls.value = hallsResponse.data;
          for (let hall of halls.value) {
            hall.arrangements = await getTodayArrangements(hall.hid);  // 存储排片信息
          }
        } catch (error) {
          console.error('获取影院或影厅信息失败:', error);
        } finally {
          loading.value = false;
        }
      };
  
      // 获取当天的排片安排
      const getTodayArrangements = async(hallId) => {
        try{
            const hallresponse = await axios.post(`http://127.0.0.1:8001/get_hall_arrangement_today/`,hallId);
            return hallresponse.data;
        } catch(error){
            console.error('获取影厅排片信息失败:',error);
            return [];
        }
      };
  
      // 格式化时间
      const formatDate = (datetime) => {
      const date = new Date(datetime);
      const month = date.getMonth() + 1; // 月份从0开始，所以需要加1
      const day = date.getDate();
      const hours = date.getHours();
      const minutes = date.getMinutes();


      // 格式化为 "MM-DD HH:mm"
      return `${month}-${day} ${hours}:${minutes < 10 ? '0' + minutes : minutes}`; 
      };
  
      // 跳转到影厅详情
      const goToHallDetails = (hallId) => {
        localStorage.setItem('hallId',hallId);
        router.push(`/HallDetails/`);
      };
  
      // 在组件挂载时获取影院和影厅信息
      onMounted(() => {
        fetchCinemaData();
      });
  
      return {
        cinema,
        halls,
        loading,
        getTodayArrangements,
        formatDate,
        goToHallDetails,
      };
    },
  };
  </script>
  
  <style scoped>
  .part{
    margin-top: 20vh;
  }

  .single-cinema {
    padding: 2rem;
    background-color: #f9f9f9;
  }
  
  h2 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
  }
  
  .hall-list {
    display: grid;
    grid-template-columns:1fr;
    gap: 1.5rem;
  }
  
  .hall-card {
    background-color: #fec979;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
 
  }
  
  .hall-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }
  
  .hall-card h3 {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
  }
  
  .hall-card ul {
    list-style-type: none;
    padding-left: 0;
  }
  
  .hall-card li {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }
  
  .hall-card li strong {
    color: #333;
  }

  .hall-card p {
  text-align: left; /* 使“近期排片安排”靠左 */
  font-size: 1.1rem;
  margin-bottom: 1rem;
  }
  
  p {
    text-align: center;
    font-size: 1.2rem;
  }
  </style>
  