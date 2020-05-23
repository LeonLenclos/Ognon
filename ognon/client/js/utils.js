
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


const shortcutRepresentation = (keysArray) =>{
    return keysArray.map((key, i)=>key == ' ' ? 'Space' : key).join('+');
}



// Colors

const hexToRgb = (hex) => {
  // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
  var shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
  hex = hex.replace(shorthandRegex, function(m, r, g, b) {
    return r + r + g + g + b + b;
  });

  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

const rgbToBwContrast = (rgb) => {
  // http://www.w3.org/TR/AERT#color-contrast
  const brightness = Math.round(((parseInt(rgb.r) * 299) +
                      (parseInt(rgb.g) * 587) +
                      (parseInt(rgb.b) * 114)) / 1000);
 return (brightness > 125) ? 'black' : 'white';
}