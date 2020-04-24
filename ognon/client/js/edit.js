/*
* This file is the script of edit.html page, the main page of the client.
*/


// Init modules.
modules = [
    new Canvas("canvas"),
    new Timeline("timeline"),
    new Toolbar("toolbar"),
    new Statusbar("element-statusbar", 'get_element_infos'),
    new CursorStatusbar("cursor-statusbar")
];

    
// Look for a project, get a default 'my_project' if none is defined. Then, start.
let start = () => {
    callModulesMethod('setup');
    startAutoUpdate();
}
fetch('/view/get_project_defined/', initOptions())
.then(handleResponse)
.then(project_defined=>{
    if (!project_defined){
        fetch('/control/projectmanager/get', initOptions({name:'my_project'}))
        .then(handleResponse)
        .then(start)
        .catch(handleError);
    } else {
        start();
    }
})
.catch(handleError);


