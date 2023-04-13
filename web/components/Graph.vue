<script setup>
let canvasRef = Vue.ref(null)
let axis_range = Vue.ref([0, 0])

let chart_scales = Vue.ref({
    x: {
        display: true
    },
    y: {
        display: true,
        type: props.logscale ? 'logarithmic' : 'linear',
    }
})

const props = defineProps({
    data: Object,
    type: String,
    logscale: Boolean
})

Vue.onMounted(() => {
    if (canvasRef.value === null) return
    const canvas = canvasRef.value.getContext('2d')
    if (canvas === null) return
    const chart_instance = new Chart(canvas, {
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
            scales: chart_scales.value
        }
    })
    console.log("chart.value.scales.y", chart_instance.scales)
    axis_range.value = [chart_instance.scales.y.min, chart_instance.scales.y.max]
})

function changeRange(value, index) {
    if (!value) return
    
    const chart_instance = Chart.getChart("canvas-id")
    axis_range.value[index] = parseInt(value, 10)
    if (index == 0) {
        chart_scales.value.y.min = parseInt(value, 10)
    } else if (index == 1) {
        chart_scales.value.y.max = parseInt(value, 10)
    }
    chart_instance.options.scales = chart_scales.value
    chart_instance.update()

    return value
}

defineExpose({
    dataUpdate,
})

function dataUpdate() {
    const chart_instance = Chart.getChart("canvas-id")
    console.log("props.data", props.data)
    chart_instance.data.datasets[0].data = props.data
    chart_instance.update()
}

</script>

<template>
<canvas id="canvas-id" ref="canvasRef" />
<v-text-field @update:modelValue="v => changeRange(v, 0)" v-model="axis_range[0]" label="min"></v-text-field>
<v-text-field @update:modelValue="v => changeRange(v, 1)" v-model="axis_range[1]" label="max"></v-text-field>
</template>