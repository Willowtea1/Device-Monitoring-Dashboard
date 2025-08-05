<!-- src/views/TestPage -->
<template>
  <div class="dashboard-wrapper">
    <v-container>
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
            v-model="selectedID"
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

      <!-- Second Section: Average Cards -->

      <v-row v-if="selectedType" class="mt-0">
        <v-col cols="12" sm="6" md="3" v-for="(card, index) in avgCards" :key="index">
          <v-card elevation="2" class="pa-4 text-center">
            <h3 class="text-subtitle-1 font-weight-bold mb-2">{{ card.label }}</h3>
            <div class="text-h5">{{ card.value }}</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Third Section: Featured Device -->

      <v-card class="pa-6 flex-grow-1 d-flex align-center mt-4">
        <v-row class="align-center flex-grow-1">
          <!-- Previous Button -->
          <v-col cols="1">
            <v-btn icon @click="prevDevice">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
          </v-col>

          <!-- Device Info -->
          <v-col cols="10">
            <v-row>
              <!-- Image -->
              <v-col cols="12" md="5">
                <v-img
                  :src="summary.featured_device?.image_url || 'https://via.placeholder.com/250'"
                  width="250"
                  height="250"
                  class="rounded"
                />
              </v-col>

              <!-- Stats -->
              <v-col cols="12" md="7">
                <v-row dense>
                  <v-col cols="12" sm="10">
                    <v-text-field
                      label="Machine ID"
                      :model-value="selectedID || '-'"
                      readonly
                      variant="outlined"
                      dense
                    />
                  </v-col>

                  <v-col cols="12" sm="2">
                    <div class="d-flex flex-column align-center">
                      <label class="text-caption font-weight-bold mb-1 text-center">Status</label>
                      <v-chip
                        :color="summary.featured_device?.status === 'On' ? 'green' : 'red'"
                        class="text-white font-weight-bold justify-center"
                        variant="flat"
                        style="width: 100px"
                      >
                        {{ summary.featured_device?.status || '-' }}
                      </v-chip>
                    </div>
                  </v-col>
                </v-row>

                <v-row dense>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      label="Temperature"
                      :model-value="(summary.featured_device?.temperature ?? '-') + ' °C'"
                      readonly
                      variant="outlined"
                      dense
                    />
                  </v-col>

                  <v-col cols="12" sm="6">
                    <v-text-field
                      label="Sound"
                      :model-value="(summary.featured_device?.sound ?? '-') + ' dB'"
                      readonly
                      variant="outlined"
                      dense
                    />
                  </v-col>

                  <v-col cols="12" sm="6">
                    <v-text-field
                      label="Vibration"
                      :model-value="(summary.featured_device?.vibration ?? '-') + ' mm/s'"
                      readonly
                      variant="outlined"
                      dense
                    />
                  </v-col>

                  <v-col cols="12" sm="6">
                    <v-text-field
                      label="Power"
                      :model-value="(summary.featured_device?.power ?? '-') + ' kW'"
                      readonly
                      variant="outlined"
                      dense
                    />
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-col>

          <!-- Next Button -->
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
import { ref, computed, watch, onMounted } from 'vue'
import axios from 'axios'

// Reactive State
const devices = ref([])
const summary = ref({})
const selectedType = ref('Mixer')
const selectedID = ref('MC_000000')
const selectedStatus = ref(null)
const featuredIndex = ref(0)

// Fetch devices and set initial selections
const fetchDevices = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/devices')
    devices.value = res.data

    const validTypes = [...new Set(devices.value.map((d) => d.type))]
    if (!validTypes.includes(selectedType.value)) selectedType.value = null

    const validIDs = devices.value.map((d) => d.id)
    if (!validIDs.includes(selectedID.value)) selectedID.value = null

    const device = devices.value.find((d) => d.id === selectedID.value)
    if (device) selectedStatus.value = device.status

    if (devices.value.length) {
      summary.value.featured_device = devices.value[0]
      featuredIndex.value = 0
    }
  } catch (err) {
    console.error('Failed to fetch devices:', err)
  }
}

// Fetch summary data only
const fetchSummary = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/summary')
    summary.value = res.data

    const idx = devices.value.findIndex((d) => d.id === summary.value.featured_device?.id)
    featuredIndex.value = idx !== -1 ? idx : 0
  } catch (err) {
    console.error('Failed to fetch summary:', err)
  }
}

onMounted(async () => {
  await fetchDevices()
  await fetchSummary()

  // Ensure selectedID matches the selectedType
  if (selectedType.value && filteredIDs.value.length > 0) {
    if (!filteredIDs.value.includes(selectedID.value)) {
      selectedID.value = filteredIDs.value[0]
    }
  } else {
    selectedID.value = null
  }
})

// Dropdown Data
const machineTypes = computed(() => {
  return [...new Set(devices.value.map((d) => d.type))]
})

const filteredIDs = computed(() => {
  return selectedType.value
    ? devices.value.filter((d) => d.type === selectedType.value).map((d) => d.id)
    : []
})

const filteredDevices = computed(() => {
  return selectedType.value ? devices.value.filter((d) => d.type === selectedType.value) : []
})

// Watcher to update status
watch(selectedID, (id) => {
  const device = devices.value.find((d) => d.id === id)
  selectedStatus.value = device ? device.status : null

  if (device) {
    summary.value.featured_device = device
    const idx = filteredDevices.value.findIndex((d) => d.id === id)
    if (idx !== -1) featuredIndex.value = idx
  }
})

watch(
  () => selectedType.value,
  (newType) => {
    if (newType && filteredIDs.value.length > 0) {
      selectedID.value = filteredIDs.value[0]
    } else {
      selectedID.value = null
    }
  },
  { immediate: true },
)

// Average Metrics
const avg = (field) => {
  const filtered = devices.value.filter((d) => d.type === selectedType.value)
  const sum = filtered.reduce((acc, d) => acc + (d[field] ?? 0), 0)
  return filtered.length ? (sum / filtered.length).toFixed(1) : null
}

const avgCards = computed(() => [
  { label: 'Avg. Temperature', value: avg('temperature') ? avg('temperature') + ' °C' : '-' },
  { label: 'Avg. Vibration', value: avg('vibration') ? avg('vibration') + ' mm/s' : '-' },
  { label: 'Avg. Sound', value: avg('sound') ? avg('sound') + ' dB' : '-' },
  { label: 'Avg. Power', value: avg('power') ? avg('power') + ' kW' : '-' },
])

// Featured Device (Bottom Section)
const nextDevice = () => {
  if (!filteredDevices.value.length) return

  featuredIndex.value = (featuredIndex.value + 1) % filteredDevices.value.length
  const newDevice = filteredDevices.value[featuredIndex.value]

  summary.value.featured_device = newDevice
  selectedID.value = newDevice.id
}

const prevDevice = () => {
  if (!filteredDevices.value.length) return

  featuredIndex.value =
    (featuredIndex.value - 1 + filteredDevices.value.length) % filteredDevices.value.length
  const newDevice = filteredDevices.value[featuredIndex.value]

  summary.value.featured_device = newDevice
  selectedID.value = newDevice.id
}
</script>
