<template>
  <v-container>
    <h1 class="text-h4 mb-4 d-flex align-center gap-2">
      <v-icon icon="mdi-chart-areaspline" size="36" class="me-2" />Analytics
    </h1>

    <!-- Filter dropdowns (pill-shaped) -->
    <v-row class="justify-space-between align-center">
      <v-col cols="12" sm="6">
        <v-select
          v-model="selectedType"
          :items="machineTypes"
          label="Machine Type"
          variant="outlined"
          rounded="pill"
          dense
          clearable
        />
      </v-col>

      <v-col cols="12" sm="6">
        <v-select
          v-model="selectedDevice"
          :items="filteredIDs"
          label="Machine ID"
          variant="outlined"
          rounded="pill"
          dense
          clearable
          :disabled="!selectedType"
        />
      </v-col>
    </v-row>

    <!-- Loading spinner -->
    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary" size="48" />
      </v-col>
    </v-row>

    <!-- Charts -->
    <v-row v-if="!loading && chartData">
      <v-col cols="12" md="6">
        <LineChart :chart-data="chartData.temperature" :chart-options="chartOptions.temperature" />
      </v-col>
      <v-col cols="12" md="6">
        <LineChart :chart-data="chartData.vibration" :chart-options="chartOptions.vibration" />
      </v-col>
      <v-col cols="12" md="6">
        <LineChart :chart-data="chartData.sound" :chart-options="chartOptions.sound" />
      </v-col>
      <v-col cols="12" md="6">
        <LineChart :chart-data="chartData.power" :chart-options="chartOptions.power" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue'
import axios from 'axios'
import LineChart from '@/components/LineChart.vue'

// State
const devices = ref([])
const selectedDevice = ref(null)
const selectedType = ref(null)
const chartData = ref(null)
const loading = ref(false) // <- loading indicator

const DEFAULT_TYPE = 'Mixer'
const DEFAULT_DEVICE_ID = 'MC_000000'

// Fetch devices on mount
onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/devices')
    devices.value = res.data

    const typeExists = devices.value.some((d) => d.type === DEFAULT_TYPE)
    const idExists = devices.value.some((d) => d.id === DEFAULT_DEVICE_ID)

    if (typeExists) selectedType.value = DEFAULT_TYPE
    await nextTick()

    if (idExists && filteredIDs.value.includes(DEFAULT_DEVICE_ID)) {
      selectedDevice.value = DEFAULT_DEVICE_ID
    } else if (filteredIDs.value.length > 0) {
      selectedDevice.value = filteredIDs.value[0]
    }
  } catch (err) {
    console.error('Error fetching devices:', err)
  }
})

// Computed dropdown items
const machineTypes = computed(() => {
  return [...new Set(devices.value.map((d) => d.type))]
})

const filteredIDs = computed(() => {
  return selectedType.value
    ? devices.value.filter((d) => d.type === selectedType.value).map((d) => d.id)
    : []
})

// Auto-select device on type change
watch(selectedType, (newType) => {
  if (newType && filteredIDs.value.length > 0) {
    if (!filteredIDs.value.includes(selectedDevice.value)) {
      selectedDevice.value = filteredIDs.value[0]
    }
  } else {
    selectedDevice.value = null
  }
})

// Chart options
const chartOptions = {
  temperature: {
    responsive: true,
    plugins: { legend: { position: 'top' }, title: { display: true, text: 'Temperature' } },
  },
  vibration: {
    responsive: true,
    plugins: { legend: { position: 'top' }, title: { display: true, text: 'Vibration' } },
  },
  sound: {
    responsive: true,
    plugins: { legend: { position: 'top' }, title: { display: true, text: 'Sound' } },
  },
  power: {
    responsive: true,
    plugins: { legend: { position: 'top' }, title: { display: true, text: 'Power' } },
  },
}

// Fetch chart data when device changes
watch(selectedDevice, async (deviceId) => {
  if (!deviceId) return

  loading.value = true
  try {
    const res = await axios.get(`http://localhost:8000/api/devices/${deviceId}/chart`)
    const data = res.data

    if (!data.length) {
      chartData.value = null
      return
    }

    const labels = data.map((d) =>
      new Date(d.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    )

    const chartDate = new Date(data[0].timestamp).toLocaleDateString()
    chartOptions.temperature.plugins.title.text = `Temperature on ${chartDate}`
    chartOptions.vibration.plugins.title.text = `Vibration on ${chartDate}`
    chartOptions.sound.plugins.title.text = `Sound on ${chartDate}`
    chartOptions.power.plugins.title.text = `Power on ${chartDate}`

    chartData.value = {
      temperature: {
        labels,
        datasets: [
          {
            label: 'Temperature (°C)',
            data: data.map((d) => d.temperature),
            borderColor: 'rgb(75, 192, 192)',
            fill: false,
            tension: 0.1,
          },
        ],
      },
      vibration: {
        labels,
        datasets: [
          {
            label: 'Vibration (Hz)',
            data: data.map((d) => d.vibration),
            borderColor: 'rgb(255, 99, 132)',
            fill: false,
            tension: 0.1,
          },
        ],
      },
      sound: {
        labels,
        datasets: [
          {
            label: 'Sound (dB)',
            data: data.map((d) => d.sound),
            borderColor: 'rgb(54, 162, 235)',
            fill: false,
            tension: 0.1,
          },
        ],
      },
      power: {
        labels,
        datasets: [
          {
            label: 'Power (W)',
            data: data.map((d) => d.power),
            borderColor: 'rgb(255, 205, 86)',
            fill: false,
            tension: 0.1,
          },
        ],
      },
    }
  } catch (err) {
    console.error('Error fetching chart data:', err)
  } finally {
    loading.value = false
  }
})
</script>
