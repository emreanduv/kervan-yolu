// Kervan Yolu masaüstü (Steam) kabuğu. Oyunun kendisi www/ içindeki web oyunudur.
// Kayıt: oyun localStorage kullanır; Electron bunu userData/Local Storage altında tutar (Steam Auto-Cloud bu klasörü eşitler).
const { app, powerSaveBlocker, BrowserWindow, ipcMain, Menu, screen, shell } = require('electron');
const path = require('path'), fs = require('fs');

app.setName('KervanYolu');
if (process.platform === 'linux') app.commandLine.appendSwitch('no-sandbox');
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
app.commandLine.appendSwitch('ignore-gpu-blocklist');

let APP_ID = 0;
try { APP_ID = JSON.parse(fs.readFileSync(path.join(__dirname, 'steam.json'), 'utf8')).appId || 0; } catch (e) {}
let steam = null;
if (APP_ID) {
  try {
    const sw = require('steamworks.js');
    if (sw.restartAppIfNecessary(APP_ID)) { app.exit(0); }
    steam = sw.init(APP_ID);
    sw.electronEnableSteamOverlay();
  } catch (e) { console.log('Steam bağlantısı yok:', e.message); steam = null; }
}

let win = null;
function createWindow() {
  const wa = screen.getPrimaryDisplay().workAreaSize;
  win = new BrowserWindow({
    width: Math.min(1440, wa.width), height: Math.min(900, wa.height), minWidth: 800, minHeight: 540,
    backgroundColor: '#0b1622', title: 'Kervan Yolu', show: false, autoHideMenuBar: true,
    icon: path.join(__dirname, 'build', 'icon.png'),
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, nodeIntegration: false, backgroundThrottling: false, spellcheck: false }
  });
  Menu.setApplicationMenu(null);
  win.loadFile(path.join(__dirname, 'www', 'index.html'));
  win.once('ready-to-show', () => win.show());
  win.webContents.setWindowOpenHandler(({ url }) => { if (/^(https?|mailto):/.test(url)) shell.openExternal(url); return { action: 'deny' }; });
  win.webContents.on('will-navigate', (e, url) => { if (!url.startsWith('file:')) { e.preventDefault(); shell.openExternal(url); } });
  win.webContents.on('before-input-event', (e, input) => {
    if (input.type !== 'keyDown') return;
    if (input.key === 'F11') { win.setFullScreen(!win.isFullScreen()); e.preventDefault(); }
    if (input.key === 'F12' && !app.isPackaged) win.webContents.toggleDevTools();
  });
}

ipcMain.on('basarim', (e, id) => { if (steam) try { if (!steam.achievement.isActivated(id)) steam.achievement.activate(id); } catch (x) {} });
ipcMain.on('dil', e => { let l = ''; if (steam) try { l = steam.apps.currentGameLanguage(); } catch (x) {} e.returnValue = l; });
ipcMain.on('cik', () => app.quit());

app.whenReady().then(() => { createWindow(); try { powerSaveBlocker.start('prevent-display-sleep'); } catch (e) {} });
app.on('window-all-closed', () => app.quit());
