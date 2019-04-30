/****************
**** SETTINGS ***
****************/

const PRECISION = 3; // Min pixel length of a stroke

/****************
**** MODULES ****
****************/
let modules = [];
function callModulesMethod(modulesMethod) {
    modules.forEach(mo => {
        if(mo[modulesMethod]){
            mo[modulesMethod]();
        }
    });
}

class Module {
    constructor(id) {
        this.id = id;
        this.elmt = document.getElementById(id);
    }
}

/***************
**** CANVAS ****
***************/

//// EVENTS ////

const onCanvasMouseDown = (e) => {
    canvas.pMouseX = e.offsetX;
    canvas.pMouseY = e.offsetY;
}

const onCanvasMouseMove = (e) => {

    canvas.cursorPosX = e.offsetX;
    canvas.cursorPosY = e.offsetY;

    if(canvas.pMouseX){
        // send tool request only if the distance between mouse and pMouse is greater than PRECISION
        if(Math.abs(canvas.pMouseX - e.offsetX) > PRECISION || Math.abs(canvas.pMouseY - e.offsetY) > PRECISION) {
            let tool = document.getElementById('tool-selector').value
            if (tool == 'draw'){
                args = {coords:[canvas.pMouseX, canvas.pMouseY, e.offsetX, e.offsetY]};
            } else if (tool == 'erease'){
                args = {coords:[e.offsetX, e.offsetY]};
            }
            fetch('/control/drawer/'+tool+'/', initOptions(args))
            .then(()=>callModulesMethod('onDraw'))

            canvas.pMouseX = e.offsetX;
            canvas.pMouseY = e.offsetY;
        }
    }
}

const onMouseUp = (e) => {
    canvas.pMouseX = null;
    canvas.pMouseY = null;
}

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


const drawCursor = (x, y, ctx) => {
    // !!! UNUSED
        let raduis = 2;
      ctx.beginPath();
      ctx.arc(x, y, raduis, 0, 2 * Math.PI, false);
      ctx.fillStyle = 'black';
      ctx.fill();
      ctx.lineWidth = 1;
      ctx.strokeStyle = 'white';
      ctx.stroke();
}

const clearCanvas = (ctx, bgColor) => {
    ctx.fillStyle = bgColor;
    ctx.fillRect(
        0,
        0,
        ctx.canvas.clientWidth,
        ctx.canvas.clientHeight);
}

//// CLASS ////

class Canvas extends Module {

    constructor(id, noOnionSkin=false, onTopOfDefault=false) {
        super(id);
        this.onTopOfDefault = onTopOfDefault
        this.onAnimChange = this.onDraw = this.onCursorMove = noOnionSkin ? this.draw : this.update;
        this.responseHandler = handleResponse;
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

    setup() {

        this.ctx = this.elmt.getContext('2d');
        this.elmt.addEventListener('mousedown', onCanvasMouseDown);
        this.elmt.addEventListener('mousemove', onCanvasMouseMove);
        addEventListener('mouseup',   onMouseUp);

        // load config
        fetch('/view/get_view_config/', initOptions())
        .then(this.responseHandler)
        .then(json => this.loadConfig(json))
    }

    update() {
        /*
        Call draw or drawOnionSkin depending on playing info given by /view/get_cursor_infos/
        */
        console.log('update')
        fetch('/view/get_cursor_infos/', initOptions())
        .then(this.responseHandler)
        .then(json =>{
            if (json.playing) {
                this.draw()
            } else if (this.onTopOfDefault){
                this.drawOnionSkinWithDefault()
            } else {
                this.drawOnionSkin()
            }
        })
    }

    draw() {
        /*
        Draw lines given by /view/get_lines/ 
        */
        fetch('/view/get_lines/', initOptions())
        .then(this.responseHandler)
        .then(lines => {
            clearCanvas(this.ctx, this.backgroundColor);
            drawLines(lines, {lineWidth:this.lineWidth, lineColor:this.lineColor}, this.ctx);
            // drawCursor(this.cursorPosX, this.cursorPosY, this.ctx);
        });
    }

    drawOnionSkin() {
        /*
        Draw lines given by /view/get_onion_skin/""
        */
        fetch('/view/get_onion_skin/', initOptions({onion_range:[-1,0,1]}))
        .then(this.responseHandler)
        .then(onionSkin => {
            clearCanvas(this.ctx, this.backgroundColor);
            drawLines(onionSkin[-1], {lineWidth:this.onionWidth, lineColor:this.onionBwColor}, this.ctx);
            drawLines(onionSkin[1], {lineWidth:this.onionWidth, lineColor:this.onionFwColor}, this.ctx);
            drawLines(onionSkin[0], {lineWidth:this.lineWidth, lineColor:this.lineColor}, this.ctx);
            // drawCursor(this.cursorPosX, this.cursorPosY, this.ctx);
        });
    }

    drawOnionSkinWithDefault() {
        /*
        Draw lines given by /view/get_onion_skin/
        Also draw lines given by /view/get_lines/ with the default cursor
        */
        fetch('/view/get_lines/', initOptions({}, 'default'))
        .then(this.responseHandler)
        .then(lines => {
            clearCanvas(this.ctx, this.backgroundColor);
            drawLines(lines, {lineWidth:this.lineWidth, lineColor:'#0000CC'}, this.ctx);
            this.drawOnionSkin()
        });
    }
}


class CanvasOnTopOfDefault extends Canvas {
    /*
    Same as Canvas but ignore errors
    */
    constructor(id, noOnionSkin=false) {
        super(id, noOnionSkin);
        this.responseHandler = handleResponseQuiet;
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
    .then(()=>callModulesMethod('onAnimChange'))
    .then(()=>callModulesMethod('onCursorMove'))

};

//// CLASS ////

class Toolbar extends Module {
    constructor(id) {
        super(id);
    }

    setup() {
        this.elmt.querySelectorAll("button")
        .forEach(control=>control.addEventListener('click', onControlClick));
        this.elmt.querySelectorAll('#projectmanager button')
        .forEach(e=>e.addEventListener('click', ()=>callModulesMethod('setup')));
        

    }
}

/*****************
**** TIMELINE ****
*****************/

//// EVENTS ////

const onFrmClick = (e) => {
    let i = Number(e.currentTarget.dataset.frm);
    fetch('/control/navigator/go_to_frm/', initOptions({i:i}))
    .then(()=>callModulesMethod('onCursorMove'))
};

const onLayerClick = (e) => {
    let layer = Number(e.currentTarget.dataset.layer);
    fetch('/control/navigator/go_to_layer/', initOptions({i:layer}))
    .then(()=>callModulesMethod('onCursorMove'));
}

const onElementClick = (e) => {
    let i = Number(e.currentTarget.dataset.frm);
    let layer = Number(e.currentTarget.parentNode.dataset.layer);
    fetch('/control/navigator/go_to_frm/', initOptions({i:i}))
    .then(fetch('/control/navigator/go_to_layer/', initOptions({i:layer})))
    .then(()=>callModulesMethod('onCursorMove'));
}

//// CLASS ////

class Timeline extends Module {
    constructor(id) {
        super(id);
    }

    onCursorMove() {
        /*
        Remove active class from frm-heading and layer-row.
        Set current layer and frm to active
        */
        const setActiveElement = (dataname, i, element) => {
            if(element.dataset[dataname] == i){
                console.log(dataname, i)
                element.classList.add('active');
            } else {
                element.classList.remove('active');
            }
        }
        const setActiveAll = (cursor) => {
            this.elmt.querySelectorAll('.frms-row td')
            .forEach((e)=>setActiveElement('frm', cursor.frm, e));
            this.elmt.querySelectorAll('.layer-row')
            .forEach((e)=>setActiveElement('layer', cursor.layer, e));
        }
        fetch('/view/get_cursor_infos/',initOptions())
        .then(handleResponse)
        .then(json =>setActiveAll(json));
    }

    onAnimChange() {

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

        fetch('/view/get_timeline/', initOptions())
        .then(handleResponse)
        .then(json => createTimeline(json, this.elmt))
        .then(this.onCursorMove());
    }
}

/******************
**** STATUSBAR ****
******************/

//// CLASS ////

class Statusbar extends Module {
    constructor(id, requestPath) {
        super(id);
        this.requestPath = requestPath
        this.setup = this.onCursorMove
    }

    onCursorMove() {
        const updateInfos = (infos, statusbar) =>{
            const null_to_str = (a) => a === null ? "" : a
            statusbar.querySelectorAll('span')
            .forEach(e=>e.innerHTML = null_to_str(infos[e.id]))
        }
        fetch(this.requestPath, initOptions())
        .then(handleResponse)
        .then(json => updateInfos(json, this.elmt));
    }
}
