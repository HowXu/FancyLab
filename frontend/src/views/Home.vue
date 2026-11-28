<template>
    <div>
        欢迎您 {{ userInfo?.name ?? '' }}
    </div>
</template>

<script setup lang="ts">
import { useUser } from '@/utils/user';

const { userInfo } = useUser()
</script>
