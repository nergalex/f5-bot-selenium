function receiveMessage(event) {
    iframe = document.getElementsByTagName('iframe')[3];
    iframe.setAttribute(name='title', event.data);
}
window.addEventListener('message', receiveMessage, false);

iframe = document.getElementsByTagName('iframe')[3];
iframe.contentWindow.postMessage('getSiteKey', '*');

