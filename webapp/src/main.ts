import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/md-dark-indigo/theme.css';
import './style.css';
import App from './App.vue';

createApp(App).use(PrimeVue).mount('#app');
