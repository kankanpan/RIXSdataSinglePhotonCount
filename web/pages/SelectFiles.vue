<script setup>
const props = defineProps({
    isDisabled: {
        type: Boolean,
        default: false
    },
    size: {
        type: Number,
        default: 600
    }
})

const tool_model = Vue.inject('tool_model')
const images = Vue.inject('images')
const current_index = Vue.inject('current_index')
const api = Vue.inject('api')
const file_names = Vue.inject('file_names')

let on_load = Vue.ref(false)

const emit = defineEmits(
    ['setImageDone']
)

async function loadImage(value) {
    on_load.value = true
    await api.loadImages(value)
    emit('setImageDone')
    on_load.value = false
}



async function setIndex(index) {
    current_index.value = [index]
}

</script>

<template>
    <template v-if="file_names">
        <v-sheet color="white" :width="props.size">
            <v-select
                :items="file_names"
                item-title="path"
                item-value="id"
                @update:modelValue="loadImage"
                :disabled="isDisabled || on_load"
                :loading="on_load"
                label="Select Data"
                outlined
            ></v-select>
            <v-row v-if="images" class="pr-1">
                <v-col v-for="i in images" :key="i[1]" class="d-flex child-flex" cols="4" @click="setIndex(i[1])" :class="current_index[0] == i[1] ? 'current' : '' ">
                    <v-chip variant="elevated" size="small" class="abs">
                        {{ i[1] > -1 ? "layer number :" + i[1] : "background" }}
                    </v-chip>
                    <v-img :src="i[0]" aspect-ratio="1" class="bg-white filters" v-bind:style="{ filter: 'brightness(' + tool_model.bright + ') contrast(' + tool_model.contrast + ')' }" >
                        <template v-slot:placeholder>
                            <v-row class="fill-height ma-0" align="center" justify="center">
                                <v-progress-circular indeterminate color="grey-lighten-5"></v-progress-circular>
                            </v-row>
                        </template>
                    </v-img>
                </v-col>
            </v-row>
        </v-sheet>
    </template>
    <v-progress-circular v-else :size="70" :width="7" color="green" indeterminate></v-progress-circular>
</template>

<style scoped>
.abs {
    position: absolute;
    z-index: 1;
    margin-top: 4px;
    margin-left: 4px;
}
.filters {
    border: solid 1px;
}
.current {
    border: solid 2px red;
}
</style>