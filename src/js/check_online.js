
function checkOnline() {
    return fetch('https://bbapi.byemc.xyz/info').then(response => {
        if (response.contentType === 'application/json') {
            return response.json();
        } else {
            return {};
        }
    });
}

bbonline = JSON.parse(checkOnline());
if (bbonline.online) {
    document.getElementById('onl-indicator').innerHTML = 'Online';
    document.getElementById('onl-indicator').style.color = '#00ff00';
}
else {
    document.getElementById('onl-indicator').innerHTML = 'Offline';
    document.getElementById('onl-indicator').style.color = '#ff0000';
}
