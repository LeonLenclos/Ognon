let shortcuts = {};
let specials = {};
let keysPressed = [];

fetch('/js/shortcuts.json')
.then(response=>response.json())
.then(json=>shortcuts=json);

shortcutRepresentation = (keysArray) =>
    keysArray.map((key, i)=>key == ' ' ? 'Space' : key).join('+');

doShortcut = action => {
    args = {};
    if(action.args){
        args = action.args;
    }
    if(action.control){
        fetch('/control'+action.control, initOptions(args))
        .then(handleResponse);
    }
    if(action.specials){
        specials[action.specials](args);
    }
    if(action.modulesMethod){
        callModulesMethod(action.modulesMethod)
    }
};

window.addEventListener("keydown", e =>{
    if(!keysPressed.includes(e.key))
        keysPressed.push(e.key);

    if(shortcuts[shortcutRepresentation(keysPressed)]){
        if(e.target.localName != 'input'){
            doShortcut(shortcuts[shortcutRepresentation(keysPressed)]);
            e.preventDefault();
        }
    }
}); 

window.addEventListener("keyup", e =>{
    keysPressed = keysPressed.filter(item => item != e.key);
});

specials.toggleSleekView = () => {
    document.body.classList.toggle('sleek');
}

specials.autoUpdateOnPlay = () => {
    if(autoUpdateOnPlay){
        autoUpdateOnPlay();
    }
}