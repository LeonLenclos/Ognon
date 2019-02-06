const url = new URL(window.location.href);
const cursor = url.searchParams.get("cursor") || 'default';

const initOptions = (args) => {return{
    method: 'post',
    headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        cursor: cursor,
        args: args
    })
};}


// Auto update

let autoUpdating = false;
const autoUpdateFrameRate = 24; //fps

const autoUpdate = (method) => {
    if (autoUpdating) {
        callModulesMethod(method);
        setTimeout(autoUpdate, 1000/autoUpdateFrameRate, method);
    }
}
const startAutoUpdate = (method) => {
    autoUpdating = true;
    autoUpdate(method);
}
const stopAutoUpdate = (method) => {
    autoUpdating = false;
}

