<script setup lang="ts">
import { onBeforeMount, ref, onMounted } from 'vue';
import TopBar from '@renderer/components/TopBar/TopBar.vue';
import NavBar from '@renderer/components/NavBar/NavBar.vue';
import SettingsPanel from './components/SettingsPannel/SettingsPanel.vue';

import { subscribe } from '@common/mediator';
import { PanelName } from '@common/models';
import Agents from './components/Agents/Agents.vue';

import ShowScreens from './components/ShowScreens/ShowScreens.vue';



const APP_THEME = {
    '--dark-bg-color': '#0B0E1F',
    '--light-bg-color': '#111D2D',
    '--light-bg-shadow-color': '#1A2636',
    '--font-color': '#8BA2CC',
    '--accent-color': '#29B2F8',
    '--empty-gauge-color': '#2D3A4B',
};


const selected_panel_name = ref<PanelName>('none')


function load_theme(theme: Record<string, string>) {
    for (const theme_var in theme)
        document.documentElement.style.setProperty(theme_var, theme[theme_var]);
}

onBeforeMount(() => {
    load_theme(APP_THEME);
});







onMounted(async () => {
    subscribe('show_panel', 'app_show_panel', (args) => {
        const { panel_name } = args
        if (selected_panel_name.value !== panel_name)
            selected_panel_name.value = panel_name
        else
            selected_panel_name.value = 'none'
    })



})



</script>

<template>
    <div id="app_shell">
        <TopBar />
        <div id="main_panel">
            <NavBar />

            <div id="selected_panel_con">
                <SettingsPanel v-show="selected_panel_name == 'settings'" />
                <ShowScreens  v-show="selected_panel_name == 'monitor'" />
                <Agents  v-show="selected_panel_name == 'agent'" />
            </div>

            

          
        </div>
    </div>
</template>

<style lang="css">
#selected_panel_con{
    padding: 24px;
    height: 100%;
    width: 100%;
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