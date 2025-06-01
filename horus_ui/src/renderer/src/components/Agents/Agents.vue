<script setup lang="ts">
import { electron_renderer_invoke } from '@renderer/lib/utils';
import { ref, Ref, onMounted, nextTick } from 'vue'
import Button from 'primevue/button';

interface BoundingBox {
    x: number,
    y: number,
    w: number,
    h: number
}
interface DetectionData {
    class_name: string,
    bounding_box: BoundingBox,
    confidence: number,
}

interface Agent {
    path: string
    agent: string
    input_src: string
    agent_params: string
}


const main_stream_source = ref('http://127.0.0.1:8889/android-wifi/whep')
const main_video = ref<HTMLCanvasElement>();
const main_detection_data = ref<DetectionData[]>([])
const main_agent = ref<string>()


const secondery_streams = ref<string[]>([])
const vid_arr = ref<HTMLCanvasElement[]>([])
const secondery_detection_data = ref<DetectionData[][]>([])


const agents = ref<Record<string, Agent>>({})

async function get_agents() {
    await electron_renderer_invoke('get_agents', {}).then((arg: any) => {
        agents.value = arg.agents
        console.log('agents: ',agents.value)
    })
}
function get_stream_link(source: string) {
    return `http://127.0.0.1:8889/${source}/whep`
}
function get_stream_source(url: string) {
    console.log('src: ', url.split('8554/')[1])
    return url.split('8554/')[1]
}
function get_agent_name(url: string): string | null {
    const match = url.match(/^rtsp:\/\/127\.0\.0\.1:8889\/(.+?)\/whep$/)
    return match ? match[1].replaceAll('/', ' > ') : null
}



async function assert_stream_to_canvas(stream_link: string, canvas: HTMLCanvasElement | undefined | null, detection_data: Ref<DetectionData[]> | null, wait_time: number = 10) {
    if (!canvas || !stream_link) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const pc = new RTCPeerConnection()
    let track: MediaStreamTrack | null = null

    pc.ontrack = (event) => {
        track = event.track
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
    while (!track) await new Promise(r => setTimeout(r, 50))
    const processor = new (window as any).MediaStreamTrackProcessor({ track })
    const reader = processor.readable.getReader()

    const drawFrame = async () => {
        const result = await reader.read()
        if (result.done) return
        const frame: VideoFrame = result.value
        canvas.width = frame.displayWidth
        canvas.height = frame.displayHeight

        ctx.drawImage(frame, 0, 0)
        frame.close()

        ctx.strokeStyle = 'red'
        ctx.lineWidth = 2
        // console.log(detection_data?.value)
        if (detection_data) {
            for (const dd of detection_data.value) {
                const bb = dd.bounding_box
                ctx.strokeRect(bb.x, bb.y, bb.w, bb.h)

                ctx.font = '14px Arial';
                ctx.fillStyle = 'black';
                const confidence = `Conficence: ${(dd.confidence * 100).toFixed(2)}`
                // Draw text on canvas
                ctx.fillText(dd.class_name, bb.x, bb.y);
                ctx.fillText(confidence, bb.x, bb.y + 20);

            }
        }

        setTimeout(() => { requestAnimationFrame(drawFrame) }, wait_time)

    }
    drawFrame()
}

function edit_main_agent(stream: string) {
    main_agent.value = stream
    assert_stream_to_canvas(main_agent.value, main_video.value, main_detection_data)
}


onMounted(async () => {

    window.electron.ipcRenderer.on('ai_agent', (_, data) => {
        console.log(data)
        main_detection_data.value = []
        for (const detail of data.data.details) {
            main_detection_data.value?.push(detail)
        }
    })


    await get_agents()

    const [_, first_val] = Object.entries(agents.value)[0] ?? []
    const source = get_stream_source(first_val.input_src)
    main_agent.value = get_stream_link(source)


    for (let [_, stream_val] of Object.entries(agents.value)) {
        const source = get_stream_source(stream_val.input_src)
        const stream_link = get_stream_link(source)
        secondery_streams.value.push(stream_link)
    }

    assert_stream_to_canvas(main_stream_source.value, main_video.value, main_detection_data)
    await nextTick()

    secondery_streams.value.forEach((url, i) => {
        const video = vid_arr.value[i]
        assert_stream_to_canvas(url, video, null)
    })

    assert_stream_to_canvas(main_stream_source.value, main_video.value, main_detection_data)

})
</script>


<template>
    <div id="view_agents_container">
        <div id="view_agents_main_agent">
            <h2 style="margin: 0;" v-if="main_agent">{{ main_agent }}</h2>
            <canvas ref="main_video"></canvas>
        </div>
        <div id="view_agents_secondery_agents_container">
            <div v-for="(agent, index) in secondery_streams" class="view_agents_secondery_agents">
                <canvas ref="vid_arr" :key="index"></canvas>
                <p class="view_agents_secondery_agent_title">{{ agent }}</p>
                <div class="btn_container">
                    <Button style="height: 32px; width: 80px;" outlined label="select" @click="edit_main_agent(agent)" />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
canvas {
    display: block;
    max-width: 100%;
    border: 1px solid #ccc;
}

.view_agents_secondery_agent {
    width: 100%;
    margin-block: 8px;
    padding: 4px;
}

.view_agents_secondery_agent>* {
    width: 100%;
}

.view_agents_secondery_agent_title {
    font-weight: bold;
    margin: 0;
    padding: 0;
}

#view_agents_secondery_agents_container {
    width: 100%;
    max-height: 98%;
    overflow-y: scroll;
    padding: 8px;
}

#view_agents_secondery_agents_container::-webkit-scrollbar {
    display: none;
    /* For Chrome, Safari, and Opera */
}

#view_agents_main_agent>* {
    width: 100%;
}

#view_agents_container {
    width: 100%;
    max-height: 100%;
    display: grid;
    grid-template-columns: 65% 25%;
    gap: 5%;
}
</style>
