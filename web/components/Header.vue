<script setup>
const emit = defineEmits(
    ['exit']
)
</script>

<template>
    <v-app-bar color="primary" prominent>
            <v-toolbar-title>RIXS data single photon count</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon @click="emit('exit')">
                <v-icon>mdi-export</v-icon>
                <v-tooltip activator="parent" location="bottom">終了する</v-tooltip>
            </v-btn>
        </v-app-bar>
</template>