<template>
    <section class="section">
      <h2>所有电影</h2>
  
      <!-- 电影列表展示 -->
      <div class="movie-list">
        <div 
          v-for="movie in allMovies" 
          :key="movie.mid" 
          class="movie-card"
          @click="goToMovieDetails(movie.mid)"
        >
          <img :src="getCoverUrl(movie.cover)" alt="Movie Cover" class="movie-cover" />
          <div class="movie-info">
            <h3>{{ movie.mname }}</h3>
            <p>时长: {{ movie.mtime }} 分钟</p>
            <p>热度: {{ movie.mhot }}</p>
            <p>评分: {{ movie.mscore }}</p>
            <p>上映时间: {{ movie.myear }}</p>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'AllMovies',
    setup() {
      const allMovies = ref([]);
      const router = useRouter();
  
      const fetchAllMovies = async () => {
        try {
          const response = await axios.get('http://localhost:8001/getmovies/');  
          allMovies.value = response.data;
        } catch (error) {
          console.error('获取所有电影失败:', error);
        }
      };
  
      // 获取封面图片的完整 URL
      const getCoverUrl = (coverPath) => {
        return `${'http://127.0.0.1:8001'}${coverPath}`;
      };
  
      onMounted(() => {
        fetchAllMovies();
      });

      const goToMovieDetails = (movieId) => {
      localStorage.setItem("mid", movieId);
      router.push(`/MovieDetails/`);
      };
  
      return {
        allMovies,
        getCoverUrl,
        goToMovieDetails
      };
    },
  };
  </script>
  
  <style scoped>
  .section {
    padding: 2rem;
    background-color: #f9f9f9;
    margin-top: 20vh;
  }
  
  h2 {
    font-size: 2rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 1rem;
  }
  
  .movie-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .movie-card {
    background-color: #ffffff;
    color: #333;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    border: 1px solid #e1e4e8;
  }
  
  .movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }
  
  .movie-card .movie-cover {
    width: 200px;
    height: 300px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 1rem;
  }
  
  .movie-card .movie-info h3 {
    font-size: 1.4rem;
    font-weight: 600;
    color: #2c3e50;
  }
  
  .movie-card .movie-info p {
    font-size: 1rem;
    color: #7f8c8d;
  }
  </style>
  