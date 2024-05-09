<script setup lang="ts">
import Avatar from 'primevue/avatar';
import Divider from 'primevue/divider';
import telegram from '../../assets/telegramIcon.svg';
import mail from '../../assets/mail.svg';
import phone from '../../assets/phone.svg';
import { IUser } from '../../types/types';

const props = defineProps<{ user: IUser }>();
const address = ['Страна:', 'Город:', 'Адрес:', 'Почтовый индекс:'];
const sizes = ['Размер одежды:', 'Размер ноги:'];
</script>

<template>
  <div class="row">
    <Avatar
      :image="'https://ambassadors.sytes.net/' + props.user?.image"
      size="xlarge"
      shape="circle"
    />
    <div>
      <p>{{ props.user?.last_name }}</p>
      <p>{{ props.user?.first_name }}</p>
      <p v-if="props.user.middle_name">{{ props.user.middle_name }}</p>
    </div>
  </div>
  <Divider
    align="left"
    type="solid"
    :pt="{
      content: { style: 'margin-left: 20px' },
    }"
  >
    <b>Контактная информация</b>
  </Divider>
  <p style="display: flex; align-items: center; gap: 10px">
    <img :src="phone" /> {{ props.user?.phone }}
  </p>

  <p style="display: flex; align-items: center; gap: 10px">
    <img :src="mail" /> {{ props.user?.email }}
  </p>

  <p style="display: flex; align-items: center; gap: 10px">
    <img :src="telegram" /> @{{ props.user?.tg_acc }}
  </p>
  <Divider
    align="left"
    type="solid"
    :pt="{
      content: { style: 'margin-left: 20px' },
    }"
  >
    <b>Почтовые реквизиты</b>
  </Divider>
  <div class="grid">
    <div>
      <p v-for="name in address">{{ name }}</p>
    </div>
    <div>
      <p v-for="item in props.user?.address">{{ item }}</p>
    </div>
  </div>
  <Divider
    align="left"
    type="solid"
    :pt="{
      content: { style: 'margin-left: 20px' },
    }"
  >
    <b>Учёба и работа</b>
  </Divider>
  <div class="grid">
    <div>
      <p>Программа обучения:</p>
      <p>Цель обучения:</p>
      <p>Образование:</p>
      <p>Работа:</p>
    </div>
    <div>
      <p>{{ props.user?.ya_programm }}</p>
      <p>{{ props.user?.purpose }}</p>
      <p>{{ props.user?.education }}</p>
      <p>{{ props.user?.work }}</p>
    </div>
  </div>
  <Divider
    align="left"
    type="solid"
    :pt="{
      content: { style: 'margin-left: 20px' },
    }"
  >
    <b>Данные для мерча</b>
  </Divider>
  <div class="grid">
    <div>
      <p v-for="name in sizes">{{ name }}</p>
    </div>
    <div>
      <p v-for="size in props.user.size">{{ size }}</p>
    </div>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  justify-content: start;
  align-items: center;
  gap: 5vh;
}
.fieldset {
  background-color: transparent;
}
/* @media (min-width: 800px) {
  .grid {
    display: grid;
    grid-template-columns: 400px 400px;
  }
} */

/* @media (max-width: 799.98px) { */
.grid {
  display: grid;
  grid-template-columns: 50% 50%;
}
/* } */
</style>
