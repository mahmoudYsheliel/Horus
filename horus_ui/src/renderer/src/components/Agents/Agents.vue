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


interface VideoStream {
    name?: string
    inp_src?: string
}


const main_stream = ref<VideoStream>()
const main_canvas_element = ref<HTMLCanvasElement>();
const main_detection_data = ref<DetectionData[]>([])

const all_streams = ref<VideoStream[]>([])
const all_canvas_elements = ref<HTMLCanvasElement[]>([])


const agents = ref<Record<string, Agent>>({})

async function get_agents() {
    await electron_renderer_invoke('get_agents', {}).then((arg: any) => {
        agents.value = arg.agents
    })
}
function get_stream_link(source: string) {
    return `http://127.0.0.1:8889/${source}/whep`
}
function get_stream_source(url: string) {
    return url.split('8554/')[1]
}



async function assert_stream_to_canvas(stream_link: string | undefined, canvas: HTMLCanvasElement | undefined | null, detection_data: Ref<DetectionData[]> | null, wait_time: number = 1) {
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

function edit_main_agent(stream: VideoStream) {
    main_stream.value = stream
    assert_stream_to_canvas(main_stream.value?.inp_src, main_canvas_element.value, main_detection_data)
}

onMounted(async () => {
    window.electron.ipcRenderer.on('ai_agent', (_, data) => {
        if (data.channel == main_stream.value?.name) {
            main_detection_data.value = []
            for (const detail of data.data.details) {
                main_detection_data.value?.push(detail)
            }
        }
    })

    await get_agents()

    for (let [name, stream_val] of Object.entries(agents.value)) {
        const source = get_stream_source(stream_val.input_src)
        const stream_link = get_stream_link(source)
        all_streams.value.push({ name: name, inp_src: stream_link })
    }
    edit_main_agent(all_streams.value[0])


    await nextTick()

    all_streams.value.forEach((stream, i) => {
        const video = all_canvas_elements.value[i]
        assert_stream_to_canvas(stream.inp_src, video, null)
    })

})
</script>


<template>
    <div id="view_agents_container">
        <div id="view_agents_main_agent">
            <h2 style="margin: 0;" v-if="main_stream">{{ main_stream.name }}</h2>
            <canvas ref="main_canvas_element"></canvas>
        </div>
        <div id="view_agents_secondery_agents_container">
            <div v-for="(stream, index) in all_streams" class="view_agents_secondery_agents">
                <canvas ref="all_canvas_elements" :key="index"></canvas>
                <p class="view_agents_secondery_agent_title">{{ stream.name }}</p>
                <div class="btn_container">
                    <Button style="height: 32px; width: 80px;" outlined label="select" @click="edit_main_agent(stream)" />
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
