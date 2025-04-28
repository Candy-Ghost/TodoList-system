<template>
  <a-layout>
    <a-layout-header style="background: #fff; padding: 0 24px">
      <a-space>
        <router-link to="/">首页</router-link>
        <a-button type="link" @click="handleLogout" danger>退出登录</a-button>
      </a-space>
    </a-layout-header>
    <a-layout-content style="padding: 24px">
      <router-view />
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const handleLogout = () => {
  localStorage.removeItem('token')
  message.success('已退出登录')
  router.push('/login')
}
</script>