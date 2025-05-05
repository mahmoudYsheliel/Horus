import { app, shell, BrowserWindow } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import { init_test_zmq } from './testzmq'

const BASE_HRES = 1280;
const BASE_VRES = 720;
function createWindow(): void {
    const mainWindow = new BrowserWindow({
        width: process.platform !== 'win32' ? BASE_HRES : BASE_HRES + 16,
        height: process.platform !== 'win32' ? BASE_VRES : BASE_VRES + 32,
        show: false,
        resizable: true,
        frame: false,
        autoHideMenuBar: true,
        // fullscreen: true,
        ...(process.platform === 'linux' ? { icon } : {}),
        webPreferences: {
            preload: join(__dirname, '../preload/index.js'),
            sandbox: false,
            contextIsolation: true,
            nodeIntegration: false,
            webSecurity: false, 
        }
    })

    mainWindow.on('ready-to-show', () => {
        mainWindow.show()
    })

    mainWindow.webContents.setWindowOpenHandler((details) => {
        shell.openExternal(details.url)
        return { action: 'deny' }
    })

    if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
        mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
    } else {
        mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
    }

    init_test_zmq(mainWindow)
}

app.whenReady().then(() => {
    electronApp.setAppUserModelId('labtronic-control-hub-v2.aAbstract')
    app.on('browser-window-created', (_, window) => {
        optimizer.watchWindowShortcuts(window)
    })
    createWindow()
    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })

    app.commandLine.appendSwitch('disable-site-isolation-trials');
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})