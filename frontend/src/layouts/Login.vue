<template>
    <div class="login-container">
        <div class="login-box">
            <h1 style="font-size: 28px;"> 实验室预约系统</h1>
            <div style="margin-top: 5px; margin-bottom: 30px;">Work with Agent</div>
            <el-form :model='form' label-width="auto" style="max-width: 600px;">
                <el-form-item>
                    <el-input size="large" v-model="form.username" placeholder="请输入账号" :prefix-icon="User" />
                </el-form-item>
                <el-form-item>
                    <el-input type="password" size="large" v-model="form.password" placeholder="请输入密码"
                        :prefix-icon="Lock" show-password />
                </el-form-item>
                <div> <el-button size="large" type="primary" style="width: 100%" @click="login"
                        :loading="loadingValue">登录</el-button>
                    <div style="text-align: right; margin-top: 20px;"> 还没有账号? 请<a
                            style="color: var(--el-color-primary);" href="/register">注册</a></div>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { loginApi } from '@/api/auth';
import router from '@/router';
import { useUser } from '@/utils/user';
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus';
import { reactive, ref } from 'vue';

const form = reactive({
    username: '',
    password: ''
})

const { saveLoginData } = useUser()
const loadingValue = ref(false)

const login = async function () {
    loadingValue.value = true
    const response = await loginApi(form)
    loadingValue.value = false
    if (response.code === 200 && response.data !== null) {
        saveLoginData(response.data)
        ElMessage.success('登录成功')
        router.push('/home')
    }
}
</script>

<style lang="css" scoped>
.login-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.login-box {
    width: 380px;
    border-radius: 8px;
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);

    padding: 30px;
    text-align: center;
    background-color: white;
}
</style>
