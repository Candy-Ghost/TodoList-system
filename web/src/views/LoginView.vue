<template>
  <a-card class="login-card">
    <a-tabs v-model:activeKey="activeKey">
      <a-tab-pane key="1" tab="登录">
        <a-form
          :model="formState"
          @finish="handleSubmit"
        >
          <a-form-item
            label="用户名"
            name="username"
            :rules="[{ required: true, message: '请输入用户名' }]"
          >
            <a-input v-model:value="formState.username" />
          </a-form-item>
          <a-form-item
            label="密码"
            name="password"
            :rules="[{ required: true, message: '请输入密码' }]"
          >
            <a-input-password v-model:value="formState.password" />
          </a-form-item>
          <a-button type="primary" html-type="submit" block>提交</a-button>
        </a-form>
      </a-tab-pane>
      
      <a-tab-pane key="2" tab="注册" force-render>
        <a-form
          :model="registerForm"
          @finish="handleRegister"
        >
          <a-form-item
            label="用户名"
            name="username"
            :rules="[{ required: true, message: '请输入用户名' }]"
          >
            <a-input v-model:value="registerForm.username" />
          </a-form-item>
          <a-form-item
            label="密码"
            name="password"
            :rules="[{ required: true, message: '请输入6-9位数字密码', pattern: /^\d{6,9}$/ }]"
          >
            <a-input-password v-model:value="registerForm.password" />
          </a-form-item>
          <a-form-item
            label="邮箱"
            name="email"
            :rules="[{ required: true, type: 'email', message: '请输入有效邮箱' }]"
          >
            <a-input v-model:value="registerForm.email" />
          </a-form-item>
          <a-button type="primary" html-type="submit" block>注册</a-button>
        </a-form>
      </a-tab-pane>
    </a-tabs>
  </a-card>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { message } from 'ant-design-vue'
import { api } from '@/utils/request'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeKey = ref('1')

const formState = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  password: '',
  email: ''
})

const handleSubmit = async () => {
  try {
    const { data } = await api.post('/login', {
      username: formState.username,
      password: formState.password
    })
    localStorage.setItem('token', data)
    await router.push('/')
  } catch (error) {
    message.error('登录失败')
  }
}

const handleRegister = async () => {
  try {
    await api.post('/enroll', registerForm)
    message.success('注册成功')
    activeKey.value = '1'
  } catch (error) {
    message.error('注册失败')
  }
}
</script>

<style scoped>
.login-card {
  max-width: 500px;
  margin: 100px auto;
  padding: 24px;
}
</style>