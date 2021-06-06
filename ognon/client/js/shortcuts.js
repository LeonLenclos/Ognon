let stdKeyboardShortcuts = {
    'd':{action:'selectTool', args:{tool:'draw'}},
    'e':{action:'selectTool', args:{tool:'erease'}},
    'm':{action:'selectTool', args:{tool:'move'}},
    'Control+ArrowLeft':{action:'elementMoveBackward'},
    'Control+ArrowRight':{action:'elementMoveForward'},
    'Control+c':{action:'elementCopy'},
    'Control+x':{action:'elementCut'},
    'Control+v':{action:'elementPaste'},
    'Control+d':{action:'elementDuplicate'},
    'Control+Delete':{action:'layerDel'},
    'Backspace':{action:'drawingClear'},
    'Delete':{action:'elementDel'},
    'c':{action:'elementAddCellAfter'},
    'Alt+c':{action:'elementAddCellBefore'},
    'PageUp':{action:'navigationFirstFrm'},
    'PageDown':{action:'navigationLastFrm'},
    'ArrowLeft':{action:'navigationPrevFrm'},
    'ArrowRight':{action:'navigationNextFrm'},
    'Enter':{action:'navigationAutoRun'},
    'Space':{action:'navigationPlay'},
    'Control+s':{action:'projectSave'},
    't':{action:'tagAdd'},
    '+':{action:'zoomIn'},
    '-':{action:'zoomOut'},
    '=':{action:'zoomReset'},
    
    
};

// Set of shortcut for use with a special ognon keyboard
let ognKeyboardShortcuts = {
    '!':{action:'selectTool', args:{tool:'draw'}},
    ':':{action:'selectTool', args:{tool:'erease'}},
    ';':{action:'selectTool', args:{tool:'move'}},
    'u':{action:'elementMoveBackward'},
    'j':{action:'elementMoveForward'},
    'y':{action:'elementCopy'},
    'h':{action:'elementPaste'},
    'b':{action:'layerDel'},
    'v':{action:'drawingClear'},
    'c':{action:'elementDel'},
    'f':{action:'elementAddCellAfter'},
    'r':{action:'elementAddCellBefore'},
    'e':{action:'navigationFirstFrm'},
    'd':{action:'navigationLastFrm'},
    'z':{action:'navigationPrevFrm'},
    's':{action:'navigationNextFrm'},
    'a':{action:'navigationAutoRun'},
    'q':{action:'navigationPlay'},
};

// Turing Test Specifics Shortcucts.
let ttKeyboardShorcuts = {
    '=':{action:'projectGet', args:{name:'tt1'}},
    '$':{action:'projectGet', args:{name:'tt2'}},
    '*':{action:'projectGet', args:{name:'tt3'}},
    'œ':{action:'animSelect', args:{name:'master'}},
    '&':{action:'animSelect', args:{name:'a'}},
    'é':{action:'animSelect', args:{name:'b'}},
    '"':{action:'animSelect', args:{name:'c'}},
    '\'':{action:'animSelect', args:{name:'d'}},
    '(':{action:'animSelect', args:{name:'e'}},
};

// define the shortcutsSets object
let shortcutsSets = {
    'std':stdKeyboardShortcuts,
    'ogn':ognKeyboardShortcuts,
    'tt':Object.assign(ognKeyboardShortcuts, ttKeyboardShorcuts),
};
