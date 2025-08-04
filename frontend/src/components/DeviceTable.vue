<!-- src/components/DeviceTable.vue -->
<template>
  <v-container>
    <h1 class="text-h5 mb-4">Device Monitor Dashboard</h1>

    <!-- Filters -->
    <v-row class="mb-4" dense>
      <v-col cols="12" sm="4">
        <v-text-field v-model="search" label="Search by name or status" clearable />
      </v-col>
    </v-row>

    <!-- Data Table -->
    <v-data-table
      :headers="headers"
      :items="filteredDevices"
      :loading="loading"
      item-value="name"
      class="elevation-1"
      @click:row="(_, row) => openDetails(row.item)"
    >
      <template #item.status="{ item }">
        <v-chip :color="item.status === 'online' ? 'green' : 'red'" dark>
          {{ item.status }}
        </v-chip>
      </template>
    </v-data-table>

    <!-- Device Details Dialog -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card v-if="selectedDevice">
        <v-card-title class="headline">{{ selectedDevice.name }}</v-card-title>
        <v-card-text>
          <p><strong>Status:</strong> {{ selectedDevice.status }}</p>
          <p><strong>CPU Usage:</strong> {{ selectedDevice.cpu }}%</p>
          <p><strong>Temperature:</strong> {{ selectedDevice.temperature }}°C</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" text @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const headers = [
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'CPU Usage (%)', key: 'cpu', sortable: true },
  { title: 'Temperature (°C)', key: 'temperature', sortable: true },
]

const devices = ref([])
const loading = ref(false)
const search = ref('')
const dialog = ref(false)
const selectedDevice = ref(null)

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

const filteredDevices = computed(() => {
  if (!search.value) return devices.value
  const keyword = search.value.toLowerCase()
  return devices.value.filter(
    (d) => d.name.toLowerCase().includes(keyword) || d.status.toLowerCase().includes(keyword),
  )
})

const openDetails = (device) => {
  selectedDevice.value = device
  dialog.value = true
}
</script>
