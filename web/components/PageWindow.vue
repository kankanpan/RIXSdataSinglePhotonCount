<script setup>
const props = defineProps({
    width: {
        type: Number
    }
})

const step = Vue.inject('step')
const allowStep = Vue.inject('allowStep')
const contents = Vue.inject('contents')
</script>

<template>
    <v-card class="rounded-lg elevation-6 mx-auto mt-4 mb-16" :width="props.width">
        <v-card-title class="text-h6 font-weight-regular justify-space-between">
            <v-avatar color="primary" size="24" v-text="step" class="mr-1"></v-avatar>
            <strong>{{ contents[step-1]["title"] }}</strong>
        </v-card-title>
        <v-card-actions>
            <v-btn v-if="step > 1" variant="text" @click="step--">
                Back
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn v-if="step < contents.length" color="primary" variant="flat" @click="step++" :disabled="allowStep <= step">
                Next
            </v-btn>
        </v-card-actions>
        <v-divider></v-divider>
        <v-window v-model="step">
            <v-window-item v-for="p of contents.length" :key="p" :value="p" class="ma-4">
                <slot :name="'page-' + p"></slot>
            </v-window-item>
        </v-window>
        <slot></slot>
    </v-card>
</template>