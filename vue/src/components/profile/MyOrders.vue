<template>
    <div>
      <!-- 订单信息展示 -->
        <section v-if="orders.length > 0" class="orders-list">
        <h2>我的订单</h2>
        <div v-for="(order, index) in orders" :key="index" class="order-item">
            <div class="order-info">
            <div class="order-details">
                <p><strong>订单时间:</strong> {{ formatDate(order.otime) }}</p>
                <p><strong>电影名称:</strong> {{ order.mname }}</p>
                <p><strong>影厅名称:</strong> {{ order.hname }}</p>
                <p><strong>影院名称:</strong> {{ order.cname }}</p>
            </div>
            <div class="order-seats">
                <p><strong>座位:</strong> {{ formatSeats(order.oseats) }}</p>
                <p><strong>花费:</strong> {{ order.oprice }} 元</p>
                <p><strong>开始时间:</strong> {{ formatDate(order.starttime) }}</p>
                <p><strong>电影时长:</strong> {{ order.mtime }} 分</p>
            </div>
            </div>
        </div>
        </section>

        <!-- 如果没有订单 -->
        <p v-else class="orders-list">您还没有订单。</p>

        <!-- 加载中 -->
        <p v-if="loading" class="loading">正在加载...</p>
    </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
    name: "MyOrders",
  setup() {
    const orders = ref([]); // 存储订单数据
    const loading = ref(true);

    const fetchOrders = async () => {
      const uid = localStorage.getItem('uid');
      try {
        const response = await axios.post(`http://127.0.0.1:8001/myorders/`, {
          uid
        });
        const ordersData = response.data.data;
        // 对订单按订单时间排序，订单时间越靠后的排的越靠前
         orders.value = ordersData.sort((a, b) => new Date(b.otime) - new Date(a.otime));
      } catch (error) {
        console.error('获取订单失败:', error);
      } finally {
        loading.value = false;
      }
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

    // 格式化座位信息
    const formatSeats = (seats) => {
      // 座位信息格式为 "r1,c1,r1,c2"
      const seatArray = seats.split(',');
      let seatList = [];
      for (let i = 0; i < seatArray.length - 1; i += 2) {
        seatList.push(`座位 ${seatArray[i].slice(1)} 行 ${seatArray[i + 1].slice(1)} 列`);
      }
      return seatList.join(', ');
    };

    // 页面加载时获取订单数据
    onMounted(() => {
        fetchOrders();
    });

    return {
      orders,
      loading,
      formatDate,
      formatSeats
    };
  },
};
</script>

<style scoped>
.my-orders {
  padding: 2rem;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.orders-list {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  margin-top: 20vh;
}

.order-item {
  background-color: #fff;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.order-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.order-details, .order-seats {
  width: 48%;
}

.order-details p, .order-seats p {
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.order-details p strong, .order-seats p strong {
  font-weight: bold;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  margin-top: 20vh;
}

</style>