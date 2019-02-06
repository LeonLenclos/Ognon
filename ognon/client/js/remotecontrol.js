let playing = false;

const toolbar   = new Toolbar("toolbar");
const statusbar = new Statusbar("statusbar");

modules = [toolbar, statusbar];


///////////// SETUP
callModulesMethod('setup')
   
    
///////////// AUTOUPDATE
const autoUpdateOnPlay = () => {
    fetch('/view/get_cursor_infos/', initOptions())
    .then(response=>response.json())
    .then(json=>{
        console.log(json);
        if (json.playing){
            startAutoUpdate('onCursorMove');
        } else {
            stopAutoUpdate();
        }
    });
}

document.getElementById('play').addEventListener('click', autoUpdateOnPlay)
