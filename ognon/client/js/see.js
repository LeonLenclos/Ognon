const canvas = new Canvas("canvas", true);
modules = [canvas];


///////////// SETUP
callModulesMethod('setup');
startAutoUpdate('onCursorMove');
