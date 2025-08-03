<template>
  <v-container>
    <h1 class="text-h5 mb-4">Device Monitor Dashboard</h1>
    <v-data-table
      :headers="headers"
      :items="devices"
      :loading="loading"
      item-value="name"
      class="elevation-1"
    >
      <template #item.status="{ item }">
        <v-chip :color="item.status === 'online' ? 'green' : 'red'" dark>
          {{ item.status }}
        </v-chip>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Status', key: 'status' },
  { title: 'CPU Usage (%)', key: 'cpu' },
  { title: 'Temperature (°C)', key: 'temperature' },
]

const devices = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await axios.get('http://localhost:8000/api/devices')
    devices.value = res.data
  } catch (err) {
    console.error('Failed to fetch devices:', err)
  } finally {
    loading.value = false
  }
})
</script>
