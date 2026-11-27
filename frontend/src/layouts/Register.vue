<template>
    <div class="register-container">
        <div class="register-box">
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
                <el-form-item>
                    <el-input type="password" size="large" v-model="form.confirmPassword" placeholder="请确认密码"
                        :prefix-icon="Lock" show-password />
                </el-form-item>
                <div> <el-button size="large" type="primary" style="width: 100%" @click="register"
                        :loading="loadingValue">注册</el-button>
                    <div style="text-align: right; margin-top: 20px;"> 已有账号? 请<a style="color: var(--el-color-primary);"
                            href="/login">登录</a></div>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script setup lang="ts">
import router from '@/router';
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus';
import { reactive, ref } from 'vue';

const form = reactive({
    username: '',
    password: '',
    confirmPassword: ''
})

const loadingValue = ref(false)

const register = function () {
    loadingValue.value = true
    setTimeout(() => {
        loadingValue.value = false
        ElMessage.success('账号创建成功')
        router.push('/login')

    }, 2000)
}
</script>

<style lang="css" scoped>
.register-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.register-box {
    width: 380px;
    border-radius: 8px;
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);

    padding: 30px;
    text-align: center;
    background-color: white;
}
</style>
