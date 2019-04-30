let shortcuts = {};
let specials = {};
let keysPressed = [];

fetch('/js/shortcuts-ognon-keyboard.json')
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
        .then(handleResponse)
        .then(()=>{
            if(action.modulesMethod){
                callModulesMethod(action.modulesMethod)
            }
            if(action.modulesMethods){
                for (var i = 0; i < action.modulesMethods.length; i++) {
                    callModulesMethod(action.modulesMethods[i]);
                }
            }
        })
    }
    if(action.specials){
        specials[action.specials](args);
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

specials.shortcutsHelp = () => {
    console.log('shortcuts Help :')
    console.log(shortcuts)
    for(let sc in shortcuts){
        console.log(sc + ': ' + shortcuts[sc].description)
    }
}