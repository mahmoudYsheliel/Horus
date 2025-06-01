<script setup lang="ts">

import { ref, Ref } from 'vue';
import Settings from '../icons/Settings.vue';
import Eye from '../icons/Eye.vue';
import Agent from '../icons/Agent.vue';
import { post_event } from '@common/mediator';
import { PanelName } from '@common/models';
import NavBarIcon from './NavBarIcon.vue';


class NavMenuItem {
    label: string;
    icon: any;
    panel_name: PanelName;
    is_active: Ref<boolean>;
    action: (event: MouseEvent) => void;

    constructor(_label: string, _icon: any, _action: (event: MouseEvent) => void, _panel_name: PanelName = 'none') {
        this.label = _label;
        this.icon = _icon;
        this.panel_name = _panel_name;
        this.is_active = ref(false);
        this.action = _action.bind(this);
    }
};


const menu_items: NavMenuItem[] = [
    new NavMenuItem('Configurations', Settings, function (this: NavMenuItem, _event: MouseEvent) { view_panel(this.panel_name) }, 'settings'),
    new NavMenuItem('Monitor', Eye, function (this: NavMenuItem, _event: MouseEvent) { view_panel(this.panel_name) }, 'monitor'),
    new NavMenuItem('Agent', Agent, function (this: NavMenuItem, _event: MouseEvent) { view_panel(this.panel_name) }, 'agent'),
]
function view_panel(panel_name: string) {
    post_event('show_panel', { panel_name })
    for (let menu_item of menu_items) {
        if (menu_item.panel_name == panel_name) 
            menu_item.is_active.value = !menu_item.is_active.value
        else
            menu_item.is_active.value = false
    }
}

</script>

<template>
    <div id="nav_bar_cont">
        <NavBarIcon v-for="m_item in menu_items" :menu_item="m_item" />
        <div style="flex-grow: 1;"></div>
        <div class="hero_icon">
            <svg viewBox="0 0 443 308" xmlns="http://www.w3.org/2000/svg">
                <path fill="var(--font-color)" d="M437.732 110.5L425.191 82C421.191 84.5 387.691 85 383.191 84C363.691 84 270.191 45 225.191 45C185.191 45 37.6914 92 17.1914 92V121.5C44.7914 121.5 156.191 167.5 206.191 167.5C285.5 167.5 285.5 167.5 215.191 221C155.591 265.4 101.691 275.167 82.1914 274.5C44.1914 274.5 29.6914 253.167 27.1914 242.5C20.3914 212.1 39.3581 202.833 49.6914 202C44.4914 222.612 60.1914 225.255 68.6914 224C87.4914 217.6 84.5247 200.667 80.6914 193C69.0914 172.2 44.1914 174.333 33.1914 178C24.0247 180.167 4.69128 191.4 0.691278 219C-3.30872 246.6 11.0246 268.833 18.6913 276.5C39.8913 301.7 88.1913 299 109.691 294.5C163.691 288.9 239.191 230.833 270.191 202.5C320.191 147 331.691 138 310.69 221C306.642 237 299.19 272.5 300.19 303.5C323.69 303.5 341.19 222.556 351.232 213.5C371.19 195.5 390.69 210.5 351.232 188C332.19 150 379.19 111.5 437.732 110.5Z" />
                <path fill="var(--light-bg-color)" d="M193.192 78C185.992 78 107.853 96.6686 69.8525 106.502C177.853 143.501 191.691 139.002 224.191 139.002C260.691 139.002 313.692 137.499 355.192 108C330.692 99 282.5 76.5 259 76.5C262.333 89.8333 260.492 118 225.691 118C190.891 118 189.525 91.3333 193.192 78Z" />
                <path fill="var(--font-color)" d="M17 78.5V42H38.5C73.5 42 145.5 0 220.5 0C274 3.14794e-08 365 39.501 396 39.501C410.8 39.901 418.5 36.6676 420.5 35.001L434.5 56.5C432.5 59.6667 425.3 66 412.5 66C340.5 66 303 31 219.5 31C153.5 31 78.5 68 46.5 72L17 78.5Z" />
            </svg>
        </div>
        <div style="height: 8px;"></div>
    </div>
</template>

<style lang="css" scoped>
.hero_icon {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: 40px;
    padding: 4px;
    border-radius: 4px;
    border: 1px solid var(--font-color);
    background-color: var(--light-bg-color);
}

#nav_bar_cont {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    background-color: var(--light-bg-color);
    border: 1px solid var(--empty-gauge-color);
    height: calc(100% - 24px);
    width: 60px;
    margin: 12px 8px;
    border-radius: 4px;
}
</style>