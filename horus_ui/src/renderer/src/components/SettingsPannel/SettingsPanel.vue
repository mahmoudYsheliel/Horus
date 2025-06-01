<script lang="ts" setup>
import { ref } from 'vue';
import Button from 'primevue/button'
import { electron_renderer_invoke } from '@renderer/lib/utils';

enum LogLevel {
    DEBUG = 0,
    INFO = 1,
    WARNING = 2,
    ERROR = 3,
    CRITICAL = 4,
}
interface Log {
    timestamp: number
    log_level: LogLevel
    src: string
    msg: string
}
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
interface Filter {
    Log: string
    input_src: string
    output_src: string
    enable_recording: boolean
    filters_chain: Object[]
}

interface Agent {
    path: string
    agent: string
    input_src: string
    agent_params: string
}


const status = ref<Map<string, number>>(new Map())
const logs = ref<{ logs: Log[] }>({ logs: [] })
const stream_sources = ref<Record<string, StreamSource>>({})
const filters = ref<Record<string, Filter>>({})
const agents = ref<Record<string, Agent>>({})

async function get_status() {
    await electron_renderer_invoke('get_monitor_status', {}).then((arg: any) => {
        status.value = arg as Map<string, number>
    })
}
async function get_logs() {
    await electron_renderer_invoke('get_monitor_logs', {}).then((arg: any) => {
        logs.value = arg
    })
}
async function get_stream_sources() {
    await electron_renderer_invoke('get_stream_sources', {}).then((arg: any) => {
        stream_sources.value = arg.stream_sources
    })
}


async function get_filters() {
    await electron_renderer_invoke('get_filters', {}).then((arg: any) => {
        filters.value = arg.filters
    })
}
async function get_agents() {
    await electron_renderer_invoke('get_agents', {}).then((arg: any) => {
        agents.value = arg.agents
    })
}
</script>

<template>
    <div class="get-groups">
        <div class="get-group">
            <Button @click="get_status" label="Get Status" />
            <pre>{{ status }}  </pre>
        </div>
        <div class="get-group">
            <Button @click="get_logs" label="Get Logs" />
            <pre>{{ logs }}  </pre>
        </div>
        <div class="get-group">
            <Button @click="get_filters" label="Get Filters" />
            <pre>{{ filters }}  </pre>
        </div>
        <div class="get-group">
            <Button @click="get_stream_sources" label="Get Stream Sources" />
            <pre>{{ stream_sources }}  </pre>
        </div>
        <div class="get-group">
            <Button @click="get_agents" label="Get Agents" />
            <pre>{{ agents }}  </pre>
        </div>
    </div>

</template>


<style scoped>
.get-group {
    display: grid;
    grid-template-columns: 180px auto;
    gap: 16px;
    align-items: start;
    margin-bottom: 16px;
}

.get-groups {
    max-height: 100%;
    width: 100%;
    overflow: scroll;
}

.get-groups::-webkit-scrollbar {
    display: none;
}

#add_camera_config {
    background-color: var(--accent-color);
    border: none;
    border-radius: 100%;
    width: 48px;
    height: 48px;
    position: absolute;
    bottom: 40px;
    right: 40px;
}
</style>