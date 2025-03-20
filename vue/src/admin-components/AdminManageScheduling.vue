<template>
    <div class="admin-manage-scheduling">
      <h1>排片管理</h1>
    
      <div class="scheduling-list">
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else>
          <button @click="openCreateSchedulingDialog" class="create-button">新建排片</button>
          
          <table v-if="schedules.length">
            <thead>
              <tr>
                <th>排片编号</th>
                <th>影院</th>
                <th>影厅</th>
                <th>电影</th>
                <th>开播时间</th>
                <th>结束时间</th>
                <th>定价</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="schedule in schedules" :key="schedule.sid">
                <td>{{ schedule.sid }}</td>
                <td>{{ schedule.cinema }}</td>
                <td>{{ schedule.hall }}</td>
                <td>{{ schedule.movie }}</td>
                <td>{{ schedule.start_time }}</td>
                <td>{{ schedule.end_time }}</td>
                <td>{{ schedule.price }} 元</td>
                <td>
                  <button @click="editScheduling(schedule)" class="edit-button">编辑</button>
                  <button @click="toggleSchedulingStatus(schedule)" class="toggle-status-button">
                    {{ schedule.f_active ? '禁用' : '启用' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
    
          <div v-if="schedules.length === 0" class="no-schedules">没有排片数据</div>
        </div>
      </div>
    
      <!-- 编辑/新建排片弹窗 -->
      <div v-if="showDialog" class="dialog-overlay">
        <div class="dialog">
          <h2>{{ isEdit ? '编辑排片' : '新建排片' }}</h2>
          <form @submit.prevent="submitSchedulingForm">
            <div class="form-group">
              <label for="sid">排片编号</label>
              <input v-model="schedulingForm.sid" type="text" id="sid" disabled />
            </div>
            <div class="form-group">
              <label for="cinema">影院</label>
              <input 
                    v-model="schedulingForm.cinema" 
                    type="text" 
                    id="cinema"
                    :required="!isEdit" 
                    :disabled="isEdit" 
                />
            </div>
            <div class="form-group">
              <label for="hall">影厅</label>
              <input 
                    v-model="schedulingForm.hall" 
                    type="text" 
                    id="hall"
                    :required="!isEdit" 
                    :disabled="isEdit" 
                />
            </div>
            <div class="form-group">
              <label for="movie">电影</label>
              <input v-model="schedulingForm.movie" type="text" id="movie" :required="!isEdit" 
              :disabled="isEdit" />
            </div>
            <div class="form-group">
              <label for="start_time">开播时间</label>
              <input v-model="schedulingForm.start_time" type="datetime-local" id="start_time" required />
            </div>
            <div class="form-group">
              <label for="end_time">结束时间</label>
              <input v-model="schedulingForm.end_time" type="datetime-local" id="end_time" required />
            </div>
            <div class="form-group">
              <label for="price">定价 (元)</label>
              <input v-model="schedulingForm.price" type="number" step="0.1" id="price" required />
            </div>
            <div class="form-actions">
              <button type="submit" class="submit-button">{{ isEdit ? '更新' : '创建' }}排片</button>
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
    name: 'AdminManageScheduling',
    setup() {
      const schedules = ref([]);
      const loading = ref(false);
      const showDialog = ref(false);
      const isEdit = ref(false);
      const schedulingForm = ref({
        sid: null,
        cinema: '',
        hall: '',
        movie: '',
        start_time: '',
        end_time: '',
        price: '',
        f_active: true,
      });
  
      // 获取所有排片数据
      const fetchSchedules = async () => {
        loading.value = true;
        try {
          const response = await axios.post('http://127.0.0.1:8001/admingetschedules/', { action: 'fetch' });
          schedules.value = response.data.data;
        } catch (error) {
          console.error('获取排片数据失败:', error);
        } finally {
          loading.value = false;
        }
      };
  
      // 打开新建排片的弹窗
      const openCreateSchedulingDialog = () => {
        isEdit.value = false;
        schedulingForm.value = {
          sid: null,
          cinema: '',
          hall: '',
          movie: '',
          start_time: '',
          end_time: '',
          price: '',
          f_active: false,
        };
        showDialog.value = true;
      };
  
      // 打开编辑排片的弹窗
      const editScheduling = (schedule) => {
        isEdit.value = true;
        schedulingForm.value = { ...schedule };
        showDialog.value = true;
      };
  
      // 提交排片表单
      const submitSchedulingForm = async () => {
        try {
          const action = isEdit.value ? 'edit' : 'create';
          await axios.post('http://127.0.0.1:8001/adminsubschedule/', {
            action,
            schedule: schedulingForm.value,
          });
          fetchSchedules();  // 刷新排片列表
          closeDialog();  // 关闭弹窗
        } catch (error) {
          console.error('操作失败:', error);
        }
      };
  
      // 切换排片状态 (启用/禁用)
      const toggleSchedulingStatus = async (schedule) => {
        try {
          await axios.post('http://127.0.0.1:8001/admindisableschedule/', {
            action: 'toggleStatus',
            sid: schedule.sid,
          });
          fetchSchedules();  // 刷新排片列表
        } catch (error) {
          console.error('切换状态失败:', error);
        }
      };
  
      // 关闭弹窗
      const closeDialog = () => {
        showDialog.value = false;
      };
  
      // 初始化获取排片数据
      onMounted(() => {
        fetchSchedules();
      });
  
      return {
        schedules,
        loading,
        showDialog,
        isEdit,
        schedulingForm,
        fetchSchedules,
        openCreateSchedulingDialog,
        editScheduling,
        submitSchedulingForm,
        toggleSchedulingStatus,
        closeDialog,
      };
    },
  };
  </script>
  
  <style scoped>
  .admin-manage-scheduling {
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
  
  .no-schedules {
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
    width: 80%;
    max-width: 600px;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    font-weight: bold;
  }
  
  input {
    width: 100%;
    padding: 0.5rem;
    margin-top: 0.2rem;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
  }
  
  .submit-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
  }
  
  .cancel-button {
    background-color: #ccc;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
  }
  </style>
  