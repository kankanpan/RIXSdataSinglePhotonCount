<script setup>
let drawer = Vue.ref(false)

const step = Vue.inject('step')
const contents = Vue.inject('contents')
</script>

<template>
    <v-navigation-drawer permanent expand-on-hover rail location="left" @update:rail="drawer = !drawer">
        <v-list density="compact" nav>
            <slot></slot>
        </v-list>
        <v-divider></v-divider>
        <v-timeline density="compact" class="ml-1" truncate-line="both">
            <v-timeline-item v-for="(c, i) in contents" :key="c['title']" :dot-color="step - 1 == i ? 'primary' : 'white'"
                :size="step - 1 == i ? 'large' : 'small'" :icon="c['icon']">
                <h4><v-avatar color="primary" size="20" v-text="i + 1" class="mr-1"></v-avatar>{{ c["title"] }}</h4>
            </v-timeline-item>
        </v-timeline>
    </v-navigation-drawer>
</template>