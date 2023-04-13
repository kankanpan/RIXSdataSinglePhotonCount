<script setup>
let api = Vue.inject('api')

const Chart = Vue.defineAsyncComponent(() =>
    loadModule("../components/graph.vue", options)
)

const chartRef = Vue.ref()
const images = Vue.ref()
const dest = Vue.ref({})

const base_images = Vue.inject('images')
const current_index = Vue.inject('current_index')

Vue.watch(current_index, (newValue, oldValue) => {
    if (!chartRef.value) return
    profileData()
    chartRef.value.dataUpdate()
})

const emit = defineEmits(
    ['loadDone']
)

function setInitLimit(img_size) {
    return [[0, img_size[1]], [0, img_size[0]]]
}

Vue.onMounted(async () => {
    emit('loadDone')
    images.value = base_images.value
    profileData()
})

async function autoFindRange() {
    const auto_range = await eel.autoFindRange()()
    if (auto_range) {
        // clip_range_w.value, clip_range_h.value = auto_range
    }
}

async function clipImagesProfile() {
    if (!chartRef.value) return
    const dists = await api.clipImageProfiles()
    images.value = images.value.map((img, index) => {
        img[2] = dists[index]
        return img
    })
    console.log(images)
    profileData()
    chartRef.value.dataUpdate()
}

function profileData() {
    let result = {}
    for (let i = 1; i <= 255; i++) {
        result[String(i)] = 0
    }
    for (const image of images.value.filter(i => current_index.value.includes(i[1]))) {
        for (let i = 1; i <= 255; i++) {
            result[String(i)] += isNaN(image[2][i]) ? 0 : image[2][i]
        }
    }
    console.log("result", result)
    dest.value = result
}

</script>

<template>
    <v-btn @click="clipImagesProfile">プロファイル更新</v-btn>
    <v-expansion-panels>
    <v-expansion-panel>
        <v-expansion-panel-title>
            Data profile
        </v-expansion-panel-title>
        <v-expansion-panel-text>
            <Chart ref="chartRef" type="line" :data="dest" :logscale="false"></Chart>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
    <!-- <v-row no-gutters>
        <v-col cols="12">
            <v-range-slider v-model="tool_model.clip_range_w" :max="tool_model_max.clip_range_w"
                :min="setInitLimit(image_size)[1][0]" thumb-label step="1"></v-range-slider>
        </v-col>
        <v-col cols="12">
            <v-range-slider v-model="tool_model.clip_range_h" :max="setInitLimit(image_size)[0][1]"
                :min="setInitLimit(image_size)[0][0]" thumb-label step="1"></v-range-slider>
        </v-col>
    </v-row> -->
</template>