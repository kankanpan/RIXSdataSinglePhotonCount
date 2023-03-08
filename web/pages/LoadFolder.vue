<script setup>
const api = Vue.inject('api')
const folder_path = Vue.inject('folder_path')

const props = defineProps({
    isDisabled: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(
    ['setFolderDone']
)

async function openFolder() {
    await api.openFolder()
    if (folder_path){
        emit('setFolderDone')
    }
}

</script>

<template>
    <v-btn
        variant="tonal"
        @click="openFolder"
        :disabled="props.isDisabled"
        class="text-capitalize"
    >
        {{ folder_path? folder_path: "Open Folder" }}
    </v-btn>
</template>
