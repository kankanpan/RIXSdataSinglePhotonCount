<script setup>
let api = Vue.inject('api')

const Chart = Vue.defineAsyncComponent(() =>
    loadModule("../components/graph.vue", options)
)

const tool_model = Vue.inject('tool_model')

let thres_data = Vue.ref({})
let thres_max = Vue.ref(100)


const emit = defineEmits(
    ['loadDone']
)

Vue.onMounted(async () => {
    const result = await api.clipImage()
    thres_data.value = result['data']
    thres_max.value = result['max']
    emit('loadDone')
})

</script>

<template>
    <Chart v-if="thres_data && Object.keys(thres_data).length > 0" type="line" :data="thres_data"></Chart>
    <v-range-slider v-model="tool_model.thres_range" :max="thres_max" :min="0" thumb-label step="1"></v-range-slider>
</template>