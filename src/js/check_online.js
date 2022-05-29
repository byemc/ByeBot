
fetch('https://bbapi.byemc.xyz/info')
    .then(response => {
        return response.json();
    })
    .then(online_status => {
        console.log(online_status);
    });