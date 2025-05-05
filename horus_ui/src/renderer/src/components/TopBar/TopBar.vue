<script setup lang="ts">

import UserInfoTag from './UserInfoTag.vue';
import CloudStatusTag from './CloudStatusTag.vue';

</script>

<template>
    <div id="top_bar_cont">
        <div id="version_tag">
            <span>Horus AI</span>
        </div>
        <div id="tags_cont">
            <div class="tags_sec">
                <div style="width: 24px;"></div>
                <UserInfoTag :icon_size="'24px'" />
                <div style="width: 16px;"></div>
                <CloudStatusTag :icon_size="'24px'" />
            </div>
            <div style="flex-grow: 1;"></div>
            <div class="tags_sec">
                <img style="user-select: none;" id="psytronic_logo" src="/images/logo.png" alt="PsyTronic">
            </div>
        </div>
    </div>
</template>

<style scoped>
.right_sec_icon {
    font-size: 24px;
    color: var(--font-color);
    margin-right: 8px;
    cursor: pointer;
    transition: 0.3s ease;
}

.right_sec_icon:hover {
    color: var(--accent-color);
}

#psytronic_logo {
    height: 40px;
    margin-right: 16px;
}

#tags_cont {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    flex-grow: 1;
}

.tags_sec {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
}

#version_tag {
    width: 16vw;
    height: 100%;
    color: white;
    font-weight: bold;
    background-color: var(--accent-color);
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    clip-path: polygon(0 0, 90% 0, 100% 100%, 0% 100%);
}

#top_bar_cont {
    width: 100%;
    height: 8vh;
    max-height: 60px;
    border-bottom: 4px solid var(--accent-color);
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
}
</style>