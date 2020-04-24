/*
* This file is the main script of the client.
*/

const url = new URL(window.location.href);
const cursor = url.searchParams.get("cursor") || 'default';

/*******************/
/***** MODULES *****/
/*******************/

// This array must be filled by the page script with the modules of the page.
let modules = []; 

// CallModuleMethod is used to call a specific method for each modules of the modules array.
// Before doing that, it runs a group query for everything the modules need. (`request` attribute of the modules)
// This function also checkout for itself and for each modules if they are not already working. (handling `callModulesMethodBusy` and the `busy` attribute of the modules)
let callModulesMethodBusy = false;
const callModulesMethod = (modulesMethod) => {

    if (callModulesMethodBusy) return; 

    // Call modulesMethod for each module after getting viewInfos.
    const onLoad = (viewInfos) => {
        modules.forEach(mo => {
            if(mo.busy || !mo[modulesMethod]) return;
            mo.busy = true;
            mo[modulesMethod](viewInfos);
            mo.busy = false;

        });
        callModulesMethodBusy = false;
    };

    callModulesMethodBusy = true;

    // modulesRequest contains by default get_cursor_infos and we add the requests of each module.
    let modulesRequest = {'get_cursor_infos':{}}
    modules.forEach(mo => {
        modulesRequest = Object.assign(modulesRequest, mo.request)
    });

    // Get all requests of modulesRequest.
    fetch('/view/get/', initOptions({request:modulesRequest}))
    .then(handleResponse)
    .then(onLoad)
    .catch(handleError);
}


/********************/
/***** REQUESTS *****/
/********************/

// Returns the options that must be passed to `fetch`
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
    };
}

// Check for errors and returns json converted response.
const handleResponse = (res) => {
        if (res.status === 400) {
            console.log(res);
            res.text().then(errMsg => alert(errMsg))
            throw 400
            return null
        }
        return res.json();
}

// Same as handleResponse but does'nt throw error.
const handleResponseQuiet = (res) => {
        if (res.status === 400) {
            res.text().then(errMsg => console.log(errMsg))
            return null
        }
        return res.json();
}

// Display thrown error in the console.
const handleError = (e) => {
    console.log("ERROR : ");
    console.log(e);
}


/**********************/
/***** AUTOUPDATE *****/
/**********************/

const FPS = 30; // fps
const DELAY = 1000/FPS; // fps
let autoUpdating = false;
let time = null;
let frame = -1;

// calls callmodulesmethod('update') in a recursion loop while autoUpdating is true
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
    }
}

const stopAutoUpdate = () => {
    autoUpdating = false;
}


