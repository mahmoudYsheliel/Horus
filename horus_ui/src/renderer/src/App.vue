<script setup lang="ts">

import { onBeforeMount, ref, onMounted } from 'vue';

import TopBar from '@renderer/components/TopBar/TopBar.vue';
import NavBar from '@renderer/components/NavBar/NavBar.vue';
import SettingsPanel from './components/SettingsPannel/SettingsPanel.vue';
import Button from 'primevue/button'
import Textarea from 'primevue/textarea';
import { electron_renderer_invoke } from './lib/utils';
import { post_event, subscribe } from '@common/mediator';
import { PanelName } from '@common/models';

const status = ref<any>()
const logs = ref<any>()
const selected_panel_name = ref<PanelName>('none')

function get_status() {
    electron_renderer_invoke('get_monitor_status', {}).then((arg: any) => {
        status.value = arg.monitor_service
        console.log(arg)
    })
}

function get_logs() {
    electron_renderer_invoke('get_monitor_logs', {}).then((arg: any) => {
        logs.value = arg
        console.log(arg)
    })
}


const APP_THEME = {
    '--dark-bg-color': '#0B0E1F',
    '--light-bg-color': '#111D2D',
    '--light-bg-shadow-color': '#1A2636',
    '--font-color': '#8BA2CC',
    '--accent-color': '#29B2F8',
    '--empty-gauge-color': '#2D3A4B',
};
function load_theme(theme: Record<string, string>) {
    for (const theme_var in theme)
        document.documentElement.style.setProperty(theme_var, theme[theme_var]);
}

onBeforeMount(() => {
    load_theme(APP_THEME);
});

onMounted(() => {
    subscribe('show_panel', 'app_show_panel', (args) => {
        const { panel_name } = args
        if (selected_panel_name.value !== panel_name)
            selected_panel_name.value = panel_name
        else
            selected_panel_name.value = 'none'
    })
})

import Hls from 'hls.js';



// Create a ref for the video element
const video = ref<HTMLMediaElement>();

// Set up HLS on mounted
onMounted(() => {
    if (video.value) {
        const videoElement = video.value;
        if (Hls.isSupported()) {
            const hls = new Hls();
            hls.loadSource('http://127.0.0.1:8888/android-wifi/index.m3u8');
            hls.attachMedia(videoElement);
        } else if (videoElement.canPlayType('application/vnd.apple.mpegurl')) {
            videoElement.src = 'http://127.0.0.1:8888/android-wifi/index.m3u8';
        }
    }
});

</script>

<template>
    <div id="app_shell">
        <TopBar />
        <div id="main_panel">
            <NavBar />
            <div id="selected_panel_con">
                <SettingsPanel v-if="selected_panel_name == 'settings'" />
            </div>

            <video ref="video" controls autoplay>
                <source type="application/x-mpegURL">
            </video>




            <!-- <div class="get-groups">
                <div class="get-group">
                    <Button @click="get_status" label="Get Status" />
                    <Textarea v-model="status" />
                </div>
                <div class="get-group">
                    <Button @click="get_logs" label="Get Logs" />
                    <Textarea v-model="logs" />
                </div>
            </div> -->


        </div>
    </div>
</template>

<style lang="css">
.get-group {
    display: flex;
    justify-content: space-between;
    width: 40%;
}

.get-groups {
    display: flex;
    width: 100%;
    justify-content: space-between;
}


#main_panel {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: flex-start;
    flex-grow: 1;
    width: 100%;
    height: 92vh;
}

#app_shell {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    height: 100%;
}

body,
html {
    width: 100%;
    height: 100%;
    margin: 0;
    background-color: var(--dark-bg-color);
}

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    font-family: "Cairo", sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: var(--font-color);
    width: 100%;
    height: 100%;
}

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
    background-color: var(--empty-gauge-color);
}

::-webkit-scrollbar-thumb {
    background: var(--font-color);
    border-radius: 8px;
}

::-webkit-scrollbar-corner {
    background-color: var(--empty-gauge-color);
}

::placeholder {
    color: var(--empty-gauge-color);
}
</style>