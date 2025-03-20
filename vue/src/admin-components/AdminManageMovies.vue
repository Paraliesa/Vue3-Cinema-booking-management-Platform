<template>
    <div class="admin-manage-movies">
      <h1>电影管理</h1>
  
      <div class="movie-list">
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else>
          <!--<button @click="openCreateMovieDialog" class="create-button">新建电影</button>-->
          
          <table v-if="movies.length">
            <thead>
              <tr>
                <th>电影名称</th>
                <th>封面</th>
                <th>时长</th>
                <th>上线时间</th>
                <th>评分</th>
                <th>热度</th>
                <th>类型</th>
                <th>来源</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="movie in movies" :key="movie.mid">
                <td>{{ movie.mname }}</td>
                <td>
                  <img :src="getCoverUrl(movie.cover)" alt="cover">
                </td>
                <td>{{ movie.mtime }} 分钟</td>
                <td>{{ movie.myear }}</td>
                <td>{{ movie.mscore }}</td>
                <td>{{ movie.mhot }}</td>
                <td>{{ movie.tname }}</td>
                <td>{{ movie.pname }}</td>
                <td>
                  <button @click="editMovie(movie)" class="edit-button">编辑</button>
                  <button @click="toggleMovieStatus(movie)" class="toggle-status-button">
                    {{ movie.m_active ? '禁用' : '启用' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
  
          <div v-if="movies.length === 0" class="no-movies">没有电影数据</div>
        </div>
      </div>
  
      <!-- 编辑/新建电影弹窗 -->
      <div v-if="showDialog" class="dialog-overlay">
        <div class="dialog">
          <h2>{{ isEdit ? '编辑电影' : '新建电影' }}</h2>
          <form @submit.prevent="submitMovieForm">
            <div class="form-group">
              <label for="mid">电影ID</label>
              <input v-model="movieForm.mid" type="text" id="mid" disabled />
            </div>
            <div class="form-group">
              <label for="mname">电影名称</label>
              <input v-model="movieForm.mname" type="text" id="mname" required />
            </div>
            <div class="form-group">
              <label for="mtime">电影时长 (分钟)</label>
              <input v-model="movieForm.mtime" type="number" id="mtime" required />
            </div>
            <div class="form-group">
              <label for="myear">上线时间</label>
              <input v-model="movieForm.myear" type="date" id="myear" required />
            </div>
            <div class="form-group">
              <label for="mscore">电影评分</label>
              <input v-model="movieForm.mscore" type="number" step="0.1" id="mscore" required />
            </div>
            <div class="form-group">
              <label for="mhot">电影热度</label>
              <input v-model="movieForm.mhot" type="number" id="mhot" required />
            </div>
            <div class="form-group">
                <label for="tname">电影类型</label>
                <select v-model="movieForm.tid" id="tname" required>
                <option v-for="type in movieTypes" :value="type.tid" :key="type.tid">
                    {{ type.tname }}
                </option>
                </select>
            </div>
            <div class="form-group">
                <label for="pname">电影来源</label>
                <select v-model="movieForm.pid" id="pname" required>
                <option v-for="place in moviePlaces" :value="place.pid" :key="place.pid">
                    {{ place.pname }}
                </option>
                </select>
            </div>
            <div class="form-group">
              <label for="mtext">简介</label>
              <textarea v-model="movieForm.mtext" id="mtext" required></textarea>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="submit-button">{{ isEdit ? '更新' : '创建' }}电影</button>
              <button @click="closeDialog" type="button" class="cancel-button">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  export default {
    name: 'AdminManageMovies',
    setup() {
      const movies = ref([]);
      const loading = ref(false);
      const showDialog = ref(false);
      const isEdit = ref(false);
      const movieTypes = ref(
        [
          { tid: 1, tname: '家庭' },
          { tid: 2, tname: '爱情' },
          { tid: 3, tname: '谍战' },
          { tid: 4, tname: '冒险' },
          { tid: 5, tname: '悬疑' },
        ]
      );
      const moviePlaces = ref(
        [
          { pid: 1, pname: '中国香港' },
          { pid: 2, pname: '中国大陆' },
          { pid: 3, pname: '美国' },
          { pid: 4, pname: '印度' },
        ]
      );
      const movieForm = ref({
        mid: null,
        mname: '',
        mtime: '',
        mscore: '',
        mhot: '',
        mtext: '',
        tname: null,
        pname: null,
        myear: null,
        pid: null,
        tid: null,
      });
  
      // 获取所有电影
      const fetchMovies = async () => {
        loading.value = true;
        try {
          const response = await axios.post('http://127.0.0.1:8001/admingetmovies/', { action: 'fetch' });
          movies.value = response.data.data;
        } catch (error) {
          console.error('获取电影失败:', error);
        } finally {
          loading.value = false;
        }
      };
  
      // 打开新建电影的弹窗
      const openCreateMovieDialog = () => {
        isEdit.value = false;
        movieForm.value = {
          mid: null,
          mname: '',
          mtime: '',
          mscore: '',
          mhot: '',
          mtext: '',
          tname: null,
          pname: null,
          myear: null,
          pid: null,
          tid: null,
        };
        showDialog.value = true;
      };

      const getCoverUrl = (coverPath) => {
        return `${'http://127.0.0.1:8001'}${coverPath}`;
      };
  
      // 打开编辑电影的弹窗
      const editMovie = (movie) => {
        isEdit.value = true;
        movieForm.value = { ...movie };
        showDialog.value = true;
      };
  
      // 提交电影表单
      const submitMovieForm = async () => {
        try {
          const action = isEdit.value ? 'edit' : 'create';
          await axios.post('http://127.0.0.1:8001/adminsubmovie/', {
            action,
            movie: movieForm.value,
          });
          fetchMovies();  // 刷新电影列表
          closeDialog();  // 关闭弹窗
        } catch (error) {
          console.error('操作失败:', error);
        }
      };
  
      // 切换电影状态 (启用/禁用)
      const toggleMovieStatus = async (movie) => {
        try {
          await axios.post('http://127.0.0.1:8001/admindisablemovie/', {
            action: 'toggleStatus',
            mid: movie.mid,
          });
          fetchMovies();  // 刷新电影列表
        } catch (error) {
          console.error('切换状态失败:', error);
        }
      };
  
      // 关闭弹窗
      const closeDialog = () => {
        showDialog.value = false;
      };
  
      // 初始化获取电影数据
      onMounted(() => {
        fetchMovies();
      });
  
      return {
        movies,
        loading,
        showDialog,
        isEdit,
        movieForm,
        fetchMovies,
        openCreateMovieDialog,
        editMovie,
        submitMovieForm,
        toggleMovieStatus,
        closeDialog,
        getCoverUrl,
        movieTypes,
        moviePlaces,
      };
    },
  };
  </script>
  
  <style scoped>
  .admin-manage-movies {
    padding: 2rem;
    background-color: #f9f9f9;
    margin-top: 20vh;
  }
  
  .create-button {
    margin-bottom: 1rem;
    padding: 0.5rem 1rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .create-button:hover {
    background-color: #45a049;
  }
  
  .loading {
    text-align: center;
    font-size: 1.2rem;
  }
  
  .no-movies {
    text-align: center;
    font-size: 1.2rem;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 0.75rem;
    text-align: left;
    border: 1px solid #ddd;
  }
  
  th {
    background-color: #f4f4f4;
  }
  
  button {
    padding: 0.5rem 1rem;
    margin: 0.2rem;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .edit-button {
    background-color: #4CAF50;
    color: white;
    border: none;
  }
  
  .edit-button:hover {
    background-color: #45a049;
  }
  
  .toggle-status-button {
    background-color: #ff9800;
    color: white;
    border: none;
  }
  
  .toggle-status-button:hover {
    background-color: #f57c00;
  }
  
  .dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  
  .dialog {
    background-color: white;
    padding: 2rem;
    border-radius: 5px;
    max-width: 600px;
    width: 100%;
  }
  
  form .form-group {
    margin-bottom: 1rem;
  }
  
  form .form-group label {
    display: block;
    font-weight: bold;
  }
  
  form .form-group input,
  form .form-group textarea {
    width: 100%;
    padding: 0.5rem;
    border-radius: 5px;
    border: 1px solid #ddd;
  }
  
  form .form-actions {
    display: flex;
    justify-content: space-between;
  }
  
  .submit-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
  }
  
  .cancel-button {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
  }
  </style>
  