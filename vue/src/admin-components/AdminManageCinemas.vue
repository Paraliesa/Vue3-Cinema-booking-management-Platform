<template>
    <div class="admin-manage-cinemas">
      <h1>电影院和影厅管理</h1>
  
      <div class="cinema-list">
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else>
          <!--<button @click="openCreateCinemaDialog" class="create-button">新建电影院</button>-->
          
          <table v-if="cinemas.length">
            <thead>
              <tr>
                <th>电影院名称</th>
                <th>影厅名称</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cinema in cinemas" :key="cinema.cid">
                <td>{{ cinema.cname }}</td>
                <td>{{ cinema.hall_name }}</td>
                <td>
                  <!--<button @click="editCinema(cinema)" class="edit-button">编辑</button>-->
                  <button @click="deleteCinema(cinema)" class="delete-button">{{ cinema.h_active ? '禁用' : '启用' }}</button>
                </td>
              </tr>
            </tbody>
          </table>
  
          <div v-if="cinemas.length === 0" class="no-cinemas">没有电影院数据</div>
        </div>
      </div>
  
      <!-- 编辑/新建电影院弹窗 -->
      <div v-if="showDialog" class="dialog-overlay">
        <div class="dialog">
          <h2>{{ isEdit ? '编辑电影院' : '新建电影院' }}</h2>
          <form @submit.prevent="submitCinemaForm">
            <div class="form-group">
              <label for="cid">电影院ID</label>
              <input v-model="cinemaForm.cid" type="text" id="cid" disabled />
            </div>
            <div class="form-group">
              <label for="cname">电影院名称</label>
              <input v-model="cinemaForm.cname" type="text" id="cname" required />
            </div>
            <div class="form-group">
              <label for="hall-name">影厅名称</label>
              <input v-model="cinemaForm.hall_name" type="text" id="hall-name" required />
            </div>
            <div class="form-actions">
              <button type="submit" class="submit-button">{{ isEdit ? '更新' : '创建' }}电影院</button>
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
    name: 'AdminManageCinemas',
    setup() {
      const cinemas = ref([]);  // 影院数据列表
      const loading = ref(false);  // 加载状态
      const showDialog = ref(false);  // 弹窗状态
      const isEdit = ref(false);  // 是否编辑
      const cinemaForm = ref({
        cid: null,
        cname: '',
        hall_name: '',
      });
  
      // 获取所有电影院数据
      const fetchCinemas = async () => {
        loading.value = true;
        try {
          const response = await axios.post('http://127.0.0.1:8001/admingetcinemas/');
          cinemas.value = response.data.data;
        } catch (error) {
          console.error('获取电影院数据失败:', error);
        } finally {
          loading.value = false;
        }
      };
  
      // 打开新建电影院弹窗
      const openCreateCinemaDialog = () => {
        isEdit.value = false;
        cinemaForm.value = { cid: null, cname: '', hall_name: '' };
        showDialog.value = true;
      };
  
      // 打开编辑电影院弹窗
      const editCinema = (cinema) => {
        isEdit.value = true;
        cinemaForm.value = { ...cinema };
        showDialog.value = true;
      };
  
      // 提交电影院表单
      const submitCinemaForm = async () => {
        try {
          const action = isEdit.value ? 'edit' : 'create';
          await axios.post('http://127.0.0.1:8001/submcinema/', {
            action,
            cinema: cinemaForm.value,
          });
          fetchCinemas();  // 刷新电影院列表
          closeDialog();  // 关闭弹窗
        } catch (error) {
          console.error('操作失败:', error);
        }
      };
  
      // 删除电影院
      const deleteCinema = async (cinema) => {
          try {
            await axios.post('http://127.0.0.1:8001/admindelcinema/', {
              cid: cinema.cid,
            });
            fetchCinemas();  // 删除后刷新列表
          } catch (error) {
            console.error('禁用电影厅失败:', error);
          
        }
      };
  
      // 关闭弹窗
      const closeDialog = () => {
        showDialog.value = false;
      };
  
      // 初始化获取电影院数据
      onMounted(() => {
        fetchCinemas();
      });
  
      return {
        cinemas,
        loading,
        showDialog,
        isEdit,
        cinemaForm,
        fetchCinemas,
        openCreateCinemaDialog,
        editCinema,
        submitCinemaForm,
        deleteCinema,
        closeDialog,
      };
    },
  };
  </script>
  
  <style scoped>
  .admin-manage-cinemas {
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
  
  .no-cinemas {
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
  
  .delete-button {
    background-color: #f44336;
    color: white;
    border: none;
  }
  
  .delete-button:hover {
    background-color: #e53935;
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
  
  form .form-group input {
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
  