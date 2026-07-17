<template>
  <div v-if="vehicle">
    <button @click="$router.push('/')" class="text-emerald-600 hover:text-emerald-800 mb-4 inline-block">
      ← Retour au tableau de bord
    </button>

    <div class="bg-white rounded-xl shadow p-6 mb-6">
      <h2 class="text-2xl font-bold mb-2">{{ vehicle.name }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
        <div><span class="text-gray-500">Adresse:</span> {{ vehicle.homeAddress }}</div>
        <div><span class="text-gray-500">Consommation:</span> {{ vehicle.consumption }} L/100km</div>
        <div><span class="text-gray-500">Facteur émission:</span> {{ vehicle.emissionFactor }} kg CO₂/L</div>
        <div><span class="text-gray-500">Étude:</span> {{ vehicle.studySettings?.studyName || '—' }}</div>
      </div>
    </div>

    <h3 class="text-xl font-semibold mb-3">Destinations ({{ vehicle.destinations.length }})</h3>
    <div class="overflow-x-auto">
      <table class="w-full bg-white rounded-xl shadow">
        <thead class="bg-gray-100 text-left text-sm uppercase text-gray-600">
          <tr>
            <th class="p-3">Nom</th>
            <th class="p-3">Adresse</th>
            <th class="p-3">Distance AR</th>
            <th class="p-3">Carburant</th>
            <th class="p-3">CO₂</th>
            <th class="p-3">Jours</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="dest in vehicle.destinations" :key="dest.id" class="hover:bg-gray-50">
            <td class="p-3 font-medium">{{ dest.name }}</td>
            <td class="p-3 text-sm text-gray-600">{{ dest.address }}</td>
            <td class="p-3">{{ dest.roundTripDistance }} km</td>
            <td class="p-3">{{ dest.fuelUsed }} L</td>
            <td class="p-3 font-semibold text-orange-600">{{ dest.co2Emissions }} kg</td>
            <td class="p-3">{{ dest.days?.join(', ') || '—' }}</td>
          </tr>
        </tbody>
        <tfoot class="bg-gray-50 font-semibold">
          <tr>
            <td colspan="2" class="p-3 text-right">Total</td>
            <td class="p-3">{{ totalDistance }} km</td>
            <td class="p-3">{{ totalFuel }} L</td>
            <td class="p-3 text-orange-600">{{ totalCo2 }} kg</td>
            <td class="p-3"></td>
          </tr>
        </tfoot>
      </table>
    </div>
  </div>
  <div v-else-if="loading" class="text-center py-12 text-gray-400">Chargement...</div>
  <div v-else class="text-center py-12 text-red-500">Véhicule introuvable.</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({ id: [String, Number] })
const vehicle = ref(null)
const loading = ref(true)

const totalCo2 = computed(() => vehicle.value?.destinations.reduce((s, d) => s + d.co2Emissions, 0).toFixed(2) || '0')
const totalFuel = computed(() => vehicle.value?.destinations.reduce((s, d) => s + d.fuelUsed, 0).toFixed(2) || '0')
const totalDistance = computed(() => vehicle.value?.destinations.reduce((s, d) => s + d.roundTripDistance, 0).toFixed(2) || '0')

onMounted(async () => {
  try {
    const res = await axios.get(`/api/vehicles/${props.id}/`)
    vehicle.value = res.data
  } catch (err) {
    console.error('Failed to load vehicle', err)
  } finally {
    loading.value = false
  }
})
</script>
