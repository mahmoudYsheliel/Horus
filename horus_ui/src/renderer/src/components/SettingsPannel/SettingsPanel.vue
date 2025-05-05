<script lang="ts" setup>
import { CameraConfig, ConnectionParam, FilterConfig } from '@common/models';
import Button from 'primevue/button';
import { compute_tooltip_pt } from '@renderer/lib/utils';
import { reactive, ref } from 'vue';

const cameras_cofiguration: CameraConfig[] = reactive([])


function add_camera_config() {
    cameras_cofiguration.push({
        source_id: '',
        soource_type: 'RTSP',
        source_name: '',
        enable_recording: false,
        connection_params: {
            address: '192.168.1.2:8080',
            username: 'admin',
            password: '5555',
            channel: '/h264_ulaw.sdp',
        }
    })
}

</script>

<template>
    <div id="settings_panel_con">
        <div id="cameras_config_con">
        {{ cameras_cofiguration }}
            <div class="comara_config" v-for="cam_conf in cameras_cofiguration">

            </div>
        </div>

        <Button @click="add_camera_config" icon="pi pi-plus" id="add_camera_config" v-tooltip="{ value: 'Add Camera Confuguration', pt: compute_tooltip_pt('left') }" />
    </div>

</template>


<style scoped>
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

#settings_panel_con {}
</style>