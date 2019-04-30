const canvas = new SweetCanvas("canvas", true);
modules = [canvas];


///////////// SETUP
callModulesMethod('setup');
startAutoUpdate('onCursorMove');
