<template>
  <a-layout class="container">
    <a-layout-content class="content">
      <a-space direction="vertical" style="width: 100%">
        <a-button type="primary" @click="showModal">新建任务</a-button>
        
        <a-radio-group v-model:value="filterStatus" @change="fetchTodos">
          <a-radio-button value="all">全部</a-radio-button>
          <a-radio-button value="finished">已完成</a-radio-button>
          <a-radio-button value="unfinished">未完成</a-radio-button>
        </a-radio-group>

        <a-table
          :columns="columns"
          :data-source="todos"
          :pagination="false"
          rowKey="id"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'state'">
              <a-tag :color="record.state === '已完成' ? 'green' : 'volcano'">
                {{ record.state }}
              </a-tag>
            </template>
            
            <template v-if="column.key === 'action'">
              <a-space>
                <a-button size="small" @click="handleEdit(record)">编辑</a-button>
                <a-popconfirm
                  title="确认删除吗？"
                  @confirm="handleDelete(record.id)"
                >
                  <a-button size="small" danger>删除</a-button>
                </a-popconfirm>
                <a-button 
                  v-if="record.state !== '已完成'"
                  type="link"
                  @click="markComplete(record.id)"
                >
                  标记完成
                </a-button>
              </a-space>
            </template>
          </template>
        </a-table>
      </a-space>
    </a-layout-content>
  </a-layout>

  <a-modal
    v-model:open="visible"
    :title="currentTodo ? '编辑任务' : '新建任务'"
    @ok="handleSubmit"
    @cancel="resetForm"
  >
    <a-form
      :model="formState"
      :label-col="{ span: 4 }"
    >
      <a-form-item label="标题" required>
        <a-input v-model:value="formState.title" />
      </a-form-item>
      <a-form-item label="内容">
        <a-textarea v-model:value="formState.content" />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { api } from '@/utils/request'

type Todo = {
  id: number
  title: string
  content: string
  state: string
  created_at: string
}

const columns = [
  { title: '标题', dataIndex: 'title' },
  { title: '内容', dataIndex: 'content' },
  { title: '状态', key: 'state' },
  { title: '创建时间', dataIndex: 'created_at' },
  { title: '操作', key: 'action' }
]

const todos = ref<Todo[]>([])
const visible = ref(false)
const currentTodo = ref<Todo | null>(null)
const filterStatus = ref('all')

const formState = reactive({
  title: '',
  content: ''
})

const fetchTodos = async () => {
  try {
    const endpoint = filterStatus.value === 'finished' 
      ? '/finish' 
      : filterStatus.value === 'unfinished'
      ? '/NO_finish'
      : '/'
    const { data } = await api.get(endpoint)
    todos.value = data
  } catch (error) {
    message.error('获取数据失败')
  }
}

const showModal = () => {
  visible.value = true
}

const handleEdit = (record: Todo) => {
  currentTodo.value = record
  formState.title = record.title
  formState.content = record.content
  visible.value = true
}

const handleSubmit = async () => {
  try {
    if (currentTodo.value) {
      await api.put(`/uptodo/${currentTodo.value.id}`, formState)
      message.success('更新成功')
    } else {
      await api.post('/add', formState)
      message.success('创建成功')
    }
    resetForm()
    await fetchTodos()
  } catch (error) {
    message.error('操作失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await api.delete(`/del/${id}`)
    message.success('删除成功')
    await fetchTodos()
  } catch (error) {
    message.error('删除失败')
  }
}

const markComplete = async (id: number) => {
  try {
    await api.put(`/uptodo/${id}`, { state: '已完成' })
    message.success('标记完成')
    await fetchTodos()
  } catch (error) {
    message.error('操作失败')
  }
}

const resetForm = () => {
  visible.value = false
  currentTodo.value = null
  formState.title = ''
  formState.content = ''
}

onMounted(() => {
  fetchTodos()
})
</script>

<style scoped>
.container {
  padding: 24px;
  min-height: 100vh;
}
.content {
  max-width: 1200px;
  margin: 0 auto;
}
</style>