<template>
    <div class="hall-details">
      <!-- 影厅信息展示 -->
      <section v-if="hallDetails && hallDetails.hname" class="hall-info">
        <h2>{{ hallDetails.cinemaname }}</h2>
        <h2>{{ hallDetails.hname }}</h2>
        <h2>{{ hallDetails.filmname }}</h2>

        <!-- 图例说明 -->
        <div class="legend">
          <span class="legend-item">
            <span class="legend-color t1"></span> 空座位
          </span>
          <span class="legend-item">
            <span class="legend-color t0"></span> 空地
          </span>
          <span class="legend-item">
            <span class="legend-color t2"></span> 已被预订座位
          </span>
          <span class="legend-item">
            <span class="legend-color t3"></span> 不可使用座位
          </span>
        </div>
  
        <!-- 座位布局网格 -->
        <div v-if="seats && seats.length > 0" class="seat-grid" :style="{ gridTemplateColumns: `repeat(${maxColumn}, 1fr)` }">
          <div
            v-for="(seat, index) in seats"
            :key="index"
            :class="['seat', seat.status]"
            :style="{ backgroundColor: seat.selected ? '#009b27': ''}"
            @click="toggleSeatSelection(seat)"
          >
            <span v-if="seat.status === 't1'"></span>
            <span v-if="seat.status === 't0'"></span>
            <span v-if="seat.status === 't3'"></span>
            <span v-if="seat.status === 't2'"></span>
          </div>
        </div>
      </section>

      <!-- 电影信息 -->
      <section class="movie-intro" v-if="hallDetails && hallDetails.filmname && hallDetails.cover">
        <div class="movie-cover">
            <img :src=getCoverUrl(hallDetails.cover) alt="Movie Cover" />
        </div>
        <div class="movie-info">
          <p><strong>{{ hallDetails.filmname }}</strong></p>
          <p>定价：{{ hallDetails.price }}元/人</p>
          <p>开始时间: {{ formatDate(hallDetails.starttime) }}</p>
          <p>结束时间: {{ formatDate(hallDetails.endtime) }}</p>
          
        </div>
      </section>
  
      <!-- 显示已选择的座位和应支付金额 -->
    <section class="payment-section" v-if="hallDetails && hallDetails.price">
      <h3>已选择 {{ tickets }} 个座位</h3>
      <ul>
        <li v-for="(seat, index) in selectedSeats" :key="index">
          座位 {{ seat.row }} 行 {{ seat.col }} 列
        </li>
      </ul>
      <p>应支付金额：{{ tickets * hallDetails.price }} 元</p>
      <button @click="processPayment" class="pay-button">立即支付</button>
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
      const tickets = ref(0);
      const selectedSeats = ref([]);
  
      // 获取影厅详细信息
      const fetchHallDetails = async () => {
        const fid = localStorage.getItem('fid'); 
        try {
          const response = await axios.post(`http://127.0.0.1:8001/purchase/`, fid);
          hallDetails.value = response.data;

          maxColumn.value = response.data.maxcolumn;
  
          // 解析座位布局
          if (hallDetails.value.smodel) {
            parseSeatLayout(hallDetails.value.smodel);
          }
  
        } catch (error) {
          console.error('获取影厅详情失败:', error);
          seats.value = [];
        } finally {
          loading.value = false;
        }
      };
  
      // 解析座位布局
      const parseSeatLayout = (layoutString) => {
        const seatArray = layoutString.split(',');
        seats.value = [];

        // 构造座位对象数组
        for (let i = 0; i < seatArray.length; i += 4) {
            const seat = {
            row: parseInt(seatArray[i].slice(1)),  // 'r1' -> 1
            col: parseInt(seatArray[i + 1].slice(1)),  // 'c1' -> 1
            status: seatArray[i + 2],  // 't1' -> 't1'
            occupied: seatArray[i + 3].slice(1),
            selected: false,
            };
            seats.value.push(seat);
        }

        // 对座位数组进行排序，先按row排序，如果row相同，再按col排序
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

      const getCoverUrl = (coverPath) => {
        return `${'http://127.0.0.1:8001'}${coverPath}`;
      };
  
      const toggleSeatSelection = (seat) => {
        const uid = localStorage.getItem('uid');
        if (seat.status === 't1') 
        { // 只允许选择空座位
            seat.selected = !seat.selected;
            if (seat.selected) {
            seat.status = 't2';
            seat.occupied = uid;
            tickets.value += 1;
            selectedSeats.value.push(seat);
            }
        }
        else if (seat.status === 't2' && seat.occupied === localStorage.getItem('uid'))
        {
            seat.selected = !seat.selected;
            seat.status = 't1';
            seat.occupied = '0';
            tickets.value -= 1;
            selectedSeats.value = selectedSeats.value.filter(s => s !== seat);
        }
      };


      // 处理支付
      const processPayment = async () => {
        try { 
            const updatedSeatLayout = seats.value.map(seat => {
                return `r${seat.row},c${seat.col},${seat.status},o${seat.occupied}`;
            }).join(',');  // 将所有座位拼接成一个字符串，传递给后端

            const occupiedSeats = seats.value.filter(seat => seat.occupied === localStorage.getItem('uid'))
                                         .map(seat => {
                                            return { row: seat.row, col: seat.col, t: seat.status, occupied: seat.occupied };
                                         });

            const fid = localStorage.getItem('fid');
            
            const uid = localStorage.getItem('uid');
            const response = await axios.post(`http://127.0.0.1:8001/updateSeatLayout/`, {
                uid,
                fid,
                updatedSeatLayout,
                occupiedSeats,
            });

            if (response.data.message === 'Seat layout updated successfully') 
            {
                const selectedSeatData = selectedSeats.value.map(seat => ({
                row: seat.row,
                col: seat.col,
            }));
                const response2 = await axios.post(`http://127.0.0.1:8001/createOrder/`, {
                    uid,
                    fid,
                    selectedSeatData,
                    tickets: tickets.value,
                });
                if (response2.data.message === 'Order created successfully') 
                {
                    alert('支付成功，请返回首页查看订单');
                    router.push('/');
                }
                else{
                    alert('一切都没有问题，但是订单没有创建成功');
                }

                
            } 
            else if (response.data.message === 'seats already been taken')
            {
                alert('您选择的座位已被其他人选择，请刷新页面重新选座');
            }
            else
            {
                alert('系统出现问题，请重试');
            }
        } catch (error) {
            console.error('系统出现问题:', error);
            alert('系统出现问题了，请重试');
        }
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
        maxColumn, 
        toggleSeatSelection,
        processPayment,
        tickets,
        getCoverUrl,
        selectedSeats,
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

.legend-color.t2 {
  background-color: #f5b7b1;
}

.legend-color.t3 {
  background-color: #000000; /* 无法使用座位背景色 */
}
  
  .seat-grid {
    display: grid;
    gap: 5px; /* 控制座位之间的间距 */
    justify-items: center; /* 水平居中每个座位 */
    margin-top: 20px;
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
  background-color: #000000; /* 无法使用的座位背景色 */
  }

  .seat.t2{
    background-color: #f5b7b1;
  }
  
  .loading {
    text-align: center;
    font-size: 1.2rem;
  }

  .payment-section {
  margin-top: 20px;
  text-align: center;
}

.pay-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.pay-button:hover {
  background-color: #45a049;
}

.movie-intro {
    margin-top: 2rem;
    display: flex;
    margin-bottom: 2rem;
  }
  
  .movie-cover img {
    width: 150px;
    height: 225px;
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
  </style>
  