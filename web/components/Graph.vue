<script setup>
let canvasRef = Vue.ref(null)
let chart = Vue.ref(null)
let axis_range = Vue.ref([0, 0])

const props = defineProps({
    data: Object,
    type: String,
    logscale: Boolean
})

Vue.onMounted(() => {
    if (canvasRef.value === null) return
    const canvas = canvasRef.value.getContext('2d')
    if (canvas === null) return
    chart.value = new Chart(canvas, {
        type: props.type,
        data: {
            datasets: [{
                data: props.data
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    display: true,
                },
                y: {
                    display: true,
                    type: props.logscale ? 'logarithmic' : 'linear',
                }
            }
        }
    })
    console.log("chart.value.scales.y", chart.value.scales)
    axis_range.value = [chart.value.scales.y.min, chart.value.scales.y.max]
})

function changeRange(value) {
    console.log(parseInt(value, 10))
    console.log(axis_range.value[1])
    console.log(chart.value.options.scales.y)
    chart.value.options.scales.y = {
        ...chart.value.options.scales.y,
        max: parseInt(value, 10)
    }
    // chart.value.scales.linear.min = axis_range.value[0]
    const result = chart.value.update()
    console.log(result)
    return value
}

</script>

<template>
<canvas ref="canvasRef" />
<!-- <v-text-field @update:modelValue="changeRange" v-model="axis_range[0]" label="min"></v-text-field>
<v-text-field @update:modelValue="changeRange" v-model="axis_range[1]" label="max"></v-text-field> -->
</template>