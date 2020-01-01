/****************
**** SETTINGS ***
****************/

const PRECISION = 3; // Min pixel length of a stroke
const IGNORE_CALLMODMET_BUSY = false; // set to true for debugging

/****************
**** MODULES ****
****************/
let modules = [];
let callModulesMethodBusy = false;
let callModulesMethodBusyCount = 0;
function callModulesMethod(modulesMethod) {
    if (!callModulesMethodBusy || IGNORE_CALLMODMET_BUSY) {
        callModulesMethodBusy = true;
        fetch('/view/get_cursor_infos/', initOptions())
        .then(handleResponse)
        .then(cursorInfos =>{
            modules.forEach(mo => {
                if(mo[modulesMethod] && !mo.busy){
                    mo.busy = true;
                    let callBack = ()=>{mo.busy = false; mo.busyCount = 0}
                    mo[modulesMethod](callBack, cursorInfos);
                } else if (mo.busy){
                    mo.busyCount += 1;
                    // console.log("busy ("+mo.busyCount+") : "+mo.id+" ("+modulesMethod+")");
                }
            });
            callModulesMethodBusy = false;
            callModulesMethodBusyCount = 0;
        })
        .catch(handleError);
    } else {
        callModulesMethodBusyCount += 1;
        // console.log('busy ('+callModulesMethodBusyCount+') : callModulesMethod !')
    }

}

class Module {
    constructor(id) {
        this.id = id;
        this.elmt = document.getElementById(id);
        this.busy = false;
        this.busyCount = 0;
    }
}

/***************
**** CANVAS ****
***************/

//// EVENTS ////


let mouseDownCoords = [];
let onCallDrawerBusy = false;


const callDrawer = () => {

    onCallDrawerBusy = true;
    let tool = document.getElementById('tool-selector').value
    let args;
    if (tool == 'draw'){
        args = {coords:mouseDownCoords};
    } else if (tool == 'erease'){
        args = {coords:[mouseDownCoords[mouseDownCoords.length-2],mouseDownCoords[mouseDownCoords.lenght-1]]};
    }
    fetch('/control/drawer/'+tool+'/', initOptions(args))
    .then(()=>{onCallDrawerBusy = false;})
    .catch(handleError);
};

const onCanvasMouseDown = (e) => {
    mouseDownCoords = [e.offsetX, e.offsetY];
};

const onMouseUp = (e) => {

    callDrawer();
    mouseDownCoords = [];
    

};

const onCanvasMouseMove = (e) => {

    if(mouseDownCoords.length>1){

        let x = e.offsetX;
        let y = e.offsetY;
        let px = mouseDownCoords[mouseDownCoords.length-2];
        let py = mouseDownCoords[mouseDownCoords.length-1];

        mouseDownCoords = mouseDownCoords.concat([x, y]);


        // send tool request only if the distance between mouse and pMouse is greater than PRECISION
        if(Math.abs(px - x) > PRECISION || Math.abs(py - y) > PRECISION) {

            if(!onCallDrawerBusy){
                // console.log(mouseDownCoords);
                callDrawer();
                mouseDownCoords = [x, y];

            }
            else {
                console.log("busy : onCanvasMouseMove")
            }


        }
    }
};

// const useCurrentTool(x1, y1, x2, y2)
//// UTILS ////

const drawLines = (lines, style, ctx) => {
    ctx.lineWidth = style.lineWidth;
    ctx.strokeStyle = style.lineColor;
    ctx.beginPath();
    lines.forEach((line) => {
        ctx.moveTo(line[0], line[1]);
        for (var i = 2; i < line.length; i+=2) {
            ctx.lineTo(line[i], line[i+1]);
        }
    });
    ctx.stroke();
}

const clearCanvas = (ctx, bgColor) => {
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, ctx.canvas.clientWidth, ctx.canvas.clientHeight);
}

//// CLASS ////

class Canvas extends Module {
    constructor(id, noOnionSkin=false, onTopOfDefault=false) {
        super(id);
        this.noOnionSkin = noOnionSkin;
        this.responseHandler = handleResponse;

        this.cache = {};
        this.currentImageID = "";
        this.updating = false;
    }

    loadConfig(config) {
        this.elmt.width  = config.width;
        this.elmt.height = config.height;
        this.backgroundColor = config.background_color;
        this.lineColor = config.line_color;
        this.lineWidth = config.line_width;
        this.onionFwColor = config.onion_skin_forward_color;
        this.onionBwColor = config.onion_skin_backward_color;
        this.onionWidth = config.onion_skin_line_width;
    }

    setup(callBack, cursorInfos) {

        this.ctx = this.elmt.getContext('2d');
        this.elmt.addEventListener('mousedown', onCanvasMouseDown);
        this.elmt.addEventListener('mousemove', onCanvasMouseMove);
        addEventListener('mouseup',   onMouseUp);

        // load config
        fetch('/view/get_view_config/', initOptions())
        .then(this.responseHandler)
        .then(json =>{
            this.loadConfig(json);
            this.update(callBack, cursorInfos);
        })
        .catch(handleError);
    }

    update(callBack, cursorInfos) {
        /*
        Call draw or drawOnionSkin depending on playing info given by /view/get_cursor_infos/
        */
        if (cursorInfos.playing || this.noOnionSkin) {
            this.draw(cursorInfos, [0])
        } else {
            this.draw(cursorInfos, [-1, 0, 1])
        }
        this.updating = false;
        callBack();
    }

    draw(cursorInfos, onionRange=[0]) {
        /*
        Draw lines given by /view/get_onion_skin/ 
        */
        let cursorPos = cursorInfos.project_name + ' ' + cursorInfos.anim + ' ' +  cursorInfos.layer + ' ' + cursorInfos.frm;
        let projState = cursorInfos.project_state_id + ' '  + cursorInfos.project_draw_state_id;
        let imageID = cursorPos + ' ' + projState + ' '  + onionRange;

        let getCol = (skin) => {
            if(skin < 0){
                return this.onionBwColor;
            } else if (skin > 0) {
                return this.onionFwColor;
            } else{
                return this.lineColor;
            }
        };

        let drawSkin = (skins, i) => {
            drawLines(skins[i], {lineWidth:this.lineWidth, lineColor:getCol(i)}, this.ctx);
        };

        let drawSkins = (skins, range) => {
            clearCanvas(this.ctx, this.backgroundColor);
            range.filter(e=>e!=0).forEach(i=>{
                drawSkin(skins, i);
            });
            drawSkin(skins, 0);
        };

        if (this.currentImageID == imageID)
        {
            return;
        }
        else if (cursorPos in this.cache 
                && onionRange.every((i)=> i in this.cache[cursorPos].onionSkin) 
                && this.cache[cursorPos].state_id == projState)
        {
            drawSkins(this.cache[cursorPos].onionSkin, onionRange);
            this.currentImageID = imageID
        }
        else
        {
            fetch('/view/get_onion_skin/', initOptions({
                frm:cursorInfos.frm,
                anim:cursorInfos.anim,
                onion_range:onionRange}))
            .then(this.responseHandler)
            .then(onionSkin => {
                drawSkins(onionSkin, onionRange);
                this.cache[cursorPos] = {
                    state_id:projState,
                    onionSkin:onionSkin
                };
                this.currentImageID = imageID
            })
            .catch(handleError);

        }
    }
}


class SweetCanvas extends Canvas {
    /*
    Same as Canvas but ignore errors
    */
    constructor(id, noOnionSkin=false) {
        super(id, noOnionSkin);
        this.responseHandler = handleResponseQuiet;
    }

}


/****************
**** TOOLBAR ****
****************/

//// EVENTS ////

const onControlClick = (e) => {
    let url = '/control/'
        + e.currentTarget.parentNode.id + '/'
        + e.currentTarget.id + '/';
    let args = {};

    if(e.currentTarget.dataset.required) {
        let required = e.currentTarget.dataset.required.split(" ");
        required.forEach(r=>{
            args[r] = e.currentTarget.parentNode.querySelector('input[name='+r+']').value;
        });
    }
    

    fetch(url, initOptions(args))
    .then(handleResponse)
   // .then(()=>callModulesMethod('update'))
    .catch(handleError);
};

//// CLASS ////

class Toolbar extends Module {
    constructor(id) {
        super(id);
    }

    setup(callBack, cursorInfos) {
        this.elmt.querySelectorAll("button")
        .forEach(control=>control.addEventListener('click', onControlClick));
        this.elmt.querySelectorAll('#projectmanager button')
        .forEach(e=>e.addEventListener('click', ()=>callModulesMethod('setup')));
        callBack();
    }
}

/*****************
**** TIMELINE ****
*****************/

//// EVENTS ////

const onFrmClick = (e) => {
    let i = Number(e.currentTarget.dataset.frm);
    fetch('/control/navigator/go_to_frm/', initOptions({i:i}))
    //.then(()=>callModulesMethod('update'))
    .catch(handleError);
};

const onLayerClick = (e) => {
    let layer = Number(e.currentTarget.dataset.layer);
    fetch('/control/navigator/go_to_layer/', initOptions({i:layer}))
    //.then(()=>callModulesMethod('update'))
    .catch(handleError);
}

const onElementClick = (e) => {
    let i = Number(e.currentTarget.dataset.frm);
    let layer = Number(e.currentTarget.parentNode.dataset.layer);
    fetch('/control/navigator/go_to_frm/', initOptions({i:i}))
    .then(fetch('/control/navigator/go_to_layer/', initOptions({i:layer})))
    //.then(()=>callModulesMethod('update'))
    .catch(handleError);
}
///// UTILS /////

const createElement = (frm, element) => {
    let td = document.createElement("td");
    td.addEventListener('click', onElementClick);
    td.dataset.frm = frm;
    td.setAttribute("colspan", element.len);
    return td;
}

const createLayerHead = () => {
    let td = document.createElement("td");
    td.addEventListener('click', onLayerClick);
    return td;
}
const createFrmHead = (i) => {
    let td = document.createElement("td");
    td.addEventListener('click', onFrmClick);
    td.dataset.frm = i;
    return td;
}

const createLayerRow = (i, elements) => {
    let tdArray = [createLayerHead()];
    let frm = 0;
    for (let j = 0; j < elements.length; j++) {
        tdArray.push(createElement(frm, elements[j]));
        frm+=elements[j].len;
    }
    let layerRow = document.createElement("tr");
    layerRow.classList.add('layer-row')
    layerRow.dataset.layer = i;
    tdArray.forEach(td=>layerRow.appendChild(td));
    return layerRow;
}

const createFrmsRow = (len) => {
    let tdArray = [createLayerHead()];
    for (let i = 0; i < len; i++) {
        tdArray.push(createFrmHead(i));
    }
    let frmsRow = document.createElement("tr");
    frmsRow.classList.add('frms-row');
    tdArray.forEach(td=>frmsRow.appendChild(td));
    return frmsRow;
}

const createTimeline = (timeline, table) => {
    while(table.firstChild && table.removeChild(table.firstChild)); //empty
    table.appendChild(createFrmsRow(timeline.len));
    for (var i = 0; i < timeline.layers.length; i++) {
        table.appendChild(createLayerRow(i, timeline.layers[i]));
    }
}

const setActiveElement = (dataname, i, element) => {
    if(element.dataset[dataname] == i){
        element.classList.add('active');
    } else {
        element.classList.remove('active');
    }
}
//// CLASS ////

class Timeline extends Module {
    constructor(id) {
        super(id);

        this.currentCursorPos = "";
        this.currentProjState = "";

    }

    setup(callBack, cursorInfos) {
        this.update(callBack, cursorInfos);
    }

    update(callBack, cursorInfos) {
        let cursorPos = cursorInfos.layer + ' ' + cursorInfos.frm;
        let projState = cursorInfos.project_name + ' ' + cursorInfos.anim + ' ' +  cursorInfos.project_state_id;
        if (projState !== this.currentProjState) {
            this.updateTimeline(callBack, cursorInfos);
        } else if (cursorPos != this.currentCursorPos) {
            this.updateActive(callBack, cursorInfos);
        }
        else {
            callBack();
        }
        this.currentCursorPos = cursorPos;
        this.currentProjState = projState;
    }

    updateActive(callBack, cursorInfos) {
        /*
        Remove active class from frm-heading and layer-row.
        Set current layer and frm to active
        */
        this.elmt.querySelectorAll('.frms-row td')
        .forEach((e)=>setActiveElement('frm', cursorInfos.frm, e));
        this.elmt.querySelectorAll('.layer-row')
        .forEach((e)=>setActiveElement('layer', cursorInfos.layer, e));
        callBack();
    }

    updateTimeline(callBack, cursorInfos) {
        fetch('/view/get_timeline/', initOptions())
        .then(handleResponse)
        .then(json => {
            createTimeline(json, this.elmt);
            this.updateActive(callBack, cursorInfos);
        })
        .catch(handleError);
    }
}

/******************
**** STATUSBAR ****
******************/


//// UTILS ////

const updateInfos = (infos, statusbar) =>{
    const null_to_str = (a) => a === null ? "" : a
    statusbar.querySelectorAll('span')
    .forEach(e=>e.innerHTML = null_to_str(infos[e.id]))
}

//// CLASS ////

class CursorStatusbar extends Module {
    constructor(id) {
        super(id);
    }

    setup(callBack, cursorInfos){
        this.update(callBack, cursorInfos);
    }

    update(callBack, cursorInfos) {
        updateInfos(cursorInfos, this.elmt)
        callBack();
    }
}

class Statusbar extends Module {
    constructor(id, requestPath) {
        super(id);
        this.requestPath = requestPath;
        this.currentElementID = ""
        this.cache = {}
    }

    setup(callBack, cursorInfos){
        this.update(callBack, cursorInfos);
    }

    update(callBack, cursorInfos) {
        let cursorPos = cursorInfos.project_name+' '+cursorInfos.anim+' '+cursorInfos.layer+' '+cursorInfos.frm;
        let projectState = cursorInfos.project_state_id
        let elementID = cursorPos+' '+projectState;
        if(elementID != this.currentElementID){
            if(cursorPos in this.cache && this.cache[cursorPos].state_id == projectState){
                updateInfos(this.cache[cursorPos].infos, this.elmt);
                this.currentElementID = elementID;
                callBack();
            }
            else {
                fetch(this.requestPath, initOptions())
                .then(handleResponse)
                .then(json => {
                    updateInfos(json, this.elmt);
                    this.currentElementID = elementID;
                    this.cache[cursorPos]={state_id:projectState, infos:json}
                    callBack();

                })
                .catch(handleError);
            }
        } else {
            callBack();
        }
    }
}
