<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { electron_renderer_invoke } from '@renderer/lib/utils';
import Button from 'primevue/button';


interface StreamSource {
    source_type: string
    source_name: string
    source_id: string
    enable_recording: boolean
    connection_params: {
        address: string
        channel: string
        password: string
        username: string
    }
}

interface FilterChain {
    name: string,
    params: object
}
interface Filter {
    camera_name: string
    input_src: string
    output_src: string
    enable_recording: boolean
    filters_chain: FilterChain[]
}


interface FilterVideo {
    name?: string
    input_src?: string
    video?: HTMLMediaElement
}

const main_video = ref<FilterVideo>({})
const all_videos = ref<FilterVideo[]>([])

const filters = ref<Record<string, Filter>>({})

async function get_filters() {
    await electron_renderer_invoke('get_filters', {}).then((arg: any) => {
        filters.value = arg.filters
        for (const filter in filters.value) {
            all_videos.value.push({ name: filter, input_src: filters.value[filter].input_src })
        }
    })
}

async function get_stream_sources() {
    await electron_renderer_invoke('get_stream_sources', {}).then((arg: any) => {
        const stream_sources = arg.stream_sources as StreamSource
        for (const stream_source in stream_sources) {
            all_videos.value.push({ name: stream_source, input_src:  stream_sources[stream_source].source_name })
        }
    })
}

function get_stream_link(source_name: string) {
    return `http://127.0.0.1:8889/${source_name}/whep`
}


async function assert_stream_to_video(stream_link: string, video_component: HTMLMediaElement | undefined | null) {
    const video = video_component
    if (!video) return
    const pc = new RTCPeerConnection()
    pc.ontrack = (event) => {
        video.srcObject = event.streams[0]
    }
    const offer = await pc.createOffer({
        offerToReceiveAudio: true,
        offerToReceiveVideo: true
    })
    await pc.setLocalDescription(offer)
    const response = await fetch(stream_link, {
        method: 'POST',
        headers: { 'Content-Type': 'application/sdp' },
        body: offer.sdp
    })
    const answerSdp = await response.text()
    await pc.setRemoteDescription({
        type: 'answer',
        sdp: answerSdp
    })
}


function edit_main_stram(stream_name: string,stream_source: string) {
    main_video.value.input_src = stream_source
    main_video.value.name = stream_name

    assert_stream_to_video(main_video.value?.input_src, main_video.value?.video)
}



onMounted(async () => {
    await get_filters()
    await get_stream_sources()
    console.log(all_videos.value)

    if (all_videos.value.length == 0)
        return

    main_video.value.input_src = all_videos.value[0].input_src
    main_video.value.name = all_videos.value[0].name

    const stram_url = get_stream_link(main_stream_path.value)
    assert_stream_to_video(stram_url, main_video.value)
    await nextTick()

    streams_paths.value.forEach((path, i) => {
        const video = vid_arr.value[i]
        const stram_url = get_stream_link(path)
        assert_stream_to_video(stram_url, video)
    })
})



</script>


<template>

    <div id="view_videos_container">
        <div id="view_videos_main_video">
            <h2 style="margin: 0;" v-if="main_stream_path">{{ main_stream_path }}</h2>
            <video ref="main_video" controls autoplay>
                <source type="application/x-mpegURL">
            </video>
        </div>
        <div id="view_videos_secondery_videos_container">
            <div v-for="(stream, index) in streams_paths" class="view_video_secondery_video">
                <video :key="index" ref="vid_arr" controls autoplay>
                    <source type="application/x-mpegURL" />
                </video>
                <p class="view_video_secondery_video_title">{{ stream }}</p>
                <div class="btn_container">
                    <Button style="height: 32px; width: 80px;" outlined label="select" @click="edit_main_stram(stream)" />
                </div>

            </div>
        </div>
    </div>


</template>


<style scoped>
.view_video_secondery_video {
    width: 100%;
    margin-block: 8px;
    padding: 4px;
}

.view_video_secondery_video>* {
    width: 100%;
}

.view_video_secondery_video_title {
    font-weight: bold;
    margin: 0;
    padding: 0;
}

#view_videos_secondery_videos_container {
    width: 100%;
    max-height: 98%;
    overflow-y: scroll;
    padding: 8px;
}

#view_videos_secondery_videos_container::-webkit-scrollbar {
    display: none;
    /* For Chrome, Safari, and Opera */
}

#view_videos_main_video>* {
    width: 100%;
}

#view_videos_container {
    width: 100%;
    max-height: 100%;
    display: grid;
    grid-template-columns: 65% 25%;
    gap: 5%;
}
</style>