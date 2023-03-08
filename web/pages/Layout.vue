<script setup>
const Header = Vue.defineAsyncComponent(() =>
    loadModule("../components/Header.vue", options)
)
const SideMenu = Vue.defineAsyncComponent(() =>
    loadModule("../components/SideMenu.vue", options)
)
const PageWindow = Vue.defineAsyncComponent(() =>
    loadModule("../components/PageWindow.vue", options)
)
const loadFolder = Vue.defineAsyncComponent(() =>
    loadModule("./pages/LoadFolder.vue", options)
)
const SelectFiles = Vue.defineAsyncComponent(() =>
    loadModule("./pages/SelectFiles.vue", options)
)
const ClipImage = Vue.defineAsyncComponent(() =>
    loadModule("./pages/ClipImage.vue", options)
)
const ChangeThreshold = Vue.defineAsyncComponent(() =>
    loadModule("./pages/ChangeThreshold.vue", options)
)
const ViewResults = Vue.defineAsyncComponent(() =>
    loadModule("./pages/ViewResults.vue", options)
)
const BottomNav = Vue.defineAsyncComponent(() =>
    loadModule("../components/BottomNav.vue", options)
)
const MyCanvas = Vue.defineAsyncComponent(() =>
    loadModule("../components/canvas.vue", options)
)

let step = Vue.ref(1)
Vue.provide('step', step)
let allowStep = Vue.ref(1)
Vue.provide('allowStep', allowStep)

const tool_model = Vue.inject('tool_model')
const api = Vue.inject('api')

const display = Vuetify.useDisplay()

const contents = Vue.inject('contents')

// eel.expose(setFile)
// function setFile() {
//     console.log("test")
// }

function sizeFix(display_width, mag) {
    // return display_width > 746 ? display_width - 146 : 600
    return (display.width.value - 100) * mag
}

const emit = defineEmits(
    ['exit']
)

</script>

<template>
    <Header @exit="emit('exit')"></Header>
    <SideMenu>
        <v-list-item @click="api.showDB" prepend-icon="mdi-folder" title="show db" value="myfiles"></v-list-item>
        <v-list-item @click="api.clearDB" prepend-icon="mdi-account-multiple" title="clear db" value="shared"></v-list-item>
        <v-list-item @click="api.test" prepend-icon="mdi-folder" title="test" value="test"></v-list-item>
    </SideMenu>
    <v-main id="main" scrollable="true">
        <PageWindow :allowStep="allowStep" :contents="contents" :width="(display.width.value - 100) * tool_model.size_mag"
            @prePage="step--" @nextPage="step++">
            <template #page-1>
                <loadFolder @setFolderDone="allowStep = 2"></loadFolder>
            </template>
            <template #page-2>
               <SelectFiles :size="sizeFix(display.width.value, tool_model.size_mag)-20"
                @setImageDone="allowStep = 5"></SelectFiles>
            </template>
            <template #page-3>
                <ClipImage :size="sizeFix(display.width.value, tool_model.size_mag)" @loadDone="allowStep = 5"></ClipImage>
            </template>
            <template #page-4>
               <ViewResults :thres_range="thres_range" :size="sizeFix(display.width.value, tool_model.size_mag)"></ViewResults>
            </template>
            <!-- <v-progress-circular :size="70" :width="7" color="green" indeterminate></v-progress-circular> -->
            <MyCanvas
                v-if="step > 2"
                :is_clip_mode="step == 3"
                :size="sizeFix(display.width.value, tool_model.size_mag)-20"
            ></MyCanvas>
        </PageWindow>
    </v-main>
    <BottomNav :tool_set="contents[step-1]['tools']"></BottomNav>
</template>