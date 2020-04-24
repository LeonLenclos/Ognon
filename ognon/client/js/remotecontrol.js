/*
* This file is the script of remotecontrol.html page.
*/


// Init modules.
modules = [
    new Toolbar("toolbar"),
    new Statusbar("element-statusbar", 'get_element_infos'),
];

    
// Start.
callModulesMethod('setup');
startAutoUpdate();