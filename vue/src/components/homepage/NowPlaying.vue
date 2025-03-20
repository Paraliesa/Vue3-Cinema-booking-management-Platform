<template>
    <section class="section" ref="nowPlayingSection">
      <h2>正在热映</h2>
  
      <!-- 电影列表展示 -->
      <div class="movie-list">
        <div 
          v-for="movie in nowPlayingMovies" 
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
            <p>上映时间: {{ formatDate(movie.myear) }}</p>
          </div>
        </div>
      </div>
  
      <!-- 查看更多按钮 -->
      <div class="view-more">
        <button @click="viewMoreMovies">查看更多</button>
      </div>
    </section>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'NowPlaying',
    setup() {
      const router = useRouter();
      const nowPlayingMovies = ref([]);
  
      // 获取正在热映的电影列表
      const fetchNowPlayingMovies = async () => {
        try {
          const response = await axios.get('http://127.0.0.1:8001/now-playing/'); 
          nowPlayingMovies.value = response.data; 
        } catch (error) {
          console.error('获取正在热映电影失败:', error);
        }
      };
  
      // 格式化上映时间
      const formatDate = (dateString) => {
        const date = new Date(dateString);
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${month}-${day}-${date.getFullYear()}`;
      };
  
      // 跳转到电影详情页
      const goToMovieDetails = (movieId) => {
        localStorage.setItem("mid", movieId);
        router.push(`/MovieDetails/`);
      };
  
      // 查看更多电影
      const viewMoreMovies = () => {
        router.push(`/AllMovies/`);
      };
  
      const getCoverUrl = (coverPath) => {
        //console.log(`封面 URL: ${'http://127.0.0.1:8001'}${coverPath}`); 
        return `${'http://127.0.0.1:8001'}${coverPath}`;
      };
  
      // 在组件挂载时获取正在热映的电影列表
      onMounted(() => {
        fetchNowPlayingMovies();
      });
  
      return {
        nowPlayingMovies,
        formatDate,
        goToMovieDetails,
        viewMoreMovies,
        getCoverUrl,
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
  
  .movie-cover {
    width: 100%;
    height: auto;
    border-radius: 8px;
  }
  
  .movie-info {
    margin-top: 1rem;
  }
  
  .movie-info h3 {
    font-size: 1.4rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 0.5rem;
  }
  
  .movie-info p {
    font-size: 1rem;
    color: #7f8c8d;
    margin: 0.2rem 0;
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
  