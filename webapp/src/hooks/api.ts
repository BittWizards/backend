import axios from 'axios';
import { ref, type Ref } from 'vue';

export function useFetch<T>(url: string) {
  const data: Ref<T | null> = ref(null);
  const error: Ref<Error | null> = ref(null);

  axios
    .get<T>(url)
    .then((res) => (data.value = res.data))
    .catch((err) => (error.value = err));

  return { data, error };
}
