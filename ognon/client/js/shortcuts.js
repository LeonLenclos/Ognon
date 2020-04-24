/*
* This file handle shortcuts.
*/


/****************
**** SETTINGS ***
****************/

const SHORTCUTS_JSON = '/js/shortcuts-ognon-keyboard.json';


/******************
**** SPECIALS *****
*******************/

let specials = {}; // An object containin specials function

// Toogle sleek view
specials.toggleSleekView = () => {
    document.body.classList.toggle('sleek');
}

// Prints shortcuts help
specials.shortcutsHelp = () => {
    console.log('shortcuts Help :')
    console.log(shortcuts)
    for(let sc in shortcuts){
        console.log(sc + ': ' + shortcuts[sc].description)
    }
}

// Select a specific tool
specials.selectDraw = () => {
    let selector = document.getElementById('tool-selector');
    selector.selectedIndex = 0;
}
specials.selectErease = () => {
    let selector = document.getElementById('tool-selector');
    selector.selectedIndex = 1;
}
specials.selectMove = () => {
    let selector = document.getElementById('tool-selector');
    selector.selectedIndex = 2;
}

/*****************
**** SHORTCUTS ***
*****************/

// Load shortcuts on the `shortcuts` object
let shortcuts = {}; 
fetch(SHORTCUTS_JSON)
.then(response=>response.json())
.then(json=>shortcuts=json);

// Return a string in the format used by the shortcuts definitions from an array of pressed keys.
shortcutRepresentation = (keysArray) =>
    keysArray.map((key, i)=>key == ' ' ? 'Space' : key).join('+');

// Do shortcut actions
doShortcut = (action) => {
    // Get args defined by the shortcut
    args = {};
    if(action.args){
        args = action.args;
    }

    // Call a control server function if defined, then call modules methods if defined.
    if(action.control){
        fetch('/control'+action.control, initOptions(args))
        .then(handleResponse)
        .then(()=>{
            if(action.modulesMethod){
                callModulesMethod(action.modulesMethod)
            }
            if(action.modulesMethods){
                action.modulesMethods.forEach((modulesMethod)=>{callModulesMethod(modulesMethod)})
            }
        })
    }

    // Call spectials functions if defined.
    if(action.specials){
        specials[action.specials](args);
    }
};


/*******************
**** KEY PRESS *****
*******************/

// keyPressed stored all pressed keys
let keysPressed = [];

// On keydown, add key to keyPressed 
window.addEventListener("keydown", e =>{
    // If key is pressed from an input element, return;
    if(e.target.localName == 'input') return;

    // Store key
    if(!keysPressed.includes(e.key))
        keysPressed.push(e.key);

    // If a shortcut is defined for pressed keys, do the shortcut.
    let repr = shortcutRepresentation(keysPressed);
    if(shortcuts[repr]){
        doShortcut(shortcuts[repr]);
        e.preventDefault();
    }
}); 

// On keyup, remove key from keyPressed
window.addEventListener("keyup", e =>{
    keysPressed = keysPressed.filter(item => item != e.key);
});