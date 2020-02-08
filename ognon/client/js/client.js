const url = new URL(window.location.href);
const cursor = url.searchParams.get("cursor") || 'default';


// Modules

let modules = [];
let callModulesMethodBusy = false;
// let modulesRequest = {};

const callModulesMethod = (modulesMethod) => {

    if (callModulesMethodBusy) return;

    const onLoad = (viewInfos) => {
        modules.forEach(mo => {
            if(mo.busy || !mo[modulesMethod]) return;
            mo.busy = true;
            mo[modulesMethod](viewInfos);
            mo.busy = false;

        });
        callModulesMethodBusy = false;
    }

    callModulesMethodBusy = true;

    let modulesRequest = {'get_cursor_infos':{}}
    modules.forEach(mo => {
        modulesRequest = Object.assign(modulesRequest, mo.request)
    });

    fetch('/view/get/', initOptions({request:modulesRequest}))
    .then(handleResponse)
    .then(onLoad)
    .catch(handleError);
}

// Request

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
            console.log(res);
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

const handleError = (e) => {
    console.log("ERROR : ");
    console.log(e);
}

// Auto update

let autoUpdating = false;
const FPS = 30; //fps
const DELAY = 1000/FPS; //fps
let time = null;
let frame = -1;
let tref;
const autoUpdate = (timestamp) => {
    if (!autoUpdating) return;
    if(time == null) time = timestamp;
    let seg = Math.floor((timestamp - time) / DELAY);
    if(seg > frame){
        frame = seg
        callModulesMethod('update');
    }
    requestAnimationFrame(autoUpdate);
}

const startAutoUpdate = () => {
    if(!autoUpdating){
        autoUpdating = true;
        autoUpdate();
    } else {
        console.log("was already autoUpdating ! strange ????")
    }
}
const stopAutoUpdate = () => {
    autoUpdating = false;
}


