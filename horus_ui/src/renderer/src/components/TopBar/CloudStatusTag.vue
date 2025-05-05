<script setup lang="ts">

import SiteAlt from '@renderer/components/icons/SiteAlt.vue';

defineProps<{ icon_size: string }>();

</script>

<template>
    <div id="cloud_status_tag">
        <SiteAlt id="site_alt_icon" :fill_color="'#FFAB00'" />
        <span>OFFLINE</span>
    </div>
</template>

<style scoped>
#site_alt_icon {
    width: v-bind(icon_size);
    margin-right: 8px;
}

#cloud_status_tag {
    background-color: var(--light-bg-color);
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    padding: 4px 0px;
    width: 180px;
    border-radius: 4px;
    color: #FFAB00;
}

#cloud_status_tag span {
    font-weight: bold;
}
</style>