import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: '/questions',
      name: 'Questions',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Questions.vue')
    },
    {
      path: '/start-new-quiz-page' ,
      name: 'NewQuizPage',
      component: () => import('../views/NewQuizPage.vue')
    }
  ]
})

export default router
