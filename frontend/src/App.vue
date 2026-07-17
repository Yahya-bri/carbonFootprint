<template>
  <div class="min-h-screen">
    <header class="bg-emerald-700 text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <router-link to="/" class="text-xl font-bold flex items-center gap-2">
          🌍 Calculateur d'Empreinte Carbone
        </router-link>
        <span class="text-emerald-200 text-sm">Déplacement Chantier</span>
      </div>
    </header>
    <main class="max-w-7xl mx-auto px-4 py-6">
      <router-view />
    </main>
  </div>
</template>
