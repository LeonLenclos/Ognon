const url = new URL(window.location.href);
const cursor = url.searchParams.get("cursor") || 'default';

const initOptions = (args, differentCursor) => {

    requestCursor = differentCursor || cursor
    return {
    method: 'post',
    headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        cursor: requestCursor,
        args: args
    })
};}

const handleResponse = (res) => {
        if (res.status === 400) {
            res.text().then(errMsg => alert(errMsg))
            throw 400
            return null
        }
        return res.json();
}

const handleResponseQuiet = (res) => {
        if (res.status === 400) {
            res.text().then(errMsg => console.log(errMsg))
            return null
        }
        return res.json();
}

// Auto update

let autoUpdating = false;
const autoUpdateFrameRate = 24; //fps

const autoUpdate = () => {
    if (autoUpdating) {
        callModulesMethod('update');
        setTimeout(autoUpdate, 1000/autoUpdateFrameRate);
    }
}
const startAutoUpdate = () => {
    if(!autoUpdating){
        autoUpdating = true;
        autoUpdate();
    } else {
        console.log("was already updatiung ! strange ????")
    }
}
const stopAutoUpdate = () => {
    autoUpdating = false;
}

