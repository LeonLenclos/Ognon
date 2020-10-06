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

// Add Turing Test Shortcucts.
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
Object.assign(ognKeyboardShortcuts, ttKeyboardShorcuts)