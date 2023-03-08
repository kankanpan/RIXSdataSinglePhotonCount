<script setup>

const props = defineProps({
    tool_set: {
        type: Array,
        default: null
    }
})
const display = Vuetify.useDisplay()

const tool_model = Vue.inject('tool_model')
const tool_model_max = Vue.inject('tool_model_max')
const tools = Vue.inject('tools')

</script>

<template>
    <v-bottom-navigation grow elevation="10" v-if="props.tool_set">
        <template v-for="(name, index) in props.tool_set" :key="name + index">
            <v-btn :value="tools[name]['name'] + index" :id="`${name + index}-menu`">
                <v-icon>{{ tools[name]['icon'] }}</v-icon>
                {{ tools[name]['name'] }}
            </v-btn>
            <v-menu :activator="`#${name + index}-menu`" :close-on-content-click="false">
                <v-sheet :width="display.width.value - 80" class="pt-2">
                    <v-range-slider v-if="tools[name]['is_range']" v-model="tool_model[name]" :min="tools[name]['min']" :max="tool_model_max[name]" :step="tools[name]['step']">
                        <template v-slot:prepend>
                            <v-icon @click="tool_model[name] = tools[name]['default']">mdi-restore</v-icon>
                            <p class="ml-2 mr-2">{{ tools[name]['prefix'] }}</p>
                            <p>{{ tool_model[name][0] + ', ' + tool_model[name][1] }}</p>
                        </template>
                    </v-range-slider>
                    <v-slider v-else v-model="tool_model[name]" :min="tools[name]['min']" :max="tool_model_max[name]" :step="tools[name]['step']">
                        <template v-slot:prepend>
                            <v-icon @click="tool_model[name] = tools[name]['default']">mdi-restore</v-icon>
                            <p class="ml-2 mr-2">{{ tools[name]['prefix'] }}</p>
                            <p>{{ tool_model[name] }}</p>
                        </template>
                    </v-slider>
                </v-sheet>
            </v-menu>
        </template>
    </v-bottom-navigation>
</template>