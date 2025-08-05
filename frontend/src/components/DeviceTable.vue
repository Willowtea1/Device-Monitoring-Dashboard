<template>
  <v-container>
    <h1 class="text-h5 mb-4">Device Monitor Dashboard</h1>

    <v-row class="mb-4" dense align="center">
      <!-- Search Box -->
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="search"
          placeholder="Search"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
          class="search-bar align-self-end"
          density="compact"
          hide-details
          rounded="pill"
        />
      </v-col>

      <!-- Sort & Filter Pills -->
      <v-col cols="12" sm="6" class="d-flex justify-end flex-wrap gap-2">
        <!-- Sort Dropdown -->
        <v-menu>
          <template #activator="{ props }">
            <v-btn v-bind="props" class="rounded-pill" color="primary" variant="outlined">
              Sort
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="sortBy = 'name'">Name</v-list-item>
            <v-list-item @click="sortBy = 'status'">Status</v-list-item>
          </v-list>
        </v-menu>

        <!-- Order Dropdown -->
        <v-menu>
          <template #activator="{ props }">
            <v-btn v-bind="props" class="rounded-pill" color="primary" variant="outlined">
              Order
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="sortOrder = 'asc'">Ascending</v-list-item>
            <v-list-item @click="sortOrder = 'desc'">Descending</v-list-item>
          </v-list>
        </v-menu>

        <!-- Filter Dropdown -->
        <v-menu>
          <template #activator="{ props }">
            <v-btn v-bind="props" class="rounded-pill" color="primary" variant="outlined">
              Filter
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="filterStatus = 'On'">On</v-list-item>
            <v-list-item @click="filterStatus = 'Off'">Off</v-list-item>
          </v-list>
        </v-menu>

        <!-- Update Button -->
        <v-btn class="rounded-pill" color="success" variant="outlined" @click="fetchDevices(true)">
          Update
        </v-btn>

        <!-- Clear Button -->
        <v-btn class="rounded-pill" color="grey" variant="outlined" @click="clearAll">
          Clear
        </v-btn>
      </v-col>
    </v-row>

    <!-- Data Table -->
    <v-data-table
      :headers="headers"
      :items="filteredDevices"
      :loading="loading"
      item-value="id"
      class="elevation-1"
      @click:row="(_, row) => openDetails(row.item)"
    >
      <template #item.status="{ item }">
        <v-chip :color="item.status === 'On' ? 'green' : 'red'" dark>
          {{ item.status }}
        </v-chip>
      </template>
    </v-data-table>

    <!-- Device Details Dialog -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card v-if="selectedDevice">
        <v-card-title class="headline"
          >{{ selectedDevice.id }} — {{ selectedDevice.type }}</v-card-title
        >
        <v-card-text>
          <p><strong>Status:</strong> {{ selectedDevice.status }}</p>
          <p><strong>Temperature:</strong> {{ selectedDevice.temperature }} °C</p>
          <p><strong>Vibration:</strong> {{ selectedDevice.vibration }} mm/s</p>
          <p><strong>Sound:</strong> {{ selectedDevice.sound }} dB</p>
          <p><strong>Power:</strong> {{ selectedDevice.power }} kW</p>
          <p><strong>Operational Hours:</strong> {{ selectedDevice.operational_hours }}</p>
          <p>
            <strong>Last Maintenance:</strong> {{ selectedDevice.last_maintenance_days }} days ago
          </p>
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
import '@mdi/font/css/materialdesignicons.css'

const headers = [
  { title: 'ID', key: 'id', sortable: true },
  { title: 'Machine Type', key: 'type', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Temperature (°C)', key: 'temperature', sortable: true },
  { title: 'Vibration (mm/s)', key: 'vibration', sortable: true },
  { title: 'Sound (dB)', key: 'sound', sortable: true },
  { title: 'Power (kW)', key: 'power', sortable: true },
  { title: 'Operational Hours', key: 'operational_hours', sortable: true },
  { title: 'Last Maintenance (days)', key: 'last_maintenance_days', sortable: true },
]

const devices = ref([])
const loading = ref(false)
const search = ref('')
const dialog = ref(false)
const selectedDevice = ref(null)
const sortBy = ref(null)
const sortOrder = ref(null)
const filterStatus = ref('all')

const clearAll = () => {
  sortBy.value = null
  sortOrder.value = null
  search.value = ''
  filterStatus.value = 'all'
  fetchDevices(false) // Reload original data from Excel
}

const fetchDevices = async (simulate = false) => {
  const res = await axios.get(
    `http://localhost:8000/api/devices${simulate ? '?simulate=true' : ''}`,
  )
  devices.value = res.data
}

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
  let list = devices.value

  // Search
  if (search.value) {
    const keyword = search.value.toLowerCase()
    list = list.filter(
      (d) => d.type.toLowerCase().includes(keyword) || d.status.toLowerCase().includes(keyword),
    )
  }

  // Filter by status (On/Off)
  if (filterStatus.value !== 'all') {
    list = list.filter((d) => d.status === filterStatus.value)
  }

  // Sort only if both sortBy and sortOrder are selected
  if (sortBy.value && sortOrder.value) {
    const key = sortBy.value === 'name' ? 'type' : 'status'
    list = [...list].sort((a, b) => {
      const aVal = a[key]?.toString().toLowerCase() || ''
      const bVal = b[key]?.toString().toLowerCase() || ''
      return sortOrder.value === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal)
    })
  }

  return list
})

const openDetails = (device) => {
  selectedDevice.value = device
  dialog.value = true
}
</script>

<style>
.search-bar {
  height: 36px;
  font-size: 0.875rem;
  padding: 0 16px;
  --v-input-padding-top: 0px;
  --v-input-padding-bottom: 0px;
}

.search-bar .v-input__control {
  min-height: 36px;
  padding-top: 0;
  padding-bottom: 0;
  align-items: center;
}

.search-bar .v-field__input {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  height: 36px !important;
  line-height: 36px !important;
}
</style>
