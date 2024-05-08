<script setup lang="ts">
import Stepper from 'primevue/stepper';
import StepperPanel from 'primevue/stepperpanel';
import { ref } from 'vue';
import { IUser } from '../../types/types';

const props = defineProps<{ user: IUser }>();
const steps = { new: 0, friend: 1, profi_friend: 2 };

const active = ref(steps[props.user?.achievement]);
</script>

<template>
  <Stepper orientation="vertical" v-model:activeStep="active" linear>
    <StepperPanel header="Новичок">
      <template #content>
        <div class="flex flex-column h-12rem">
          <div
            class="border-2 border-dashed surface-border border-round surface-ground flex-auto flex justify-content-center align-items-center font-medium"
          >
            <p>Мы только познакомились, у тебя всё впереди!</p>
            <p>Чтобы достичь следующего звания тебе необходимо написать 1 отзыв.</p>
          </div>
        </div>
      </template>
    </StepperPanel>
    <StepperPanel header="Друг Практикума">
      <template #content>
        <div class="flex flex-column h-12rem">
          <div
            class="border-2 border-dashed surface-border border-round surface-ground flex-auto flex justify-content-center align-items-center font-medium"
          >
            <p>Поздравляем! Мы рады, что ты с нами, и в качестве награды пришлем тебе подарок :)</p>
            <p>Чтобы достичь следующего звание тебе необходимо выложить контент 5 раз</p>
          </div>
        </div>
      </template>
    </StepperPanel>
    <StepperPanel header="Амбассадор Практикума">
      <template #content>
        <div class="flex flex-column h-12rem">
          <div
            class="border-2 border-dashed surface-border border-round surface-ground flex-auto flex justify-content-center align-items-center font-medium"
          >
            <p>
              Ого! Поздравляем, теперь ты Амбассадор! Скоро мы отправим твой заслуженный приз :)
            </p>
            <p>
              На текущий момент мы одарили тебя всем, что у нас есть, но мы будем очень рады, если
              ты продолжишь выкладывать контент с нами :)
            </p>
          </div>
        </div>
      </template>
    </StepperPanel>
  </Stepper>
</template>
