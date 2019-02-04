let playing = false;

const canvas    = new Canvas("canvas");
const timeline  = new Timeline("timeline");
const toolbar   = new Toolbar("toolbar");
const statusbar = new Statusbar("statusbar");

const modules = [canvas, timeline, toolbar, statusbar];


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
