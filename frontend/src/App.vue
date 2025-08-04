<!-- src/App.vue -->
<template>
  <v-app>
    <v-navigation-drawer app permanent>
      <v-list>
        <v-list-item to="/" title="Dashboard" />
        <v-list-item to="/devices" title="Device Management" />
        <v-list-item to="/analytics" title="Analytics" />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
