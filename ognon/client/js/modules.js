/*
* This file defines the modules.
*/


/****************
**** SETTINGS ***
****************/

const PRECISION = 1; // Min pixel length of a stroke

/****************
**** MODULES ****
****************/

class Module {
    constructor(id) {
        this.id = id;
        this.elmt = document.getElementById(id); 
        this.busy = false;
        this.request = {};
    }

    add_request(request) {
        this.request = Object.assign(this.request, request)
    }

    reset_request(){
        this.request = {}
    }
}

/***************
**** CANVAS ****
***************/

//// EVENTS ////


let mouseDownCoords = [];
let onCallDrawerBusy = false;


const callDrawer = () => {
    //callDrawer only if not busy and at least 2 points in coords
    if(onCallDrawerBusy || mouseDownCoords.length<4){
        return false;
    }
    onCallDrawerBusy = true;
    let tool = document.getElementById('tool-selector').value
    let args = {coords:[]};
    args.coords = mouseDownCoords;
    fetch('/control/drawer/'+tool+'/', initOptions(args))
    .then(()=>{onCallDrawerBusy = false;})
    .catch(handleError);
    return true;
};

const onCanvasMouseDown = (e) => {
    mouseDownCoords = [e.offsetX, e.offsetY];
};

const onMouseUp = (e) => {

    callDrawer();
    mouseDownCoords = [];
    

};

const onCanvasMouseMove = (e) => {

    if(mouseDownCoords.length < 2) return;

    let x = e.offsetX;
    let y = e.offsetY;
    let px = mouseDownCoords[mouseDownCoords.length-2];
    let py = mouseDownCoords[mouseDownCoords.length-1];




    // store coords only if the distance between mouse and pMouse is greater than PRECISION
    if(Math.abs(px - x) > PRECISION || Math.abs(py - y) > PRECISION) {
    
        mouseDownCoords = mouseDownCoords.concat([x, y]);

        if(callDrawer()){
            mouseDownCoords = [x, y];
        }
        else {
            console.log("busy : onCanvasMouseMove")
        }


    }
};

// const useCurrentTool(x1, y1, x2, y2)
//// UTILS ////

const drawLines = (lines, style, ctx) => {
    ctx.lineWidth = style.lineWidth;
    ctx.strokeStyle = style.lineColor;
    ctx.beginPath();
    for (var i=0; i<lines.length; i++) {
        ctx.moveTo(lines[i][0], lines[i][1]);
        for (var j=2; j<lines[i].length; j+=2) {
            ctx.lineTo(lines[i][j], lines[i][j+1]);
        }

    }
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

    setup(viewInfos) {

        this.ctx = this.elmt.getContext('2d');
        this.elmt.addEventListener('mousedown', onCanvasMouseDown);
        this.elmt.addEventListener('mousemove', onCanvasMouseMove);
        addEventListener('mouseup',   onMouseUp);

        this.updateConfig = true
        this.update(viewInfos);
    }

    update(viewInfos) {
        /*
        Call draw or drawOnionSkin depending on playing info given by /view/get_cursor_infos/
        */
        this.reset_request();

        if(viewInfos['get_view_config']){
            this.loadConfig(viewInfos['get_view_config']);
            this.updateConfig = false;
        } else if (this.updateConfig) {
            this.add_request({'get_view_config':{}})
        }

        if (viewInfos['get_cursor_infos'].playing || this.noOnionSkin) {
            this.draw(viewInfos, [0], false)
        } else {
            this.draw(viewInfos, [-1, 0, 1], true)
        }

        if(mouseDownCoords.length>=2){
            drawLines([mouseDownCoords],{lineWidth:this.lineWidth, lineColor:'#00CCCC'},this.ctx)
        } // DONT WORK ?

        this.updating = false; // useless ??
    }

    draw(viewInfos, onionRange=[0], draft=false) {
        /*
        Draw lines given by /view/get_onion_skin/ 
        */
        let c = viewInfos['get_cursor_infos']

        let cursorPos = c.project_name + ' ' + c.anim + ' ' +  c.layer + ' ' + c.frm;
        let projState = c.project_state_id + ' '  + c.project_draw_state_id;
        let imageID = cursorPos + ' ' + projState + ' '  + onionRange;



        if (this.currentImageID == imageID)
        {
            return;
        }
        else if (cursorPos in this.cache 
                && this.cache[cursorPos].onionRange == onionRange.join()
                && this.cache[cursorPos].draft == draft
                && this.cache[cursorPos].state_id == projState)
        {

            this.ctx.drawImage(this.cache[cursorPos].canvas,0,0);
            this.currentImageID = imageID

        }
        else
        {           

            this.add_request({'get_onion_skin':{
                onion_range:onionRange
            }});

            if (!viewInfos['get_onion_skin']) {
                return;
            }

            if(draft){
                this.add_request({'get_lines':{
                    draft:true
                }});
                if (viewInfos['get_lines']==undefined) {
                    return;
                }

            }
            clearCanvas(this.ctx, this.backgroundColor);

            if (draft) {
                let draftLines = viewInfos['get_lines']
                this.drawDraft(draftLines);
            }

            let onionSkin = viewInfos['get_onion_skin']
            this.drawSkins(onionSkin, onionRange);

            let cacheCanvas = document.createElement('canvas');
            cacheCanvas.width = this.elmt.width;
            cacheCanvas.height = this.elmt.height;
            cacheCanvas.getContext('2d').drawImage(this.elmt,0,0);
            this.cache[cursorPos] = {
                state_id:projState,
                onionRange:onionRange.join(),
                draft:draft,
                canvas:cacheCanvas
            };
            this.currentImageID = imageID
        }
    }

    getCol(skin){
        if(skin < 0){
            return this.onionBwColor;
        } else if (skin > 0) {
            return this.onionFwColor;
        } else{
            return this.lineColor;
        }
    }

    drawDraft(draftLines) {
        drawLines(draftLines, {lineWidth:this.lineWidth, lineColor:'#0000CC'}, this.ctx);
    }

    drawSkin(skins, i) {
        drawLines(skins[i], {lineWidth:this.lineWidth, lineColor:this.getCol(i)}, this.ctx);
    }

    drawSkins(skins, range) {
        range.filter(e=>e!=0).forEach(i=>{
            this.drawSkin(skins, i);
        });
        this.drawSkin(skins, 0);
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

const onCustomOptionSelectChange = (e) => {
    let el = e.currentTarget;
    if(el.options[el.selectedIndex].value=='customOption'){
        el.nextSibling.disabled=false;
        el.nextSibling.focus();
        el.nextSibling.style.display='inline';
        el.nextSibling.value = '';
    } else{
        el.nextSibling.disabled=true;
        el.nextSibling.value = el.value;
        el.nextSibling.style.display='none';
    }
}

//// UTILS ////

const updateCustomOptionSelect = (infos, e, listFrom) => {
    e.querySelectorAll('[data-list-from='+listFrom+']')
    .forEach(e=>{
        while (e.firstChild) {
            e.removeChild(e.firstChild);
        }
        let new_opt = document.createElement('option');  
        new_opt.value = 'customOption'
        new_opt.innerHTML = '[new]';
        e.appendChild(new_opt);

        infos[listFrom].forEach((opt_name)=>{
            let opt = document.createElement('option');  
            opt.value = opt_name
            opt.innerHTML = opt_name;
            e.appendChild(opt);
        })
    })
}

//// CLASS ////

class Toolbar extends Module {
    constructor(id) {
        super(id);
    }

    setup(viewInfos) {
        this.elmt.querySelectorAll(".customOptionSelect")
        .forEach(e=>e.addEventListener('change', onCustomOptionSelectChange));

        this.elmt.querySelectorAll("button")
        .forEach(control=>control.addEventListener('click', onControlClick));

        this.elmt.querySelectorAll('#projectmanager button')
        .forEach(e=>e.addEventListener('click', ()=>callModulesMethod('setup')));
    }

    update(viewInfos) {
        this.reset_request();

        let c = viewInfos['get_cursor_infos'];

        let projectState = c.project_state_id;

        if(projectState != this.projectState){

            if (!viewInfos['get_projects'] || !viewInfos['get_anims']) {
                this.add_request({'get_projects':{}})
                this.add_request({'get_anims':{}})
                return;
            }


            updateCustomOptionSelect(viewInfos, this.elmt, 'get_projects');
            updateCustomOptionSelect(viewInfos, this.elmt, 'get_anims');
            this.projectState = projectState;
        }
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

    setup(viewInfos) {
        this.update(viewInfos);
    }

    update(viewInfos) {
        this.reset_request();

        let c = viewInfos['get_cursor_infos']
        let cursorPos = c.layer + ' ' + c.frm;
        let projState = c.project_name + ' ' + c.anim + ' ' +  c.project_state_id;

        if (projState !== this.currentProjState) {
            this.add_request({'get_timeline':{}});
            this.updateTimeline(viewInfos, cursorPos, projState);
        } else if (cursorPos != this.currentCursorPos) {
            this.updateActive(viewInfos);
        }
        else {

        }
    }

    updateActive(viewInfos, cursorPos) {
        /*
        Remove active class from frm-heading and layer-row.
        Set current layer and frm to active
        */
        let c = viewInfos['get_cursor_infos']

        this.elmt.querySelectorAll('.frms-row td')
        .forEach((e)=>setActiveElement('frm', c.frm, e));
        this.elmt.querySelectorAll('.layer-row')
        .forEach((e)=>setActiveElement('layer', c.layer, e));
        this.currentCursorPos = cursorPos;
    }

    updateTimeline(viewInfos, cursorPos, projState) {
        if (!viewInfos['get_timeline']) {
            return;
        }
        createTimeline(viewInfos['get_timeline'], this.elmt);
        this.updateActive(viewInfos);
        this.currentProjState = projState;

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

    setup(viewInfos){
        this.update(viewInfos);
    }

    update(viewInfos) {
        updateInfos(viewInfos['get_cursor_infos'], this.elmt)
    }
}

class Statusbar extends Module {
    constructor(id, view_function) {
        super(id);
        this.view_function = view_function;
        this.currentElementID = ""
        this.cache = {}
    }

    setup(viewInfos){
        this.update(viewInfos);
    }

    update(viewInfos) {
        this.reset_request();

        let c = viewInfos['get_cursor_infos'];

        let cursorPos = c.project_name+' '+c.anim+' '+c.layer+' '+c.frm;
        let projectState = c.project_state_id;
        let elementID = cursorPos+' '+projectState;

        if(elementID != this.currentElementID){
            if(cursorPos in this.cache && this.cache[cursorPos].state_id == projectState){
                updateInfos(this.cache[cursorPos].infos, this.elmt);
                this.currentElementID = elementID;
            }
            else {
                if (!viewInfos[this.view_function]) {
                    let req = {}; req[this.view_function] = {};
                    this.add_request(req)
                    return;
                }
                let infos = viewInfos[this.view_function]

                updateInfos(infos, this.elmt);
                this.currentElementID = elementID;
                this.cache[cursorPos]={state_id:projectState, infos:infos}
            }
        }
    }
}
