<template>
  <div class="min-h-screen">
    <header class="bg-emerald-700 text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold">🌍 Calculateur d'Empreinte Carbone pour Déplacement Chantier</h1>
        <p class="text-emerald-200 text-sm">Planifiez vos mesures de terrain et calculez les émissions de transport</p>
      </div>
    </header>

    <!-- Tab Bar -->
    <div class="max-w-7xl mx-auto px-4 pt-6">
      <div class="flex flex-row gap-2 border-b">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-4 py-2 rounded-t-lg font-semibold transition-colors"
          :class="activeTab === tab.id
            ? 'bg-emerald-600 text-white'
            : 'bg-white text-gray-600 hover:bg-gray-100 hover:text-gray-800'">
          {{ tab.label }}
        </button>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-6">
      <!-- Tab: Véhicules -->
      <div v-if="activeTab === 'vehicules'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Vehicle List -->
        <div class="lg:col-span-1 space-y-6">
          <div class="bg-white rounded-xl shadow p-5">
            <h2 class="text-xl font-bold mb-4">🚗 Gestion des Véhicules</h2>
            <div v-for="(v, i) in vehicles" :key="v.id"
              class="vehicle-card bg-gray-50 p-4 rounded-lg mb-3 border cursor-pointer"
              :class="{ 'ring-2 ring-emerald-500 bg-emerald-50': selectedIdx === i }"
              @click="selectVehicle(i)">
              <div class="flex justify-between items-start">
                <h3 class="font-semibold">{{ v.name }}</h3>
                <button @click.stop="deleteVehicle(i)" class="text-red-500 hover:text-red-700">&times;</button>
              </div>
              <p class="text-xs text-gray-500">📍 {{ v.homeAddress }}</p>
              <p class="text-xs text-gray-500">🌫️ {{ v.emissionFactor }} kg CO₂/L · ⛽ {{ v.consumption }} L/100km</p>
              <p class="text-xs text-gray-500">📋 {{ v.destinations?.length || 0 }} sites</p>
            </div>
            <button @click="showAddVehicle = true" class="w-full bg-emerald-600 text-white py-2 rounded-lg hover:bg-emerald-700">+ Ajouter un Véhicule</button>
          </div>

          <!-- Vehicle Settings -->
          <div class="bg-white rounded-xl shadow p-5" v-if="currentVehicle">
            <h3 class="font-bold mb-3">⚙️ {{ currentVehicle.name }}</h3>
            <div class="space-y-3 text-sm">
              <div><label class="block text-gray-600">Nom</label><input v-model="currentVehicle.name" class="w-full p-2 border rounded" /></div>
              <div><label class="block text-gray-600">Adresse de Base</label><input v-model="currentVehicle.homeAddress" class="w-full p-2 border rounded" /></div>
              <div class="grid grid-cols-2 gap-2">
                <div><label class="block text-gray-600">Émission (kg CO₂/L)</label><input v-model.number="currentVehicle.emissionFactor" type="number" step="0.01" class="w-full p-2 border rounded" /></div>
                <div><label class="block text-gray-600">Consommation (L/100km)</label><input v-model.number="currentVehicle.consumption" type="number" step="0.1" class="w-full p-2 border rounded" /></div>
              </div>
              <div><label class="block text-gray-600">Nom de l'Étude</label><input v-model="currentVehicle.studySettings.studyName" class="w-full p-2 border rounded" /></div>
              <div class="grid grid-cols-2 gap-2">
                <div><label class="block text-gray-600">Durée (jours)</label><input v-model.number="currentVehicle.studySettings.studyDuration" type="number" min="1" class="w-full p-2 border rounded" /></div>
                <div><label class="block text-gray-600">Heures/Jour</label><select v-model.number="currentVehicle.studySettings.workingHours" class="w-full p-2 border rounded"><option>8</option><option>10</option><option>12</option></select></div>
              </div>
              <button @click="saveVehicle" class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">💾 Enregistrer</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab: Sites -->
      <div v-if="activeTab === 'sites'" class="space-y-6">
        <div class="bg-white rounded-xl shadow p-5">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold">📍 Sites de Terrain</h2>
            <div class="flex gap-2">
              <button @click="showAddDest = true" class="bg-emerald-600 text-white px-3 py-2 rounded-lg text-sm hover:bg-emerald-700">+ Site</button>
              <button @click="calcRoutes" class="bg-blue-600 text-white px-3 py-2 rounded-lg text-sm hover:bg-blue-700">🔄 Optimiser Routes</button>
            </div>
          </div>

          <div v-if="!currentVehicle?.destinations?.length" class="text-center py-8 text-gray-400">Aucun site ajouté. Cliquez sur "+ Site" pour commencer.</div>

          <div v-for="(d, i) in currentVehicle?.destinations" :key="d.id" class="destination-item border rounded-lg p-4 mb-3">
            <div class="flex justify-between items-start">
              <h3 class="font-semibold">{{ d.name || 'Site ' + (i+1) }}</h3>
              <div class="flex gap-2 text-sm">
                <button @click="editDest(i)" class="text-blue-600">Modifier</button>
                <button @click="deleteDest(i)" class="text-red-600">Supprimer</button>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm mt-2">
              <p>📍 {{ d.address }}</p>
              <p>📏 {{ d.measurements || '—' }}</p>
              <p>⏱ {{ d.duration }}h</p>
              <p>📅 Jours: {{ d.days?.join(', ') }}</p>
              <p>📐 Distance: {{ d.roundTripDistance?.toFixed(1) }} km</p>
              <p>🌫️ CO₂: {{ d.co2Emissions?.toFixed(2) }} kg</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab: Carte -->
      <div v-if="activeTab === 'carte'" class="space-y-6">
        <div class="bg-white rounded-xl shadow p-5">
          <h3 class="font-bold mb-3">🗺️ Carte</h3>
          <div id="map" class="map-container"></div>
        </div>
      </div>

      <!-- Tab: Résumé -->
      <div v-if="activeTab === 'resume'" class="space-y-6">
        <div class="bg-white rounded-xl shadow p-5">
          <h3 class="text-xl font-bold mb-4">📊 Résumé</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div class="bg-blue-50 p-4 rounded-lg"><p class="text-sm text-blue-800">Distance Totale</p><p class="text-2xl font-bold text-blue-600">{{ totalDistance.toFixed(1) }} km</p></div>
            <div class="bg-yellow-50 p-4 rounded-lg"><p class="text-sm text-yellow-800">Carburant</p><p class="text-2xl font-bold text-yellow-600">{{ totalFuel.toFixed(1) }} L</p></div>
            <div class="bg-red-50 p-4 rounded-lg"><p class="text-sm text-red-800">CO₂ Total</p><p class="text-2xl font-bold text-red-600">{{ totalCO2.toFixed(2) }} kg</p></div>
            <div class="bg-purple-50 p-4 rounded-lg"><p class="text-sm text-purple-800">Sites</p><p class="text-2xl font-bold text-purple-600">{{ currentVehicle?.destinations?.length || 0 }}</p></div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><h4 class="font-semibold mb-2">Par Véhicule</h4><div v-for="vt in allTotals" :key="vt.name" class="flex justify-between py-1 text-sm border-b"><span>{{ vt.name }}</span><span class="font-bold">{{ vt.co2.toFixed(2) }} kg CO₂</span></div></div>
            <div><h4 class="font-semibold mb-2">Répartition CO₂</h4><canvas id="chart"></canvas></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Vehicle Modal -->
    <div v-if="showAddVehicle" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showAddVehicle=false">
      <div class="bg-white p-6 rounded-xl shadow-xl max-w-md w-full">
        <h3 class="text-xl font-bold mb-4">Nouveau Véhicule</h3>
        <div class="space-y-3">
          <input v-model="newV.name" placeholder="Nom" class="w-full p-2 border rounded" />
          <input v-model="newV.homeAddress" placeholder="Adresse de base" class="w-full p-2 border rounded" />
          <div class="grid grid-cols-2 gap-2">
            <input v-model.number="newV.emissionFactor" type="number" step="0.01" placeholder="Émission" class="w-full p-2 border rounded" />
            <input v-model.number="newV.consumption" type="number" step="0.1" placeholder="Consommation" class="w-full p-2 border rounded" />
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-4">
          <button @click="showAddVehicle=false" class="px-4 py-2 border rounded">Annuler</button>
          <button @click="addVehicle" class="px-4 py-2 bg-emerald-600 text-white rounded-lg">Ajouter</button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Destination Modal -->
    <div v-if="showDestModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showDestModal=false">
      <div class="bg-white p-6 rounded-xl shadow-xl max-w-lg w-full">
        <h3 class="text-xl font-bold mb-4">{{ editingDest !== null ? 'Modifier' : 'Nouveau' }} Site</h3>
        <div class="space-y-3">
          <input v-model="destForm.name" placeholder="Nom du site" class="w-full p-2 border rounded" />
          <input v-model="destForm.address" placeholder="Adresse" class="w-full p-2 border rounded" />
          <textarea v-model="destForm.measurements" placeholder="Mesures" class="w-full p-2 border rounded" rows="2"></textarea>
          <div class="grid grid-cols-2 gap-2">
            <input v-model.number="destForm.duration" type="number" step="0.5" placeholder="Durée (h)" class="w-full p-2 border rounded" />
            <div><label class="text-sm text-gray-600">Jours</label><div class="flex flex-wrap gap-1 mt-1"> <label v-for="day in maxDays" :key="day" class="flex items-center text-xs gap-1"><input type="checkbox" :value="day" v-model="destForm.days" />J{{ day }}</label></div></div>
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-4">
          <button @click="showDestModal=false" class="px-4 py-2 border rounded">Annuler</button>
          <button @click="saveDest" class="px-4 py-2 bg-emerald-600 text-white rounded-lg">Enregistrer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import axios from 'axios'
import L from 'leaflet'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

const vehicles = ref([])
const selectedIdx = ref(0)
const showAddVehicle = ref(false)
const showDestModal = ref(false)
const editingDest = ref(null)
const showAddDest = ref(false)

const tabs = [
  { id: 'vehicules', label: '🚗 Véhicules' },
  { id: 'sites', label: '📍 Sites' },
  { id: 'carte', label: '🗺️ Carte' },
  { id: 'resume', label: '📊 Résumé' },
]
const activeTab = ref('vehicules')

const newV = ref({ name: '', homeAddress: '', emissionFactor: 2.31, consumption: 8.5 })
const destForm = ref({ name: '', address: '', measurements: '', duration: 4, days: [1] })

let map = null
let markers = []
let routeLayers = []
let chart = null

const DAY_COLORS = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316']

const currentVehicle = computed(() => vehicles.value[selectedIdx.value])

const maxDays = computed(() => currentVehicle.value?.studySettings?.studyDuration || 5)

const totalDistance = computed(() => currentVehicle.value?.destinations?.reduce((s, d) => s + (d.roundTripDistance || 0), 0) || 0)
const totalFuel = computed(() => currentVehicle.value?.destinations?.reduce((s, d) => s + (d.fuelUsed || 0), 0) || 0)
const totalCO2 = computed(() => currentVehicle.value?.destinations?.reduce((s, d) => s + (d.co2Emissions || 0), 0) || 0)

const allTotals = computed(() => vehicles.value.map(v => ({
  name: v.name,
  co2: v.destinations?.reduce((s, d) => s + (d.co2Emissions || 0), 0) || 0,
})))

async function loadData() {
  try {
    const res = await axios.get('/api/vehicles/')
    vehicles.value = res.data
    if (vehicles.value.length === 0) {
      // Create default vehicle
      const r = await axios.post('/api/vehicles/', { name: 'Field Survey Van', homeAddress: '123 Engineering Road, City Center' })
      vehicles.value = [r.data]
    }
  } catch (e) {
    console.error('Failed to load', e)
  }
}

function selectVehicle(i) { selectedIdx.value = i; nextTick(updateMap) }

async function addVehicle() {
  const r = await axios.post('/api/vehicles/', newV.value)
  vehicles.value.push(r.data)
  showAddVehicle.value = false
  newV.value = { name: '', homeAddress: '', emissionFactor: 2.31, consumption: 8.5 }
}

async function deleteVehicle(i) {
  const v = vehicles.value[i]
  await axios.delete(`/api/vehicles/${v.id}/`)
  vehicles.value.splice(i, 1)
  if (selectedIdx.value >= vehicles.value.length) selectedIdx.value = vehicles.value.length - 1
}

async function saveVehicle() {
  const v = currentVehicle.value
  await axios.put(`/api/vehicles/${v.id}/`, v)
}

function editDest(i) {
  const d = currentVehicle.value.destinations[i]
  destForm.value = { ...d, days: [...d.days] }
  editingDest.value = i
  showDestModal.value = true
}

async function deleteDest(i) {
  const d = currentVehicle.value.destinations[i]
  await axios.delete(`/api/destinations/${d.id}/`)
  currentVehicle.value.destinations.splice(i, 1)
  updateMap()
}

async function saveDest() {
  const v = currentVehicle.value
  if (editingDest.value !== null) {
    const d = v.destinations[editingDest.value]
    await axios.put(`/api/destinations/${d.id}/`, destForm.value)
    Object.assign(d, destForm.value)
  } else {
    const r = await axios.post(`/api/vehicles/${v.id}/destinations/`, destForm.value)
    v.destinations.push(r.data)
  }
  showDestModal.value = false
  editingDest.value = null
  destForm.value = { name: '', address: '', measurements: '', duration: 4, days: [1] }
  updateMap()
}

async function calcRoutes() {
  const v = currentVehicle.value
  if (!v) return
  const r = await axios.get(`/api/route/${v.id}/`)
  // Store per-day route geometry on the vehicle for map drawing
  v.dayRouteGeometries = {}
  // Update each destination with route data
  for (const d of v.destinations) {
    const day = d.days?.[0]
    if (day && r.data[day]) {
      const route = r.data[day]
      if (route.type === 'round_trip') {
        d.distance = route.distance / 1000
        d.roundTripDistance = route.distance / 1000
      } else {
        d.distance = route.distance / 1000 / (d.days?.length || 1)
        d.roundTripDistance = route.distance / 1000
      }
      d.fuelUsed = d.roundTripDistance * (v.consumption / 100)
      d.co2Emissions = d.fuelUsed * v.emissionFactor
      // Attach geometry so the map can draw this destination's route segment
      if (route.geometry?.coordinates) {
        d.routeGeometry = route.geometry.coordinates
        v.dayRouteGeometries[day] = route.geometry.coordinates
      }
      await axios.put(`/api/destinations/${d.id}/`, {
        distance: d.distance, roundTripDistance: d.roundTripDistance,
        fuelUsed: d.fuelUsed, co2Emissions: d.co2Emissions,
      })
    }
  }
  updateMap()
  updateChart()
}

function updateMap() {
  if (!map) return
  markers.forEach(m => map.removeLayer(m))
  markers = []
  // Clear previous route polylines
  routeLayers.forEach(l => map.removeLayer(l))
  routeLayers = []

  const v = currentVehicle.value
  if (!v) return

  const bounds = []

  // Determine home position: prefer first coordinate of any route geometry,
  // fall back to hardcoded [46.5, 2.5].
  let home = [46.5, 2.5]
  const geometries = v.dayRouteGeometries
  if (geometries) {
    const anyDay = Object.keys(geometries).find(k => geometries[k]?.length)
    if (anyDay) {
      const [lng, lat] = geometries[anyDay][0]
      home = [lat, lng]
    }
  } else {
    // Fall back to per-destination route geometry if available
    const firstWithGeo = (v.destinations || []).find(d => d.routeGeometry?.length)
    if (firstWithGeo) {
      const [lng, lat] = firstWithGeo.routeGeometry[0]
      home = [lat, lng]
    }
  }

  // Home marker
  if (v.homeAddress) {
    const m = L.marker(home, { icon: L.divIcon({ html: '🏠', className: '', iconSize: [24, 24] }) }).addTo(map).bindPopup(`<b>${v.name}</b><br>${v.homeAddress}`)
    markers.push(m)
    bounds.push(home)
  }

  // Destination markers
  for (const d of v.destinations || []) {
    if (d.lat && d.lng) {
      const color = d.co2Emissions > 50 ? 'red' : d.co2Emissions > 20 ? 'orange' : 'green'
      const m = L.circleMarker([d.lat, d.lng], {
        radius: 8, fillColor: color, color: '#fff', weight: 2, fillOpacity: 0.8
      }).addTo(map).bindPopup(`<b>${d.name}</b><br>${d.address}<br>CO₂: ${d.co2Emissions?.toFixed(2)} kg`)
      markers.push(m)
      bounds.push([d.lat, d.lng])
    }
  }

  // Draw route polylines per day using stored geometry (GeoJSON [lng, lat] pairs)
  if (geometries) {
    const days = Object.keys(geometries).sort((a, b) => Number(a) - Number(b))
    days.forEach((day, idx) => {
      const coords = geometries[day]
      if (!coords || coords.length < 2) return
      const latlngs = coords.map(([lng, lat]) => [lat, lng])
      const color = DAY_COLORS[idx % DAY_COLORS.length]
      const polyline = L.polyline(latlngs, {
        color,
        weight: 4,
        opacity: 0.8,
      }).addTo(map).bindPopup(`Journée ${day}`)
      routeLayers.push(polyline)
      latlngs.forEach(ll => bounds.push(ll))
    })
  }

  if (bounds.length > 1) map.fitBounds(bounds, { padding: [50, 50] })
}

function updateChart() {
  if (chart) { chart.destroy(); chart = null }
  const canvas = document.getElementById('chart')
  if (!canvas || !allTotals.value.length) return
  const ctx = canvas.getContext('2d')
  chart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: allTotals.value.map(v => v.name),
      datasets: [{ data: allTotals.value.map(v => v.co2), backgroundColor: ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B', '#EF4444'] }]
    },
    options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
  })
}

onMounted(async () => {
  await loadData()
  await nextTick()
  initMap()
  updateChart()
})

watch(activeTab, (tab) => {
  if (tab === 'carte') {
    nextTick(() => {
      initMap()
      updateMap()
    })
  } else if (tab === 'resume') {
    nextTick(updateChart)
  }
})

function initMap() {
  const el = document.getElementById('map')
  if (!el) return
  if (!map) {
    map = L.map('map').setView([46.5, 2.5], 6)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)
  } else {
    // Ensure correct sizing after re-entering the tab
    map.invalidateSize()
  }
  updateMap()
}

watch(currentVehicle, () => { nextTick(() => { updateMap(); updateChart() }) }, { deep: true })
</script>
