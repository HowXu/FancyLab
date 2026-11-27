<template>
    <div>
        <el-container style='min-height: 100vh;'>
            <el-header style='display: flex;align-items: center; border-bottom: 1px sold #ddd; background-color: #fff;'>
                <div style="flex: 1;display: flex;align-items: center; font-size: 24px; font-weight: bold;">
                    <img src="@/assets/imgs/logo.png" alt="" style="width: 40px;border-radius: 0.5;">
                    <div style='margin-left: 5px;'>
                        实验室预约系统
                    </div>
                </div>
                <div>
                    <el-dropdown>
                        <div style="display: flex; align-items: center; cursor: pointer;">
                            <img src="@/assets/imgs/logo.png" style="width: 30px; border-radius: 50%;" alt="" />
                            <div style="margin-left: 3px;">管理员</div>
                        </div>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item @click='logout'>退出登录</el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </div>
            </el-header>
            <el-container>
                <el-aside width='220px'>
                    <el-menu router style="height: 100%" default-active="/home">
                        <el-menu-item index="/home">
                            <el-icon> <icon-menu /></el-icon>
                            <span>系统首页</span>
                        </el-menu-item>
                        <el-menu-item index="/lab">
                            <el-icon>
                                <House />
                            </el-icon>
                            <span>实验室管理</span>
                        </el-menu-item>
                        <el-menu-item index="/equ">
                            <el-icon>
                                <Setting />
                            </el-icon>
                            <span>设备列表管理</span>
                        </el-menu-item>
                        <el-menu-item index="/user">
                            <el-icon>
                                <User />
                            </el-icon>
                            <span>用户管理</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main><router-view /></el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script setup lang="ts">
import router from '@/router';
import { Menu as IconMenu, House, Setting, User } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus';

const logout = function () {
    ElMessage.success('您已退出登录')
    router.push('/login')
}
</script>
