// Ognon   
app.addAction('ognAbout', {
    menu:'Ognon',
    text:'About',
   description:"Open the About page.",
    clientFunction:openInNewTab,
    args:{
        url:{value:'/about.html'}
    }
});
app.addAction('ognHelp', {
    menu:'Ognon',
    text:'Help',
   description:"Open the Help page",
    clientFunction:openInNewTab,
    args:{
        url:{value:'/help.html'}
    }
});
app.addAction('ognSee', {
    menu:'Ognon',
    text:'See',
   description:"Open the See page",
    clientFunction:()=>openInNewTab({url:'/see.html?cursor='+app.cursor}),
});
app.addAction('ognSelectCursor', {
    menu:'Ognon',
    text:'Select Cursor',
   description:"Select a cursor.",
    clientFunction:({cursor})=>app.selectCursor(cursor),
    args:{
        cursor:{description:'Name of the cursor'}
    }
});
app.addAction('ognToggleGUISize', {
    menu:'Ognon',
    text:'Toggle GUI size',
   description:"Toggle between big and small graphic user interface.",
    clientFunction:()=>document.body.classList.toggle('big'),
});
app.addAction('ognToggleFullScreen', {
    menu:'Ognon',
    text:'Toggle Full Screen',
   description:"Toggle between window and full screen.",
    clientFunction:()=>document.fullscreenElement?document.exitFullscreen():document.body.requestFullscreen(),
});
// Project 
app.addAction('projectGet', {
    menu:'Project',
   text:'Get Project',
   description:"Choose and open a project.",
    serverCursorFunction:'/control/projectmanager/get/',
    args:{
        name:{
           description:"Name of the project",
            suggestionListFromServer:"/view/get_projects"
        }
    }
});
app.addAction('projectLoad', {
    menu:'Project',
   text:'Load Project',
   description:"Load project from disk.",
    serverCursorFunction:'/control/projectmanager/load/',
});
app.addAction('projectSave', {
    menu:'Project',
   text:'Save Project',
   description:"Save project to disk.",
    serverCursorFunction:'/control/projectmanager/save/',
});
// Anims   
app.addAction('animSelect', {
    menu:'Anims',
   text:'Select Anim',
   description:"Select an animation.",
    serverCursorFunction:'/control/animsmanager/select_anim/',
    args:{
        name:{
           description:"Name of the animation",
          suggestionListFromServer:"/view/get_anims"
        }
    }
});
app.addAction('animrefSelect', {
    menu:'Anims',
   text:'Select Animref',
   description:"Select the animation referenced by selected animref.",
    serverCursorFunction:'/control/animsmanager/select_animref/',
});
app.addAction('animrefNew', {
    menu:'Anims',
   text:'New Animref',
   description:"Create an animref pointing to a new animation which contains selected element.",
    serverCursorFunction:'/control/animsmanager/new_animref/',
    args:{
        name:{
            description:"Name of the animation",
        }
    }
});
// Export  
app.addAction('exportFrmToPng', {
    menu:'Export',
   text:'Frm to png',
   description:"Export a frm to png.",
    serverCursorFunction:'/control/exporter/frm_to_png/',
});
app.addAction('exportAnimToPngs', {
    menu:'Export',
   text:'Anim to png Sequence',
   description:"Export an animation to png sequence.",
    serverCursorFunction:'/control/exporter/anim_to_pngs/',
});
app.addAction('exportAnimToTgas', {
    menu:'Export',
   text:'Anim to tgas Sequence',
   description:"Export an animation to tga sequence.",
    serverCursorFunction:'/control/exporter/anim_to_tgas/',
});
app.addAction('exportAnimToGif', {
    menu:'Export',
   text:'Anim to gif',
   description:"Export an animation to gif.",
    serverCursorFunction:'/control/exporter/anim_to_gif/',
});
app.addAction('exportAnimToAvi', {
    menu:'Export',
   text:'Anim to avi',
   description:"Export an animation to avi.",
    exportAnimToAvi:'/control/exporter/anim_to_avi/',
});

// Navigation
app.addAction('navigationRun', {
    menu:'Navigation',
   text:'Run',
   description:"Run the animation",
    serverCursorFunction:'/control/navigator/run/',
});
app.addAction('navigationAutoRun', {
    menu:'Navigation',
   text:'Auto Run',
   description:"Run the animation at each tick of a clock",
    serverCursorFunction:'/control/navigator/auto_run/',
});
app.addAction('navigationPlay', {
    menu:'Navigation',
   text:'Play',
   description:"Toogle play mode",
    serverCursorFunction:'/control/navigator/play/',
});
app.addAction('navigationPrevFrm', {
    menu:'Navigation',
   text:'Previous Frm',
   description:"Select previous frm",
    serverCursorFunction:'/control/navigator/prev_frm/',
});
app.addAction('navigationNextFrm', {
    menu:'Navigation',
   text:'Next Frm',
   description:"Select next frm",
    serverCursorFunction:'/control/navigator/next_frm/',
});
app.addAction('navigationFirstFrm', {
    menu:'Navigation',
   text:'First Frm',
   description:"Select first frm",
    serverCursorFunction:'/control/navigator/first_frm/',
});
app.addAction('navigationLastFrm', {
    menu:'Navigation',
   text:'Last Frm',
   description:"Select last frm",
    serverCursorFunction:'/control/navigator/last_frm/',
});
// Elements
app.addAction('elementMoveBackward', {
    menu:'Elements',
   text:'Move Element Backward',
   description:"Move Backward",
    serverCursorFunction:'/control/elementsorganizer/move_element_backward/',
});
app.addAction('elementMoveForward', {
    menu:'Elements',
   text:'Move Element Forward',
   description:"Move Forward",
    serverCursorFunction:'/control/elementsorganizer/move_element_forward/',
});
app.addAction('elementDel', {
    menu:'Elements',
   text:'Delete Element',
   description:"Delete",
    serverCursorFunction:'/control/elementsorganizer/del_element/',
});
app.addAction('elementDuplicate', {
    menu:'Elements',
   text:'Duplicate Element',
   description:"Duplicate",
    serverCursorFunction:'/control/elementsorganizer/duplicate_element/',
});
app.addAction('elementCopy', {
    menu:'Elements',
   text:'Copy Element',
   description:"Copy",
    serverCursorFunction:'/control/elementsorganizer/copy_element/',
});
app.addAction('elementCut', {
    menu:'Elements',
   text:'Cut Element',
   description:"Cut",
    serverCursorFunction:'/control/elementsorganizer/cut_element/',
});
app.addAction('elementPaste', {
    menu:'Elements',
   text:'Paste Element',
   description:"Paste",
    serverCursorFunction:'/control/elementsorganizer/paste_element/',
});
app.addAction('elementAddCellAfter', {
    menu:'Elements',
   text:'Add Cell After',
   description:"Add Cell After",
    serverCursorFunction:'/control/elementsorganizer/add_cell_after/',
});
app.addAction('elementAddCellBefore', {
    menu:'Elements',
   text:'Add Cell Before',
   description:"Add Cell Before",
    serverCursorFunction:'/control/elementsorganizer/add_cell_before/',

});
app.addAction('elementAddAnimRefAfter', {
    menu:'Elements',
   text:'Add Animref Before',
   description:"Add AnimRef After",
    serverCursorFunction:'/control/elementsorganizer/add_animref_after/',
    args:{
        name:{
            description:"Name of the animation",
          suggestionListFromServer:"/view/get_anims"

        }
    }
});
app.addAction('elementAddAnimRefBefore', {
    menu:'Elements',
   text:'Add Animref Before',
   description:"Add AnimRef Before",
    serverCursorFunction:'/control/elementsorganizer/add_animref_before/',
    args:{
        name:{
        description:"Name of the animation",
            suggestionListFromServer:"/view/get_anims"

        }
    }
});
// Layers  
app.addAction('layerAdd', {
    menu:'Layers',
   text:'Add Layer',
   description:"Add layer",
    serverCursorFunction:"/control/layersorganizer/add_layer/",
});
app.addAction('layerMoveUp', {
    menu:'Layers',
   text:'Move Layer Up',
   description:"Move layer Up",
    serverCursorFunction:"/control/layersorganizer/move_layer_up/",
});
app.addAction('layerMoveDown', {
    menu:'Layers',
   text:'Move Layer Down',
   description:"Move layer Down",
    serverCursorFunction:"/control/layersorganizer/move_layer_down/",
});
app.addAction('layerDel', {
    menu:'Layers',
   text:'Delete Layer',
   description:"Delete layer",
    serverCursorFunction:"/control/layersorganizer/del_layer/",
});
// Tags
app.addAction('tagAdd', {
    menu:'Tags',
   text:'Add Tag',
   description:"Add a tag to the selected element",
    serverCursorFunction:'/control/tagger/add_tag/',
    args:{
        tag:{
        description:"Tag",
        }
    }
});
app.addAction('tagsClear', {
    menu:'Tags',
   text:'Clear Tags',
   description:"Clear all the element tags",
    serverCursorFunction:"/control/tagger/rm_tags/",
});

// Drawing 
app.addAction('drawingClear', {
    menu:'Drawing',
   text:'Clear Drawing',
   description:"Clear the current cell",
    serverCursorFunction:"/control/drawer/clear/",
});



// Lightbox
app.addAction('selectTool', {
    menu:'Lightbox',
   text:'Select Tool',
   description:"Select a tool.",
    clientFunction:(args)=>app.modules['lightbox'].canvas.selectTool(args.tool),
    args:{
        tool:{}
    }
});
app.addAction('zoomIn', {
    menu:'Lightbox',
   text:'Zoom In',
   description:"Zoom in the animation canvas.",
    clientFunction:(args)=>app.modules['lightbox'].canvas.zoomIn(),
});
app.addAction('zoomOut', {
    menu:'Lightbox',
   text:'Zoom Out',
   description:"Zoom out the animation canvas.",
    clientFunction:(args)=>app.modules['lightbox'].canvas.zoomOut(),
});
app.addAction('zoomReset', {
    menu:'Lightbox',
   text:'Reset Zoom',
   description:"Reset the animation canvas zoom ratio to 1.",
    clientFunction:(args)=>app.modules['lightbox'].canvas.zoomReset(),
});

app.addAction('zoomContains', {
    menu:'Lightbox',
   text:'Zoom Contains',
   description:"Scale the animation canvas to make the image fully visible",
    clientFunction:(args)=>app.modules['lightbox'].canvas.zoomContains(),
});
