<!-- src/App.vue -->
<template>
  <v-app>
    <v-navigation-drawer app permanent width="225">
      <v-list nav class="mt-6">
        <v-list-item to="/" link prepend-icon="mdi-view-dashboard" class="nav-item">
          <v-list-item-title class="text-subtitle-1 font-weight-bold">
            Dashboard
          </v-list-item-title>
        </v-list-item>

        <v-list-item to="/devices" link prepend-icon="mdi-cellphone-link" class="nav-item">
          <v-list-item-title class="text-subtitle-1 font-weight-bold">
            Device Management
          </v-list-item-title>
        </v-list-item>

        <v-list-item to="/analytics" link prepend-icon="mdi-chart-areaspline" class="nav-item">
          <v-list-item-title class="text-subtitle-1 font-weight-bold">
            Analytics
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<style>
.v-list-item__spacer {
  display: none !important;
}

.v-list-item__prepend .v-icon {
  margin-right: 8px;
}
</style>
