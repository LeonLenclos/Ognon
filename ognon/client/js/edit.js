let playing = false;

const canvas    = new Canvas("canvas");
const timeline  = new Timeline("timeline");
const toolbar   = new Toolbar("toolbar");
const elementStatusbar = new Statusbar("element-statusbar", 'get_element_infos');
const cursorStatusbar = new CursorStatusbar("cursor-statusbar");

modules = [canvas, timeline, toolbar, cursorStatusbar, elementStatusbar];

    
///////////// AUTOUPDATE
// const autoUpdateOnPlay = () => {
//     fetch('/view/get_cursor_infos/', initOptions())
//     .then(response=>response.json())
//     .then(json=>{
//         console.log(json.playing)
//         if (json.playing){
//             startAutoUpdate();
//         } else {
//             stopAutoUpdate();
//         }
//     });
// }

// document.getElementById('play').addEventListener('click', autoUpdateOnPlay)
// document.getElementById('auto_play').addEventListener('click', autoUpdateOnPlay)

fetch('/view/get_project_defined/', initOptions())
.then(handleResponse)
.then(project_defined=>{
    if (!project_defined){
        fetch('/control/projectmanager/get', initOptions({name:'my_project'}))
        .then(handleResponse)
        .then(()=>{
            callModulesMethod('setup');
            startAutoUpdate();
        })
        .catch(handleError);
    } else {
        callModulesMethod('setup');
        startAutoUpdate();
    }
})
.catch(handleError);


