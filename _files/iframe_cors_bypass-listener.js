function getSiteKey (event) {
    if (event.data == 'getSiteKey') {
        iframe = document.getElementsByTagName('iframe')[0];
        siteKey = iframe.getAttribute('src');
        event.source.postMessage(siteKey, event.origin);
    }
    if (event.data.startsWith('captchaCallback')) {
        document.getElementsByName('g-recaptcha-response')[0].innerHTML = event.data.split("=")[1];
        captchaCallback();
    }
}
window.addEventListener('message', getSiteKey, false);

function geeTest (event) {
    if (event.data == 'geeTestGetChallenge') {
        script = document.getElementsByTagName('script')[2];
        challenge = script.getAttribute('src');
        event.source.postMessage(challenge, event.origin);
    }
    if (event.data.startsWith('geeTestCallback')) {
        console.log("geeTestCallback");
        console.log(event.data.split("=")[1]);
        console.log(event.data.split("=")[2]);
        console.log(event.data.split("=")[3]);
        geetestResponse = {
            geetest_challenge: event.data.split("=")[1],
            geetest_validate: event.data.split("=")[2],
            geetest_seccode: event.data.split("=")[3]
        };
        document.getElementsByName('geetest_challenge')[0].setAttribute("type", "display");
        document.getElementsByName('geetest_challenge')[0].setAttribute("value", event.data.split("=")[1]);
        document.getElementsByName('geetest_validate')[0].setAttribute("type", "display");
        document.getElementsByName('geetest_validate')[0].setAttribute("value", event.data.split("=")[2]);
        document.getElementsByName('geetest_seccode')[0].setAttribute("type", "display");
        document.getElementsByName('geetest_seccode')[0].setAttribute("value", event.data.split("=")[3]);
        captchaCallback();
    }
}
window.addEventListener('message', geeTest, false);