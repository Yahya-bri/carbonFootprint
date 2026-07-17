<template>
  <div>
    <!-- Summary Cards -->
    <div v-if="summary" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-xl shadow p-5 border-l-4 border-emerald-500">
        <p class="text-sm text-gray-500 uppercase tracking-wide">Véhicules</p>
        <p class="text-3xl font-bold text-emerald-700">{{ summary.totalVehicles }}</p>
      </div>
      <div class="bg-white rounded-xl shadow p-5 border-l-4 border-blue-500">
        <p class="text-sm text-gray-500 uppercase tracking-wide">Destinations</p>
        <p class="text-3xl font-bold text-blue-700">{{ summary.totalDestinations }}</p>
      </div>
      <div class="bg-white rounded-xl shadow p-5 border-l-4 border-orange-500">
        <p class="text-sm text-gray-500 uppercase tracking-wide">CO₂ Total</p>
        <p class="text-3xl font-bold text-orange-700">{{ summary.totalCo2Kg }} <span class="text-sm font-normal">kg</span></p>
      </div>
      <div class="bg-white rounded-xl shadow p-5 border-l-4 border-purple-500">
        <p class="text-sm text-gray-500 uppercase tracking-wide">Distance Totale</p>
        <p class="text-3xl font-bold text-purple-700">{{ summary.totalDistanceKm }} <span class="text-sm font-normal">km</span></p>
      </div>
    </div>

    <!-- Vehicle List -->
    <h2 class="text-2xl font-semibold mb-4">Équipes & Véhicules</h2>
    <div v-if="loading" class="text-center py-12 text-gray-400">Chargement...</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="(vehicle, index) in vehicles"
        :key="vehicle.id"
        class="bg-white rounded-xl shadow hover:shadow-lg transition-shadow p-6 cursor-pointer"
        @click="$router.push(`/vehicle/${vehicle.id}`)"
      >
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-lg font-semibold text-gray-800">{{ vehicle.name }}</h3>
          <span class="text-xs bg-emerald-100 text-emerald-700 px-2 py-1 rounded-full">
            {{ vehicle.destinations.length }} destinations
          </span>
        </div>
        <p class="text-sm text-gray-500 mb-1">📍 {{ vehicle.homeAddress }}</p>
        <p class="text-sm text-gray-500 mb-1">⛽ Consommation: {{ vehicle.consumption }} L/100km</p>
        <p class="text-sm text-gray-500">🌫️ Facteur émission: {{ vehicle.emissionFactor }} kg CO₂/L</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const vehicles = ref([])
const summary = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const [vehRes, sumRes] = await Promise.all([
      axios.get('/api/vehicles/'),
      axios.get('/api/summary/'),
    ])
    vehicles.value = vehRes.data
    summary.value = sumRes.data
  } catch (err) {
    console.error('Failed to load data', err)
  } finally {
    loading.value = false
  }
})
</script>
