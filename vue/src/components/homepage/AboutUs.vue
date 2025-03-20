<template>
    <footer class="footer">
      <div class="container">
        <!-- 第一部分 -->
        <div class="section">
          <h2 class="title">Cinema Distribution Zone</h2>
          <p class="subtitle">关于我们</p>
        </div>
  
        <!-- 第二部分 -->
        <div class="section">
          <h3 class="section-title">选座购票流程</h3>
          <ul class="process">
            <li>选择影片和场次</li>
            <li>选择中意的座位</li>
            <li>支付并收到取票短信</li>
          </ul>
        </div>
  
        <!-- 第三部分 -->
        <div class="section">
          <h3 class="section-title">常见问题</h3>
          <ul class="faq">
            <li><a href="javascript:void(0);">是否支持退换票</a></li>
            <li><a href="javascript:void(0);">填错手机号怎么办</a></li>
            <li><a href="javascript:void(0);">更多问题 >></a></li>
          </ul>
        </div>
      </div>
    </footer>
  </template>
  
  <style scoped>
  .footer {
    background-color: #f5f5f5; 
    padding: 3rem 1.5rem;
    color: #333;
    font-family: '明黑', '微软雅黑', sans-serif; 
  }
  
  .container {
    display: flex;
    justify-content: space-between; 
    align-items: flex-start; 

    margin: 0 auto;
    gap: 10rem; 
  }
  
  .section {
    flex: 1; 
    text-align: left;
  }
  
  .title {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
    color: #555;
  }
  
  .section-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  
  .process, .faq {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .process li {
    margin-bottom: 0.5rem;
    color: #666;
    font-size: 1rem;
  }
  
  .faq li {
    margin-bottom: 0.5rem;
  }
  
  .faq a {
    text-decoration: none;
    color: #007BFF;
    font-size: 1rem;
    transition: color 0.3s ease;
  }
  
  .faq a:hover {
    color: #0056b3;
  }

  @media (max-width: 768px) {
  .container {
    flex-direction: column; 
    text-align: center;
    gap: 1rem;
  }

  .section {
    margin-bottom: 0rem;
  }
}
  </style>
  