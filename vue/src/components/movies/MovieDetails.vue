<template>
    <div class="movie-details">
      <!-- 电影介绍部分 -->
      <section class="movie-intro">
        <div class="movie-cover">
          <img :src=getCoverUrl(movie.cover) alt="Movie Cover" />
        </div>
        <div class="movie-info">
          <h1>{{ movie.mname }}</h1>
          <p><strong>时长：</strong>{{ movie.mtime }} 分钟</p>
          <p><strong>热度：</strong>{{ movie.mhot }}</p>
          <p><strong>评分：</strong>{{ movie.mscore }}</p>
          <p><strong>上线时间：</strong>{{ movie.myear }}</p>
          <p><strong>类型：</strong>{{ movie.type }}</p>
          <p><strong>来源地：</strong>{{ movie.place }}</p>
          <p>{{ movie.mtext }}</p>
        </div>
      </section>

      <!-- 影厅信息部分 -->
        <section class="hall-info">
        <h2>播放影厅</h2>
        <div class="hall-list">
            <div
            v-for="hall in halls"
            :key="hall.hid"
            class="hall-card"
            @click="goToHallDetails(hall.hid)"
            >
            <div class="hall-info-content">
                <h3>{{ hall.cinema }}</h3>
                <h3>{{ hall.hname }}</h3>
                <p><strong>播放时间：</strong>{{ formatTime(hall.fstarttime) }} - {{ formatTime(hall.fendtime) }}</p>
                <p><strong>票价：</strong>￥{{ hall.fcost }}</p>
            </div>
            </div>
        </div>
        </section>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'MovieDetails',
    setup() {
      const movie = ref({});  // 用于存储电影详细信息
      const halls = ref([]);
      const router = useRouter();
  
      // 从localStorage获取movieId
      const movieId = localStorage.getItem("mid");
  
      const fetchMovieDetails = async () => {
        try {
          const response = await axios.post('http://127.0.0.1:8001/movie_details/', movieId);
          movie.value = response.data;  // 将返回的电影数据赋值给movie
        } catch (error) {
          console.error('获取电影详情失败:', error);
        }
      };

      const fetchHalls = async () => {
        try {
            const response = await axios.post(`http://127.0.0.1:8001/get_movie_halls/`, movieId);
            halls.value = response.data;
        } catch (error) {
            console.error('获取影厅信息失败:', error);
        }
      };

      const getCoverUrl = (coverPath) => {
        return `${'http://127.0.0.1:8001'}${coverPath}`;
      };

      const formatTime = (time) => {
        const date = new Date(time);
        const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，+1并确保两位数
        const day = String(date.getDate()).padStart(2, '0'); // 确保两位数
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');

        return `${month}-${day} ${hours}:${minutes}`;
      };

      const goToHallDetails = (hallId) => {
        localStorage.setItem("hallId", hallId);
        router.push(`/HallDetails/`);
      };
  
      onMounted(() => {
        if (movieId) {
          fetchMovieDetails();
          fetchHalls();
        } else {
          console.error('没有找到电影ID');
        }
      });
  
      return {
        movie,
        halls,
        getCoverUrl,
        formatTime,
        goToHallDetails
      };
    },
  };
  </script>
  
  <style scoped>
  .movie-details {
    display: flex;
    flex-direction: column;
    padding: 2rem;
    background-color: #121212;
    color: white;
    margin-top: 15vh;
  }
  
  .movie-intro {
    display: flex;
    margin-bottom: 2rem;
  }
  
  .movie-cover img {
    width: 300px;
    height: 450px;
    object-fit: cover;
    border-radius: 10px;
  }
  
  .movie-info {
    margin-left: 2rem;
    flex: 1;
  }
  
  .movie-info h1 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  
  .movie-info p {
    font-size: 1rem;
    margin: 0.5rem 0;
  }
  
.hall-info {
  margin-top: 2rem;
}

.hall-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.hall-card {
  background-color: #ffffff;
  color: #333;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.hall-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.hall-info-content h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.hall-info-content p {
  font-size: 1rem;
}
  </style>
  