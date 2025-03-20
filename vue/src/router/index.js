import { createRouter, createWebHistory } from 'vue-router';
import { useHeaderStore } from '../stores/header';
import HomePage from '../components/homepage/HomePage.vue';
import LoginPage from '../components/login&register/LoginPage.vue';
import RegisterPage from '../components/login&register/RegisterPage.vue';
import AllTheaters from '../components/theaters/AllTheaters.vue';
import HallDetails from '../components/theaters/HallDetails.vue';
import SingleTheater from '../components/theaters/SingleTheater.vue';
import AllMovies from '../components/movies/AllMovies.vue';
import MovieDetails from '../components/movies/MovieDetails.vue';
import MyOrders from '../components/profile/MyOrders.vue';
import ProfilePage from '../components/profile/ProfilePage.vue';
import BookingPage from '../components/theaters/BookingPage.vue';
import AdminCheckOrders from '../admin-components/AdminCheckOrders.vue';
import AdminManageCinemas from '../admin-components/AdminManageCinemas.vue';
import AdminManageMovies from '../admin-components/AdminManageMovies.vue';
import AdminManageScheduling from '../admin-components/AdminManageScheduling.vue';
import AdminPage from '../admin-components/AdminPage.vue';


const routes = [
  {
    path: '/',
    name: 'Homepage',
    component: HomePage, 
  },
  {
    path: '/LoginPage',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/RegisterPage',
    name: 'RegisterPage',
    component: RegisterPage,
  },
  {
    path: '/AllTheaters',
    name: 'AllTheaters',
    component: AllTheaters,
  },
  {
    path: '/HallDetails',
    name: 'HallDetails',
    component: HallDetails,
  },
  {
    path: '/SingleTheater',
    name: 'SingleTheater',
    component: SingleTheater,
  },
  {
    path: '/AllMovies',
    name: 'AllMovies',
    component: AllMovies,
  },
  {
    path: '/MovieDetails',
    name: 'MovieDetails',
    component: MovieDetails,
  },
  {
    path: '/MyOrders',
    name: 'MyOrders',
    component: MyOrders,
  },
  {
    path: '/ProfilePage',
    name: 'ProfilePage',
    component: ProfilePage,
  },
  {
    path: '/BookingPage',
    name: 'BookingPage',
    component: BookingPage,
  },
  {
    path: '/AdminCheckOrders',
    name: 'AdminCheckOrders',
    component: AdminCheckOrders,
  },
  {
    path: '/AdminManageCinemas',
    name: 'AdminManageCinemas',
    component: AdminManageCinemas,
  },
  {
    path: '/AdminManageMovies',
    name: 'AdminManageMovies',
    component: AdminManageMovies,
  },
  {
    path: '/AdminManageScheduling',
    name: 'AdminManageScheduling',
    component: AdminManageScheduling,
  },
  {
    path: '/AdminPage',
    name: 'AdminPage',
    component: AdminPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next)=>{
  const store = useHeaderStore();
  console.log(to.name)
  // 如果目标路由是登录页或者注册页，则将 needHeader 设为 0
  if (to.name === 'LoginPage' || to.name === 'RegisterPage') {
    store.setNeedHeader('0');
  } else {
    store.setNeedHeader('1');
  }

  // 必须调用 next() 才能继续导航
  next();
})

export default router;
