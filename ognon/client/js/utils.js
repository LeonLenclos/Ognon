
// Network


const initOptionsCursor = (args, requestCursor) => {
    args = args || {}
    requestCursor = requestCursor || cursor
    args.cursor = requestCursor;
    return initOptions(args);
}


// Check for errors and returns json converted response.
const handleResponse = (res) => {
        if (res.status === 400) {
            // console.log(res);
            // res.text().then(errMsg => alert(errMsg))
            return res.text().then(errMsg => {
                throw new Error(errMsg);
            });
        }
        return res;
}

// Same as handleResponse but does'nt throw error.
const handleResponseQuiet = (res) => {
        if (res.status === 400) {
            res.text().then(errMsg => console.log(errMsg))
            return null
        }
        return res;
}

// Display thrown error in the console.
const handleError = (e) => {
    console.log("ERROR : ");
    console.log(e);
}



const handleJson = (res) => res.json();
const handleText = (res) => res.text();

const post = (path, json) => {
    return fetch(path, {
        method:'post',
        body:JSON.stringify(json || {})
    })
    .then(handleResponse)
    .then(handleJson)
}

const get = (path) => {
    return fetch(path, {method:'get'})
    .then(handleResponse)
    .then(handleText)
}


// Divers

const openInNewTab = ({url}) => window.open(url, '_blank').focus();
