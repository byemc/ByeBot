
fetch('https://bbapi.byemc.xyz/info')
    .then(response => {
        return response.json();
    })
    .then(online_status => {
        console.log(online_status.online);
        if (online_status.online == true) {
            document.getElementById("onl-indicator").innerHTML = "online";
            document.getElementById("onl-indicator").style.color = "green";
        } else {
            document.getElementById("onl-indicator").innerHTML = "offline";
            document.getElementById("onl-indicator").style.color = "red";
        }
    })
    .catch(error => {
        console.log(error);
        document.getElementById("onl-indicator").innerHTML = "offline";
        document.getElementById("onl-indicator").style.color = "red";
    });

