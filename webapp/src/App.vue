<script setup lang="ts">
import Info from './components/Info/Info.vue';
import Achievements from './components/Achievements/Achievements.vue';
import ProgressSpinner from 'primevue/progressspinner';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import { useFetch } from './hooks/api.ts';
// import { useTelegram } from './hooks/telegram.ts';
import Statistic from './components/Statistic/Statistic.vue';
import { IUser, IUserContent } from './types/types.ts';
import { Ref, ref, watchEffect } from 'vue';
import axios from 'axios';

// const { webApp, user } = useTelegram();

const user = { username: 'Igor' };
const contentData: Ref<IUserContent | null> = ref(null);
const active = ref(0);
let startX: number | null = null;

const { data: userData } = useFetch<IUser>(
  `https://ambassadors.sytes.net/api/v1/ambassador_by_tg_username/${user.username}/`
);

watchEffect(async () => {
  if (userData.value) {
    try {
      const response = await axios.get(
        `https://ambassadors.sytes.net/api/v1/ambassadors/${userData.value.id}/content/`
      );
      contentData.value = response.data;
    } catch (error) {
      console.error('Error fetching content data:', error);
    }
  }
});

const switchTabOnSwipe = (e: TouchEvent) => {
  if (!startX) return;
  const currentX = e.touches[0].clientX;
  const deltaX = startX - currentX;
  const sensitivity = 20; // Порог чувствительности для определения свайпа
  if (Math.abs(deltaX) > sensitivity) {
    if (deltaX > 0) {
      active.value < 2 && active.value++;
    } else {
      active.value > 0 && active.value--;
    }
  }
  startX = null;
};
</script>

<template>
  <div
    class="fullwidth"
    v-if="userData"
    @touchstart="startX = $event.touches[0].clientX"
    @touchmove.prevent="switchTabOnSwipe"
    @touchend="startX = null"
  >
    <TabView
      v-model:activeIndex="active"
      :pt="{ nav: { style: 'justify-content: space-between; width: 100%' } }"
    >
      <TabPanel header="Personal info">
        <Info :user="userData" />
      </TabPanel>
      <TabPanel header="Achievements">
        <Achievements :user="userData" />
      </TabPanel>
      <TabPanel header="Statistic">
        <Statistic v-if="contentData" :data="contentData" />
      </TabPanel>
    </TabView>
  </div>
  <ProgressSpinner v-else />
</template>

<style scoped>
.fullwidth {
  height: 100vh;
}

@media (min-width: 800px) {
  .fullwidth {
    width: 70vw;
  }
}

@media (max-width: 799.98px) {
  .fullwidth {
    width: 100vw;
  }
}
</style>
