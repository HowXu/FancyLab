import axios from "axios";
import { getToken, logout } from "./auth";
import { ElMessage } from "element-plus";
import router from "@/router";


const service = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 30000 // 30s
})

// config
service.interceptors.request.use(config => {
    const token = getToken()
    if (token != null) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config

}, error => {
    return Promise.reject(error)
})

// config
service.interceptors.response.use(res => {
    const data = res.data
    if (data.code !== 200) {
        ElMessage.error(data?.message || '请求失败')
        if (data.code === 401) {
            logout()
            router.push('/login')
            return Promise.reject(data)
        }
    }
    return data
}, error => {
    // 后端死了
    if (error.response) {
        const httpStatusCode = error.response.status
        if (httpStatusCode === 401) {
            ElMessage.error('登录状态失效')
            logout()
            router.push('/login')
        } else {
            ElMessage.error(error.response.data?.message || '请求失败')
        }
    } else {
        ElMessage.error('请检查后端服务')
    }
    return Promise.reject(error)
})

export default service
