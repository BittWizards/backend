<script setup lang="ts">
import { Ref, onMounted, ref } from 'vue';
import Chart, { ChartSelectEvent } from 'primevue/chart';
import { IData, IUserContent } from '../../types/types';
import { ChartDataset } from 'chart.js';

const props = defineProps<{ data: IUserContent }>();

const platformColors: { [key: string]: string } = {
  habr: '#408080', // 65A3BE 408080
  VC: '#e8c4d7', // FEEBEF e8c4d7
  youtube: '#ff5c5c', // FF0000 ff5c5c
  telegram: '#3fc1c9', // 26A5E4 3fc1c9
  instagram: '#ff62a7', // E4405F ff62a7
  linkedin: '#0077b5', // 0A66C2 0077b5
  other: '#6f6f6f',
};
const dateCategoryList: ('halfYear' | 'month' | 'day')[] = ['halfYear', 'month', 'day'];
const dateCategory = { halfYear: 'Month', month: 'Date', day: 'Hours' };
const titleCategory = {
  halfYear: 'Статистика за последние полгода',
  month: 'Статистика за ',
  day: 'Статистика ',
};

const currentChart: Ref<'halfYear' | 'month' | 'day'> = ref('halfYear');
const choosedDate: Ref<Date> = ref(new Date());
const chart: Ref<Chart | null> = ref(null);

const sixMonthsAgo = new Date();
sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
sixMonthsAgo.setDate(1);

const sixMonthsContent = props.data.my_content.filter(
  (content) => new Date(content.created_at) >= sixMonthsAgo
);

const createData = (category: 'halfYear' | 'month' | 'day', date: Date) => {
  const data = [];
  category !== 'day' && date.setDate(1);
  date.setHours(0);
  const end = category === 'halfYear' ? new Date() : new Date(date.getFullYear(), 0);
  category !== 'halfYear' &&
    end.setMonth(category === 'month' ? date.getMonth() + 1 : date.getMonth()) &&
    end.setDate(category === 'day' ? date.getDate() + 1 : date.getDate());
  for (
    let i = new Date(date);
    i < end;
    i[`set${dateCategory[category]}` as 'setMonth' | 'setDate' | 'setHours'](
      i[`get${dateCategory[category]}` as 'getMonth' | 'getDate' | 'getHours']() + 1
    )
  ) {
    const xLabel =
      category === 'halfYear'
        ? i.toLocaleString('default', { month: 'long' })
        : i[`get${dateCategory[category]}` as 'getMonth' | 'getDate' | 'getHours']().toString();
    const groupContent: IData = { x: xLabel };
    sixMonthsContent
      .filter((content) => {
        const date = new Date(content.created_at);
        return (
          date.getMonth() === i.getMonth() &&
          (category === 'halfYear' || date.getDate() === i.getDate()) &&
          (category === 'halfYear' || category === 'month' || date.getHours() === i.getHours())
        );
      })
      .forEach((content) => {
        if (!groupContent[content.platform]) {
          groupContent[content.platform] = [];
        }
        groupContent[content.platform]!.push(content);
      });
    data.push(groupContent);
  }
  return data;
};

const monthsData = createData('halfYear', sixMonthsAgo);

const dataset: ChartDataset<'bar', IData[]>[] = [];
Object.keys(platformColors).forEach((platform) => {
  dataset.push({
    label: platform,
    data: monthsData,
    parsing: { yAxisKey: `${platform}.length` },
    backgroundColor: platformColors[platform],
  });
});

onMounted(() => {
  chartData.value = setChartData();
  chartOptions.value = setChartOptions();
});

const chartData = ref();
const chartOptions = ref();

const setChartData = () => {
  return {
    datasets: dataset,
  };
};

const test = (e: ChartSelectEvent) => {
  const months = [
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
  ];
  const test = chart.value!.getChart();
  const xLabel = e.element.element.$context.raw.x;
  const nextCategory =
    dateCategoryList[
      dateCategoryList.indexOf(currentChart.value) === 2
        ? 0
        : dateCategoryList.indexOf(currentChart.value) + 1
    ];
  nextCategory === 'halfYear' && (choosedDate.value = new Date(sixMonthsAgo));
  const date = choosedDate.value;
  nextCategory === 'month' && date.setMonth(months.indexOf(xLabel));
  nextCategory === 'day' && date.setDate(xLabel);
  const data = createData(
    nextCategory,
    date > new Date() ? new Date(date.setFullYear(date.getFullYear() - 1)) : new Date(date)
  );
  test.data.labels = [];
  test.data.datasets.forEach((dataset: ChartDataset<'bar', IData[]>) => (dataset.data = data));
  test.options.plugins.title.text =
    titleCategory[nextCategory] +
    (nextCategory !== 'halfYear'
      ? nextCategory === 'month'
        ? choosedDate.value.toLocaleString('default', { month: 'long', year: 'numeric' })
        : choosedDate.value.toLocaleString('default', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
          })
      : '');
  currentChart.value = nextCategory;
};

const setChartOptions = () => {
  const documentStyle = getComputedStyle(document.documentElement);
  const textColor = documentStyle.getPropertyValue('--text-color');
  const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
  const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

  return {
    aspectRatio: 2,
    plugins: {
      title: {
        display: true,
        color: textColor,
        font: { size: 20, weight: 'normal' },
        text: 'Статистика за последние полгода',
      },
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      legend: {
        labels: {
          color: textColor,
        },
      },
    },
    scales: {
      x: {
        stacked: true,
        ticks: {
          color: textColorSecondary,
        },
        grid: {
          color: surfaceBorder,
        },
      },
      y: {
        stacked: true,
        suggestedMax: 5,
        ticks: {
          display: true,
          callback: (v: number) => (v % 1 === 0 ? v : undefined),
          color: textColorSecondary,
        },
        grid: {
          color: surfaceBorder,
        },
      },
    },
  };
};
</script>

<template>
  <Chart type="bar" :data="chartData" :options="chartOptions" v-on:select="test" ref="chart" />
  <br />
  <p>Всего контента выложено: {{ data.my_content.length }}</p>
</template>
