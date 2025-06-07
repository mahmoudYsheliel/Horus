<!-- This code made to implement canvas not video to support object track -->



<script setup lang="ts">
import { electron_renderer_invoke, electron_renderer_send } from '@renderer/lib/utils';
import { ref, onMounted, nextTick, Ref } from 'vue'
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

// interface Agent {
//     path: string
//     agent: string
//     input_src: string
//     agent_params: string
// }


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


class StreamCanvas {
    public static instances: Ref<StreamCanvas[]> = ref([]);
    public static main_stream = ref<StreamCanvas>(new StreamCanvas('', ''))
    public static last_id = 0

    private pc: RTCPeerConnection | null = null;
    private reader: ReadableStreamDefaultReader<any> | null = null;
    private controller = new AbortController();
    private is_active = true;
    public is_drawing = false;
    private stopped_frame: ImageData | null = null;
    private is_previewing = false;
    private startX = 0;
    private startY = 0;
    private endX = 0;
    private endY = 0;
    public detection_data: Record<string, DetectionData[]> = {};
    private canvas: HTMLCanvasElement | null = null;
    private ctx: CanvasRenderingContext2D | null = null;
    public detection_channels: string[] = []

    constructor(
        public name: string,
        public input_src: string,
        private wait_time = 50,
    ) { }

    public assign_as_main_stream() {
        StreamCanvas.main_stream.value.name = this.name
        StreamCanvas.main_stream.value.input_src = this.input_src
        StreamCanvas.main_stream.value.detection_channels = this.detection_channels
        StreamCanvas.main_stream.value.detection_data = {}
        StreamCanvas.main_stream.value.start()
    }
    public assign_canvas(canvas: HTMLCanvasElement) {
        this.canvas = canvas
        this.ctx = this.canvas.getContext('2d')
    }

    public async start() {
        if (!this.ctx || !this.input_src) return;

        this.pc = new RTCPeerConnection();

        let track: MediaStreamTrack | null = null;
        this.pc.ontrack = (event) => {
            track = event.track;
        };

        const offer = await this.pc.createOffer({
            offerToReceiveAudio: true,
            offerToReceiveVideo: true
        });

        await this.pc.setLocalDescription(offer);

        const response = await fetch(this.input_src, {
            method: 'POST',
            headers: { 'Content-Type': 'application/sdp' },
            body: offer.sdp
        });

        const answerSdp = await response.text();
        await this.pc.setRemoteDescription({
            type: 'answer',
            sdp: answerSdp
        });

        // Wait for track
        while (!track && this.is_active) {
            await new Promise(r => setTimeout(r, 50));
        }
        if (!track || !this.is_active) return;

        const processor = new (window as any).MediaStreamTrackProcessor({ track });
        this.reader = processor.readable.getReader();

        this.drawLoop();
    }

    private async drawLoop() {
        if (!this.reader || !this.is_active || !this.ctx || !this.canvas) return;

        const result = await this.reader.read();
        if (result.done || !this.is_active) {
            this.stop();
            return;
        }

        const frame: VideoFrame = result.value;
        this.canvas.width = frame.displayWidth;
        this.canvas.height = frame.displayHeight;
        if (this.is_drawing && this.stopped_frame) {
            this.ctx.putImageData(this.stopped_frame, 0, 0)
        }
        else {
            this.ctx.drawImage(frame, 0, 0);
        }

        frame.close();
        this.draw_traking_rec()

        for (const dd_key in this.detection_data) {
            const dd_arr = this.detection_data[dd_key]
            for (const dd of dd_arr) {
                const bb = dd.bounding_box;
                this.ctx.strokeStyle = 'red';
                this.ctx.lineWidth = 2;
                this.ctx.strokeRect(bb.x, bb.y, bb.w, bb.h);

                this.ctx.font = '14px Arial';
                this.ctx.fillStyle = 'black';
                const confidence = `Confidence: ${(dd.confidence * 100).toFixed(2)}`;
                this.ctx.fillText(dd.class_name, bb.x, bb.y);
                this.ctx.fillText(confidence, bb.x, bb.y + 20);
            }
        }

        setTimeout(() => requestAnimationFrame(() => this.drawLoop()), this.wait_time);
    }

    public stop() {
        this.is_active = false;
        this.controller.abort();
        if (this.reader) this.reader.cancel();
        if (this.pc) this.pc.close();
    }


    public toggle_drawing() {
        this.is_drawing = !this.is_drawing


        if (this.is_drawing) {
            if (!this.ctx || !this.canvas) return
            this.stopped_frame = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height)
            console.log(this.stopped_frame)
            this.canvas.addEventListener('mousedown', this.handle_mouse_down)
            this.canvas.addEventListener('mousemove', this.handle_mouse_move)
            this.canvas.addEventListener('mouseup', this.handle_mouse_up)
        }
    }

    private handle_mouse_down = (e: any) => {
        if (!this.is_drawing || !this.canvas) return
        const rect = this.canvas.getBoundingClientRect()
        this.startX = ((e.clientX - rect.left) / rect.width) * this.canvas.width
        this.startY = ((e.clientY - rect.top) / rect.height) * this.canvas.height
        this.endX = this.startX
        this.endY = this.startY

        this.is_previewing = true

    }



    private handle_mouse_move = (e: any) => {
        if (!this.is_previewing || !this.is_drawing || !this.canvas) return

        const rect = this.canvas.getBoundingClientRect()
        this.endX = ((e.clientX - rect.left) / rect.width) * this.canvas.width
        this.endY = ((e.clientY - rect.top) / rect.height) * this.canvas.height
    }


    private handle_mouse_up = (e: any) => {
        if (!this.is_previewing || !this.is_drawing || !this.canvas) return

        const rect = this.canvas.getBoundingClientRect()
        this.endX = ((e.clientX - rect.left) / rect.width) * this.canvas.width
        this.endY = ((e.clientY - rect.top) / rect.height) * this.canvas.height
        this.is_previewing = false

        // this.send_tracking_data()
        if (this.stopped_frame) {
            StreamCanvas.all_track_one(
                this.stopped_frame,
                this.startX,
                this.startY,
                this.endX,
                this.endY)
        }

    }


    private send_tracking_data() {
        const w = this.stopped_frame?.width
        const h = this.stopped_frame?.height
        const d = this.stopped_frame?.data
        const data = {
            image_width: w,
            image_height: h,
            image_data: d,
            object_x: Math.round(Math.min(this.startX, this.endX)),
            object_y: Math.round(Math.min(this.startY, this.endY)),
            object_w: Math.round(Math.abs(this.endX - this.startX)),
            object_h: Math.round(Math.abs(this.endY - this.startY)),
            track_name: `object_track_${this.name}_${StreamCanvas.last_id}`,
            stream_src: this.name,
        }
        electron_renderer_send('send_track_data', { data })
        this.detection_channels.push(`object_track_${this.name}_${StreamCanvas.last_id}`)
    }
    static all_track_one(stopped_frame: ImageData, startX: number, startY: number, endX: number, endY: number) {
        for (const stream_canvas of StreamCanvas.instances.value) {
            stream_canvas.stopped_frame = stopped_frame
            stream_canvas.startX = startX
            stream_canvas.startY = startY
            stream_canvas.endX = endX
            stream_canvas.endY = endY
            stream_canvas.send_tracking_data()
        }
        StreamCanvas.last_id += 1
    }

    private draw_traking_rec() {

        // Finalize rectangle
        if (!this.ctx) return

        if (this.is_drawing && !this.is_previewing) {
            this.ctx.setLineDash([])
            this.ctx.strokeStyle = 'blue'
            this.ctx.lineWidth = 2
            this.ctx.strokeRect(
                this.startX,
                this.startY,
                this.endX - this.startX,
                this.endY - this.startY
            )
        }



        if (this.is_drawing && this.is_previewing) {
            // Draw preview
            this.ctx.strokeStyle = 'red'
            this.ctx.lineWidth = 2
            this.ctx.setLineDash([6])
            this.ctx.strokeRect(
                this.startX,
                this.startY,
                this.endX - this.startX,
                this.endY - this.startY
            )
        }
    }

}

const all_streams_ref = ref<HTMLCanvasElement[]>([])
const main_canvas_ref = ref<HTMLCanvasElement | null>(null)

async function get_filters() {
    await electron_renderer_invoke('get_filters', {}).then((arg: any) => {
        const filters = arg.filters as Record<string, Filter>
        for (const filter in filters) {
            const path = filters[filter].camera_name + '/' + filter
            const tem = new StreamCanvas(path, get_stream_link(path), 1000)
            StreamCanvas.instances.value.push(tem)
        }
    })
}

async function get_stream_sources() {
    await electron_renderer_invoke('get_stream_sources', {}).then((arg: any) => {
        const stream_sources = arg.stream_sources as Record<string, StreamSource>
        for (const stream_source in stream_sources) {
            const tem = new StreamCanvas(stream_sources[stream_source].source_name, get_stream_link(stream_sources[stream_source].source_name), 1000)
            StreamCanvas.instances.value.push(tem)
        }
    })
}



function get_stream_link(source: string) {
    return `http://127.0.0.1:8889/${source}/whep`
}



onMounted(async () => {

    // change to detection agent

    window.electron.ipcRenderer.on('ai_agent', (_, data) => {
        const channel = data.channel as string
        if (StreamCanvas.main_stream.value && StreamCanvas.main_stream.value.detection_channels.includes(channel)) {
            StreamCanvas.main_stream.value.detection_data[channel] = []
            for (const detail of data.data.details) {
                StreamCanvas.main_stream.value.detection_data[channel].push(detail)
            }
        }
    })




    await get_filters()
    await get_stream_sources()
    StreamCanvas.instances.value[0].assign_as_main_stream()

    await nextTick()
    if (main_canvas_ref.value) {
        StreamCanvas.main_stream.value.assign_canvas(main_canvas_ref.value)
        StreamCanvas.main_stream.value.start()
    }

    StreamCanvas.instances.value.forEach((stream_canvas, i) => {
        stream_canvas.assign_canvas(all_streams_ref.value[i])
        stream_canvas.start()
    })
})



function draw_button_label(is_drawing: boolean) {
    return is_drawing ? 'Confirm' : 'Select Region'
}




</script>


<template>
    <div id="view_agents_container">
        <div id="view_agents_main_agent" v-if="StreamCanvas.main_stream.value">
            <h2 style="margin: 0;">{{ StreamCanvas.main_stream.value?.name }}</h2>
            <canvas ref="main_canvas_ref"></canvas>
            <Button :label="draw_button_label(StreamCanvas.main_stream.value.is_drawing)" @click="() => { if (StreamCanvas.main_stream.value) StreamCanvas.main_stream.value.toggle_drawing() }" />
        </div>
        <div id="view_agents_secondery_agents_container">
            <div v-for="(stream_canvas) in StreamCanvas.instances.value" class="view_agents_secondery_agents">
                <canvas ref="all_streams_ref"></canvas>
                <p class="view_agents_secondery_agent_title">{{ stream_canvas.name }}</p>
                <div class="btn_container">
                    <Button style="height: 32px; width: 80px;" outlined label="select" @click="stream_canvas.assign_as_main_stream()" />
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










<!-- This code was designed to support video element to show streams -->

<!-- <script setup lang="ts">
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


interface VideoStream {
    name?: string
    input_src?: string
}

const main_video_element = ref<HTMLMediaElement>()
const all_video_elements = ref<HTMLMediaElement[]>()

const main_stream = ref<VideoStream>({})
const all_streams = ref<VideoStream[]>([])


async function get_filters() {
    await electron_renderer_invoke('get_filters', {}).then((arg: any) => {
        const filters  = arg.filters as Record<string, Filter>
        for (const filter in filters) {
            const path = filters[filter].camera_name + '/' + filter
            all_streams.value.push({ name: filter, input_src: get_stream_link(path) })
        }
    })
}

async function get_stream_sources() {
    await electron_renderer_invoke('get_stream_sources', {}).then((arg: any) => {
        const stream_sources = arg.stream_sources as Record<string, StreamSource>
        for (const stream_source in stream_sources) {
            all_streams.value.push({ name: stream_sources[stream_source].source_name, input_src: get_stream_link(stream_sources[stream_source].source_name) })
        }
    })
}

function get_stream_link(source_name: string) {
    return `http://127.0.0.1:8889/${source_name}/whep`
}


async function assert_stream_to_video(stream_link: string | undefined, video_component: HTMLMediaElement | undefined | null) {
    if (!stream_link)
        return
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


function edit_main_stram(video_stream: VideoStream) {
    main_stream.value = video_stream
    assert_stream_to_video(main_stream.value?.input_src, main_video_element.value)
}



onMounted(async () => {
    await get_filters()
    await get_stream_sources()
    if (all_streams.value.length == 0)
        return

    main_stream.value = all_streams.value[0]
    // main_video.value.video = main_video_element.value

    assert_stream_to_video(main_stream.value?.input_src, main_video_element.value)
    await nextTick()

    all_streams.value.forEach((video_object,i) => {
        const stram_url = video_object.input_src
        if (all_video_elements.value )
            assert_stream_to_video(stram_url, all_video_elements.value[i])
    })
})



</script>


<template>

    <div id="view_videos_container">
        <div id="view_videos_main_video">
            <h2 style="margin: 0;" v-if="main_stream.name">{{ main_stream.name }}</h2>
            <video ref="main_video_element" controls autoplay>
                <source type="application/x-mpegURL">
            </video>
        </div>
        <div id="view_videos_secondery_videos_container">
            <div v-for="(video_object, index) in all_streams" class="view_video_secondery_video">
                <video :key="index" ref="all_video_elements" controls autoplay>
                    <source type="application/x-mpegURL" />
                </video>
                <p class="view_video_secondery_video_title">{{ video_object.name }}</p>
                <div class="btn_container">
                    <Button style="height: 32px; width: 80px;" outlined label="select" @click="edit_main_stram(video_object)" />
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
 -->
