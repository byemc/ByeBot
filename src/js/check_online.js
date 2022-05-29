
bb_response = fetch("https://bbapi.byemc.xyz/info").then(response => response.json()).catch(error => {
    console.error(error);
    return {};
});

console.log(bb_response);
