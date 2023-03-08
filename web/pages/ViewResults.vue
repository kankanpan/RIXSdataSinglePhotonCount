<script setup>
const Chart = Vue.defineAsyncComponent(() =>
    loadModule("../components/graph.vue", options)
)

const props = defineProps({
    size: {
        type: Number,
        default: 600
    }
})

let api = Vue.inject('api')
let result_data = Vue.inject('result_data')

const emit = defineEmits(
    ['timelineBack']
)

let count_peak = Vue.ref([])

Vue.onMounted(async () => {
    await photonCount()
})

const photonCount = async () => {
    const result = await api.photonCount()
    result_data.value = result.map((d, i) => [i, d[3], d[1], d[0], d[2]])
    count_peak.value = countX(result, 4, true)
}

function countX(data_array, width, include_int = false) {
    let result = {}
    for (const d of data_array) {
        let key = Math.floor(d[1] / width)
        key *= width
        let int = include_int ? d[3] : 1
        if (key in result === false) {
            result[key] = int
        } else {
            result[key] += int
        }
    }
    return result
}

function saveCSV() {
    api.saveCSV(['index', 'layer number', 'x', 'y', 'intensity'], result_data.value)
}

function saveIgor() {
    api.saveIgor(['index', 'layer number', 'x', 'y', 'intensity'], result_data.value)
}

</script>

<template>
    <v-btn @click="photonCount">retray</v-btn>
    <v-btn @click="saveCSV">save as CSV</v-btn>
    <v-btn @click="saveIgor">save as Igor text</v-btn>
    <v-table fixed-header height="300px">
        <thead>
            <tr>
                <th class="text-left">
                    index
                </th>
                <th class="text-left">
                    layer
                </th>
                <th class="text-left">
                    x
                </th>
                <th class="text-left">
                    y
                </th>
                <th class="text-left">
                    intensity
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in result_data" :key="item[0]">
                <td>{{ item[0] }}</td>
                <td>{{ item[1] }}</td>
                <td>{{ item[2] }}</td>
                <td>{{ item[3] }}</td>
                <td>{{ item[4] }}</td>
            </tr>
        </tbody>
    </v-table>
    <v-expansion-panels>
        <v-expansion-panel>
            <v-expansion-panel-title>
                X profile
            </v-expansion-panel-title>
            <v-expansion-panel-text>
                <Chart type="line" :data="count_peak"></Chart>
            </v-expansion-panel-text>
        </v-expansion-panel>
    </v-expansion-panels>
</template>