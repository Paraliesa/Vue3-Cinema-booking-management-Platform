<template>
    <div class="hall-details">
      <!-- 影厅信息展示 -->
      <section v-if="hallDetails && hallDetails.hname" class="hall-info">
        <h2>{{ hallDetails.hname }} - 影厅布局</h2>

        <!-- 图例说明 -->
        <div class="legend">
          <span class="legend-item">
            <span class="legend-color t1"></span> 座位
          </span>
          <span class="legend-item">
            <span class="legend-color t0"></span> 空地
          </span>
        </div>
  
        <!-- 座位布局网格 -->
        <div class="seat-grid" :style="{ gridTemplateColumns: `repeat(${maxColumn}, 1fr)` }">
          <div
            v-for="(seat, index) in seats"
            :key="index"
            :class="['seat', seat.status]"
          >
            <span v-if="seat.status === 't1'"></span>
            <span v-if="seat.status === 't0'"></span>
            <span v-if="seat.status === 't3'"></span>
          </div>
        </div>
      </section>
  
      <!-- 排片安排 -->
      <section v-if="hallDetails && hallDetails.arrangements.length > 0" class="arrangements">
        <h3>近期排片</h3>
        <ul>
          <li v-for="arrangement in hallDetails.arrangements" :key="arrangement.fid">
            <strong>{{ arrangement.mname }}</strong> -
            <span>{{ formatDate(arrangement.fstarttime) }} ~ {{ formatDate(arrangement.fendtime) }}</span>
            <button @click="goToBookingPage(arrangement.fid)">立即订票</button>
          </li>
        </ul>
      </section>
  
      <!-- 加载中 -->
      <p v-if="loading" class="loading">正在加载...</p>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'HallDetails',
    setup() {
      const router = useRouter();
      const hallDetails = ref(null); // 影厅详情
      const loading = ref(true); // 加载状态
      const seats = ref([]); // 座位布局
      const maxColumn = ref(0); 
  
      // 获取影厅详细信息
      const fetchHallDetails = async () => {
        const hallId = localStorage.getItem('hallId'); // 从 localStorage 获取影厅ID
        try {
          const response = await axios.post(`http://127.0.0.1:8001/get_hall_details/`, hallId);
          hallDetails.value = response.data;

          maxColumn.value = response.data.maxcolumn;
  
          // 解析座位布局
          if (hallDetails.value.smodel) {
            parseSeatLayout(hallDetails.value.smodel);
          }
  
        } catch (error) {
          console.error('获取影厅详情失败:', error);
        } finally {
          loading.value = false;
        }
      };
  
      // 解析座位布局
      const parseSeatLayout = (layoutString) => {
        const seatArray = layoutString.split(',');
        seats.value = [];
        for (let i = 0; i < seatArray.length; i += 4) {
          const seat = {
            row: seatArray[i].slice(1), // 'r1' -> 1
            col: seatArray[i + 1].slice(1), // 'c1' -> 1
            status: seatArray[i + 2], // 't1' -> 't1'
          };
          seats.value.push(seat);
        }
        seats.value.sort((a, b) => {
            if (a.row === b.row) {
            return a.col - b.col;  // 如果row相同，按col排序
            }
            return a.row - b.row;  // 否则按row排序
        });
      };
  
      // 格式化时间
      const formatDate = (datetime) => {
        const date = new Date(datetime);
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const hours = date.getHours();
        const minutes = date.getMinutes();
        return `${month}-${day} ${hours}:${minutes < 10 ? '0' + minutes : minutes}`;
      };
  
      // 跳转到订票页面
      const goToBookingPage = (fid) => {
        localStorage.setItem('fid', fid);
        router.push(`/BookingPage/`);
      };
  
      // 在组件挂载时获取影厅信息
      onMounted(() => {
        fetchHallDetails();
      });
  
      return {
        hallDetails,
        loading,
        seats,
        formatDate,
        goToBookingPage,
        maxColumn, 
      };
    },
  };
  </script>
  
  <style scoped>
  .hall-details {
    padding: 2rem;
    background-color: #f9f9f9;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

  }
  
  .hall-info {
    margin-top: 20vh;
  }
  
  .hall-info h2 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  /* 图例样式 */
.legend {
  display: flex;
  gap: 1rem;
  margin-top: 10px;
  font-size: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
}

.legend-color {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  margin-right: 5px;
}

.legend-color.t1 {
  background-color: #a2d1a4; /* 空座位背景色 */
}

.legend-color.t0 {
  background-color: #e0e0e0; /* 空地背景色 */
}

.legend-color.t3 {
  background-color: #f5b7b1; /* 无法使用座位背景色 */
}
  
  .seat-grid {
    display: grid;
    gap: 5px; /* 控制座位之间的间距 */
    justify-items: center; /* 水平居中每个座位 */
    margin-top: 20px;
    pointer-events: none; /* 禁止点击 */
  }
  
  .seat {
    width: 30px;  /* 增加紧凑度，减小每个座位的宽度 */
    height: 30px;  /* 增加紧凑度，减小每个座位的高度 */
    background-color: #f0f0f0;
    text-align: center;
    line-height: 30px;
    border-radius: 5px;
    font-size: 12px; /* 适应较小的座位 */
  }
  
  .seat.t1 {
    background-color: #a2d1a4; /* 空座位背景色 */
  }
  
  .seat.t0 {
    background-color: #e0e0e0; /* 空地背景色 */
  }

  .seat.t3 {
  background-color: #f16053; /* 无法使用的座位背景色 */
  }
  
  .arrangements h3 {
    font-size: 1.5rem;
    font-weight: bold;
    margin-top: 2rem;
  }
  
  .arrangements ul {
    list-style-type: none;
    padding-left: 0;
  }
  
  .arrangements li {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }
  
  .arrangements button {
    margin-left: 10px;
    padding: 5px 10px;
    background-color: #ff5722;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .arrangements button:hover {
    background-color: #e64a19;
  }
  
  .loading {
    text-align: center;
    font-size: 1.2rem;
  }
  </style>
  