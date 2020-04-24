/*
* This file is the script of see.html page.
*/


// Init modules.
modules = [
    new SweetCanvas("canvas", true)
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
