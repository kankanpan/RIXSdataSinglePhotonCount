<script setup>
const tool_model = Vue.inject('tool_model')
const tool_model_max = Vue.inject('tool_model_max')

let folder_path = Vue.ref("")
Vue.provide('folder_path', folder_path)

let file_names = Vue.ref([])
Vue.provide('file_names', file_names)

let images = Vue.ref([])
Vue.provide('images', images)

let result_image = Vue.ref("")
Vue.provide('result_image', result_image)

let image_size = Vue.ref([0, 0])
Vue.provide('image_size', image_size)

let current_index = Vue.ref([0])
Vue.provide('current_index', current_index)

let file_id = Vue.ref("")
Vue.provide('file_id', file_id)

let result_data = Vue.ref([])
Vue.provide('result_data', result_data)

async function showDB() {
    return await eel.showDb()()
}

function clearDB() {
    eel.dbClear()()
}

const openFolder = async () => {
    const open_folder_path = await eel.openLocalFolder()()
    if (open_folder_path) {
        folder_path.value = open_folder_path
        file_names.value = await eel.loadFiles()()
    }
}

const loadImages = async (id) => {
    if (!id) return
    console.log("id", id)
    file_id.value = id
    images.value = []
    await eel.loadFile(id)()
}

eel.expose(setImage)
function setImage(results) {
    images.value = results
    console.log("images", images)
    api.loadImage()
}

const loadImage = async () => {
    const result = await eel.setCurrentFile(file_id.value, 0)()
    if (result && result['size']) {
        image_size.value = result['size']
        tool_model_max.value.clip_range_w = result['size'][1]
        tool_model_max.value.clip_range_h = result['size'][0]
        tool_model.value.clip_range_w = [0, result['size'][1]]
        tool_model.value.clip_range_h = [0, result['size'][0]]
    }
}

const clipImage = async () => {
    let ip = await eel.clipImage([tool_model.value.clip_range_w, tool_model.value.clip_range_h])()
    tool_model_max.value.thres_range = ip['max'] + 0
    tool_model.value.thres_range[1] = ip['max'] + 0
    return {'data': ip['dist'], 'max': ip['max'] + 0}
}

const photonCount = async () => {
    // {"raw_img": clip_dset, "result_img": result_img, "size": np.shape(clip_dset), "results": single_count_list, "max": dset_max}
    // let ip = await eel.photonCount(
    //     file_id.value,
    //     current_index.value,
    //     [tool_model.value.clip_range_h, tool_model.value.clip_range_w],
    //     tool_model.value.thres_range
    // )()
    
    const prom = [];
    for (const index of current_index.value) {
        if (index < 0) continue
        prom.push(
            eel.photonCount(
                file_id.value,
                index,
                [tool_model.value.clip_range_h, tool_model.value.clip_range_w],
                tool_model.value.thres_range
            )()
        )
    }
    const results = await Promise.all(prom)
    
    console.log("photonCount", results)
    result_image.value = results[0]['result_img']
    
    let all_results = []
    for (const result of results) {
        console.log("result['results']", result['results'])
        all_results = all_results.concat(result['results'].map(x => {
            x.push(result['index'])
            return x
        }))
    }
    console.log("all_results", all_results)
    return all_results
}

const test = async () => {
    await eel.test()()
    console.log("test Done")
}

const saveCSV = async (title, data) => {
    await eel.saveCSV(title, data)()
}

const saveIgor = async (title, data) => {
    await eel.saveIgor(title, data)()
}

const api = {
    'test': test,
    'openFolder': openFolder,
    'loadImage': loadImage,
    'loadImages': loadImages,
    'showDB': showDB,
    'clearDB': clearDB,
    'clipImage': clipImage,
    'photonCount': photonCount,
    'saveCSV': saveCSV,
    'saveIgor': saveIgor
}
Vue.provide('api', api)

</script>

<template>
    <slot></slot>
</template>