const canvas = new SweetCanvas("canvas", true);
modules = [canvas];


///////////// SETUP

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