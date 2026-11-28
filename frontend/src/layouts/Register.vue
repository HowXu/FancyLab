<template>
    <div class="register-container">
        <div class="register-box">
            <h1 style="font-size: 28px;"> 实验室预约系统</h1>
            <div style="margin-top: 5px; margin-bottom: 30px;">Work with Agent</div>
            <el-form ref="formRef" :rules="rules" :model='form' label-width="0px" style="width: 100%;">
                <el-form-item prop="username">
                    <el-input size="large" v-model="form.username" placeholder="请输入账号" :prefix-icon="User" />
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" size="large" v-model="form.password" placeholder="请输入密码"
                        :prefix-icon="Lock" show-password />
                </el-form-item>
                <el-form-item prop="confirmPassword">
                    <el-input type="password" size="large" v-model="form.confirmPassword" placeholder="请确认密码"
                        :prefix-icon="Lock" show-password />
                </el-form-item>
                <div> <el-button size="large" type="primary" style="width: 100%" @click="register"
                        :loading="loadingValue">注册</el-button>
                    <div style="text-align: right; margin-top: 20px;"> 已有账号? 请<router-link
                            style="color: var(--el-color-primary);" to="/login">登录</router-link>
                    </div>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { registerApi } from '@/api/auth';
import router from '@/router';
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage, type FormInstance, type FormItemRule } from 'element-plus';
import { reactive, ref } from 'vue';

const form = reactive({
    username: '',
    password: '',
    confirmPassword: ''
})

const formRef = ref<FormInstance>()

const validatePass: NonNullable<FormItemRule['validator']> = (_rule, value, callback) => {
    if (value === '') {
        callback(new Error('请确认密码'))
    }
    else {
        if (value !== form.password) {
            callback(new Error('两次密码输入不一致'))
        }
        else {
            callback()
        }
    }
}

const rules = {
    username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
    confirmPassword: [{ validator: validatePass, trigger: 'blur' }],
}

const loadingValue = ref(false)


const register = async function () {
    const valid = await formRef.value?.validate().catch(() => false)
    if (!valid) return
    loadingValue.value = true
    try {
        const response = await registerApi({
            username: form.username,
            password: form.password,
            name: form.username
        })
        if (response.code === 200) {
            ElMessage.success('注册成功')
            await router.push('/login')
        }

    } finally {
        loadingValue.value = false
    }
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
