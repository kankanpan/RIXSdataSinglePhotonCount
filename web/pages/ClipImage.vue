<script setup>
const Chart = Vue.defineAsyncComponent(() =>
    loadModule("../components/graph.vue", options)
)


const images = Vue.inject('images')
const current_index = Vue.inject('current_index')

const emit = defineEmits(
    ['loadDone']
)

function setInitLimit(img_size) {
    return [[0, img_size[1]], [0, img_size[0]]]
}

Vue.onMounted(async () => {
    emit('loadDone')
})

async function autoFindRange() {
    const auto_range = await eel.autoFindRange()()
    if (auto_range) {
        // clip_range_w.value, clip_range_h.value = auto_range
    }
}

function profileData() {
    let result = {}
    for (let i = 1; i <= 255; i++) {
        result[String(i)] = 0
    }
    console.log(images.value.filter(i => current_index.value.includes(i[1])))
    for (const image of images.value.filter(i => current_index.value.includes(i[1]))) {
        image[2]
        for (let i = 1; i <= 255; i++) {
            result[String(i)] += image[2][String(i)]
        }
    }
    console.log("result", result)
    return result
}

</script>

<template>
    <v-expansion-panels>
    <v-expansion-panel>
        <v-expansion-panel-title>
            Data profile
        </v-expansion-panel-title>
        <v-expansion-panel-text>
            <Chart type="line" :data="profileData()" :logscale="true"></Chart>
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