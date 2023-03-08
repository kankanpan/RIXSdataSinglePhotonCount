<script setup>
const Layout = Vue.defineAsyncComponent(() =>
    loadModule("./pages/Layout.vue", options)
)

const Api = Vue.defineAsyncComponent(() =>
    loadModule("./api.vue", options)
)

let theme = Vue.ref("light")

const contents = [
    {
        "title": "Open Folder",
        "icon": "mdi-folder-open",
        "tools": null
    }, {
        "title": "Open File",
        "icon": "mdi-file-import",
        "tools": ["size_mag", "bright", "contrast"]
    }, {
        "title": "Count Setting",
        "icon": "mdi-chart-sankey",
        "tools": ["size_mag", "clip_range_w", "clip_range_h", "thres_range", "blur"]
    }, {
        "title": "Single Photon Count",
        "icon": "mdi-select-group",
        "tools": ["size_mag", "thres_range", "blur"]
    }
]
Vue.provide('contents', contents)

const tools = {
    'size_mag': {
        'name': 'Window Size',
        'icon': 'mdi-image-size-select-large',
        'default': 1,
        'min': 0.01,
        'max': 5,
        'step': 0.1,
        'prefix': 'x',
        'is_range': false
    },
    'clip_range_w': {
        'name': 'Clipping Width',
        'icon': 'mdi-arrow-split-vertical',
        'default': [0,100],
        'min': 0,
        'max': 100,
        'step': 1,
        'prefix': 'pixcel',
        'is_range': true
    },
    'clip_range_h': {
        'name': 'Clipping Height',
        'icon': 'mdi-arrow-split-horizontal',
        'default': [0, 100],
        'min': 0,
        'max': 100,
        'step': 1,
        'prefix': 'pixcel',
        'is_range': true
    },
    'bright': {
        'name': 'Brightness',
        'icon': 'mdi-format-color-highlight',
        'default': 1,
        'min': 0,
        'max': 100,
        'step': 0.01,
        'prefix': '',
        'is_range': false
    },
    'contrast': {
        'name': 'Contrast',
        'icon': 'mdi-chart-sankey',
        'default': 1,
        'min': 0,
        'max': 20,
        'step': 0.01,
        'prefix': '',
        'is_range': false
    },
    'blur': {
        'name': 'Expand',
        'icon': 'mdi-format-color-highlight',
        'default': 0,
        'min': 0,
        'max': 100,
        'step': 0.1,
        'prefix': '',
        'is_range': false
    },
    'thres_range': {
        'name': 'Threshold',
        'icon': 'mdi-chart-sankey',
        'default': [0, 255],
        'min': 0,
        'max': 255,
        'step': 0.01,
        'prefix': '',
        'is_range': true
    }
}
Vue.provide('tools', tools)

const tool_model = Vue.ref({
    size_mag: tools['size_mag']['default'],
    clip_range_w: tools['clip_range_w']['default'],
    clip_range_h: tools['clip_range_h']['default'],
    bright: tools['bright']['default'],
    contrast: tools['contrast']['default'],
    blur: tools['blur']['default'],
    thres_range: tools['thres_range']['default']
})
Vue.provide('tool_model', tool_model)

const tool_model_max = Vue.ref({
    size_mag: tools['size_mag']['max'],
    clip_range_w: tools['clip_range_w']['max'],
    clip_range_h: tools['clip_range_h']['max'],
    bright: tools['bright']['max'],
    contrast: tools['contrast']['max'],
    blur: tools['blur']['max'],
    thres_range: tools['thres_range']['max']
})
Vue.provide('tool_model_max', tool_model_max)

function exit() {
    window.close()
}

</script>

<template>
<v-app :theme="theme">
    <Api>
        <Layout
            @exit="exit"
        ></Layout>
    </Api>
</v-app>
</template>