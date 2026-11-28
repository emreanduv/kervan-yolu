// Oyuna açılan köprü. KY_MAGAZA='steam': uygulama içi satın alma ve puan penceresi kapanır (Steam'de tam oyun 1,99 $).
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('KY_MAGAZA', 'steam');
contextBridge.exposeInMainWorld('KervanHost', {
  platform: 'steam',
  lang: ipcRenderer.sendSync('dil'),
  achieve: id => ipcRenderer.send('basarim', String(id)),
  quit: () => ipcRenderer.send('cik')
});
