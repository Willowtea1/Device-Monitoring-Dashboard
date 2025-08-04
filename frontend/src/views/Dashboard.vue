<!-- Dashboard.vue -->
<template>
  <div class="dashboard-wrapper">
    <v-container>
      <h1 class="text-h5 mb-4">Dashboard</h1>

      <v-row>
        <v-col cols="12" sm="4">
          <v-card>
            <v-card-title>Status</v-card-title>
            <v-card-text>{{ summary.online }} online / {{ summary.offline }} offline</v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card>
            <v-card-title>Avg CPU</v-card-title>
            <v-card-text>{{ summary.avg_cpu }}%</v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card>
            <v-card-title>Avg Temp</v-card-title>
            <v-card-text>{{ summary.avg_temp }}°C</v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-container class="flex-grow-1 d-flex flex-column">
      <v-card class="pa-4 flex-grow-1 d-flex align-center">
        <v-row class="align-center flex-grow-1">
          <v-col cols="1">
            <v-btn icon @click="prevDevice">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
          </v-col>

          <v-col cols="10">
            <v-row>
              <v-col cols="5">
                <v-img
                  :src="summary.featured_device?.image_url"
                  width="250"
                  height="250"
                  class="rounded"
                />
              </v-col>
              <v-col cols="7">
                <h3>{{ summary.featured_device?.name }}</h3>
                <div>Status: {{ summary.featured_device?.status }}</div>
                <div>CPU: {{ summary.featured_device?.cpu }}%</div>
                <div>Temperature: {{ summary.featured_device?.temperature }}°C</div>
              </v-col>
            </v-row>
          </v-col>

          <v-col cols="1">
            <v-btn icon @click="nextDevice">
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { onMounted } from 'vue'
import axios from 'axios'

const summary = ref({})
const devices = ref([])
const featuredIndex = ref(0)

const fetchData = async () => {
  const resSummary = await axios.get('http://localhost:8000/api/summary')
  const resDevices = await axios.get('http://localhost:8000/api/devices')
  summary.value = resSummary.data
  devices.value = resDevices.data
  featuredIndex.value = devices.value.findIndex((d) => d.id === summary.value.featured_device.id)
}

const nextDevice = () => {
  featuredIndex.value = (featuredIndex.value + 1) % devices.value.length
}

const prevDevice = () => {
  featuredIndex.value = (featuredIndex.value - 1 + devices.value.length) % devices.value.length
}

// Watch for index change and update featured device
watch(featuredIndex, (newIndex) => {
  summary.value.featured_device = devices.value[newIndex]
})

onMounted(fetchData)
</script>

<style scoped>
.dashboard-wrapper {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
