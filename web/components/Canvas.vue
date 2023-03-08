<script setup>
const select_point_num = Vue.ref(-1)

const tool_model = Vue.inject('tool_model')
const image_size = Vue.inject('image_size')
const result_data = Vue.inject('result_data')

const images = Vue.inject('images')
const current_index = Vue.inject('current_index')

const props = defineProps({
    size: {
        type: Number,
        default: 550
    },
    is_clip_mode: {
        type: Boolean,
        default: false
    },
    data: {
        type: Array,
        default: null
    },
    disabled: {
        type: Boolean,
        default: true
    }
})
const emit = defineEmits(
    ['selectPoint']
)

function emitSelectPoint(index) {
    select_point_num.value = index
    emit('selectPoint', index)
}

let color_range = Vue.ref([0, 255])
let image_dom = Vue.ref(null)

function getViewSize() {
    if (!props.is_clip_mode) {
        let image_size_array = [0, 0]
        image_size_array[1] = tool_model.value.clip_range_w[1] - tool_model.value.clip_range_w[0]
        image_size_array[0] = tool_model.value.clip_range_h[1] - tool_model.value.clip_range_h[0]
        return image_size_array
    } else {
        return image_size.value
    }
}

function getAspect() {
    return getViewSize()[1] / getViewSize()[0]
}

function setTable() {
    const offset = 0.5
    return new Array(
        Math.trunc(tool_model.value.thres_range[0])
    ).fill(1).concat(
        new Array(
            Math.trunc(tool_model.value.thres_range[1]) - Math.trunc(tool_model.value.thres_range[0])
        ).fill(1).map(
            (x, i) => (i / ( Math.trunc(tool_model.value.thres_range[1]) - Math.trunc(tool_model.value.thres_range[0]) ) ) * offset
        )
    ).concat(
        new Array(
            255 - Math.trunc(tool_model.value.thres_range[1])
        ).fill(1)
    ).join(' ')
}

function setAll() {
    current_index.value = images.value.map(i => i[1]).filter(i => i >= 0)
}

</script>

<template>
    <v-btn @click="setAll">select all layer</v-btn>
    <v-combobox v-model="current_index" :items="images.map(i => i[1])" label="I use chips" multiple chips></v-combobox>
    <div class="wrapper">
        <template v-for="img in images" :key="img[1]">
            <svg v-if="current_index.includes(img[1])" class="image" :style="('margin-top: -' + getAspect() < 1 ? props.size : props.size / getAspect() + 'px')" :width="getAspect() > 1 ? props.size : props.size * getAspect()" :height="getAspect() < 1 ? props.size : props.size / getAspect()"
                :viewBox="'0, 0, ' + getViewSize()[1] + ', ' + getViewSize()[0]" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <filter id="table" x="0" y="0" width="100%" height="100%">
                        <feComponentTransfer>
                            <feFuncR type="table"
                                :tableValues="setTable()">
                            </feFuncR>
                            <feFuncG type="table"
                                :tableValues="setTable()">
                            </feFuncG>
                            <feFuncB type="table"
                                :tableValues="setTable()">
                            </feFuncB>
                        </feComponentTransfer>
                        <feMorphology operator="erode" :radius="tool_model.blur" />
                    </filter>
                    <clipPath id="cut-off-bottom">
                        <rect :width="tool_model.clip_range_w[1] - tool_model.clip_range_w[0]"
                            :height="tool_model.clip_range_h[1] - tool_model.clip_range_h[0]" />
                    </clipPath>
                </defs>
                <image :href="img[0]" :width="image_size[1]" :height="image_size[0]" ref="image_dom" :style="props.is_clip_mode ? 'filter:url(#table)' : 'filter:url(#table) url(#clip-offset)'"
                    :clip-path="props.is_clip_mode ? '' : 'url(#cut-off-bottom)'" :x="props.is_clip_mode ? 0 : -tool_model.clip_range_w[0]" :y="props.is_clip_mode  ? 0 : -tool_model.clip_range_h[0]" />
            </svg>
        </template>
        <svg v-if="props.is_clip_mode" :width="getAspect() > 1 ? props.size : props.size * getAspect()" :height="getAspect() < 1 ? props.size : props.size / getAspect()"
                :viewBox="'0, 0, ' + getViewSize()[1] + ', ' + getViewSize()[0]" xmlns="http://www.w3.org/2000/svg">
            <rect :x="tool_model.clip_range_w[0]" :y="tool_model.clip_range_h[0]" :width="tool_model.clip_range_w[1] - tool_model.clip_range_w[0]"
                        :height="tool_model.clip_range_h[1] - tool_model.clip_range_h[0]" stroke-width="5" stroke="red" fill-opacity="0" />
        </svg>

        <!-- <image v-if="result_image" :href="result_image" /> -->

        <svg v-if="!props.is_clip_mode" :width="getAspect() > 1 ? props.size : props.size * getAspect()" :height="getAspect() < 1 ? props.size : props.size / getAspect()"
                    :viewBox="'0, 0, ' + getViewSize()[1] + ', ' + getViewSize()[0]" xmlns="http://www.w3.org/2000/svg">
            <template v-for="(d, index) in result_data" :key="d[0]">
                <text text-anchor="middle" dominant-baseline="central"
                    :style="{ fill: d[0] == select_point_num.value ? 'red' : 'green' }" :x="d[2]" :y="d[3]" font-size="20"
                    @click="emitSelectPoint(index)">+</text>
            </template>
        </svg>
    </div>
</template>

<style scoped>
svg {
    position: absolute;
}
.wrapper {
    height: v-bind(props.size + 'px');
    position: relative;
    display: block;
    margin: 10px;
}

.image {
    mix-blend-mode: v-bind(current_index.length > 1 ? 'darken' : 'nomal');
}

text {
    cursor: pointer;
}</style>
