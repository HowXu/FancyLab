import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/register',
            name: 'Register',
            component: () => import('@/layouts/Register.vue')
        },
        {
            path: '/login',
            name: 'Login',
            component: () => import('@/layouts/Login.vue')
        },
        {
            path: '/',
            name: 'Layout',
            component: ()=> import('@/layouts/Layout.vue'),
            children: [{
                path: 'home',
                name: 'Home',
                component: () => import('@/views/Home.vue')
            }, {
                path: 'lab',
                name: 'Lab',
                component: () => import('@/views/Lab.vue')
            }]
        }
    ],
})

export default router
