/****************
**** MODULES ****
****************/

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
    if(canvas.pMouseX){
        let tool = document.getElementById('tool-selector').value
        fetch('/control/drawer/'+tool+'/', initOptions({
            coords:[canvas.pMouseX, canvas.pMouseY, e.offsetX, e.offsetY]
        }))
        .then(()=>callModulesMethod('onDraw'))
        canvas.pMouseX = e.offsetX;
        canvas.pMouseY = e.offsetY;
    }
}

const onCanvasMouseUp = (e) => {
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
const clearCanvas = (ctx) => {
    ctx.fillStyle = "#222222" ;
    ctx.fillRect(
        0,
        0,
        ctx.canvas.clientWidth,
        ctx.canvas.clientHeight);
}

//// CLASS ////

class Canvas extends Module {

    constructor(id, noOnionSkin=false) {
        super(id);
        this.onAnimChange = this.onDraw = this.onCursorMove = noOnionSkin ? this.draw : this.update
    }

    setup() {
        this.ctx = this.elmt.getContext('2d');
        this.elmt.width  = 800;
        this.elmt.height = 600;
        this.elmt.addEventListener('mousedown', onCanvasMouseDown);
        this.elmt.addEventListener('mousemove', onCanvasMouseMove);
        this.elmt.addEventListener('mouseup',   onCanvasMouseUp);
    }

    update() {
        /*
        Call draw or drawOnionSkin depending on playing info given by /view/get_cursor_infos/
        */
        fetch('/view/get_cursor_infos/', initOptions())
        .then(response => response.json())
        .then(json =>{
            if (json.playing) {
                this.draw()
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
        .then(response => response.json())
        .then(lines => {
            clearCanvas(this.ctx);
            drawLines(lines, {lineWidth:2, lineColor:"#ffffff"}, this.ctx);
        });
    }

    drawOnionSkin() {
        /*
        Draw lines given by /view/get_lines/ and /view/get_onion_skin/""
        */
        fetch('/view/get_onion_skin/', initOptions({onion_range:[-1,0,1]}))
        .then(response => response.json())
        .then(onionSkin => {
            clearCanvas(this.ctx);
            drawLines(onionSkin[-1], {lineWidth:1, lineColor:"#ff0000"}, this.ctx);
            drawLines(onionSkin[1], {lineWidth:1, lineColor:"#00ff00"}, this.ctx);
            drawLines(onionSkin[0], {lineWidth:2, lineColor:"#ffffff"}, this.ctx);
        });
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
    .then(()=>callModulesMethod('onAnimChange'))
    .then(()=>callModulesMethod('onCursorMove'));
}

//// CLASS ////

class Toolbar extends Module {
    constructor(id) {
        super(id);
    }

    setup() {
        this.elmt.querySelectorAll("button")
        .forEach(control=>control.addEventListener('click', onControlClick));
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
        .then(response => response.json())
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
        .then(response => response.json())
        .then(json => createTimeline(json, this.elmt));
    }
}

/******************
**** STATUSBAR ****
******************/

//// CLASS ////

class Statusbar extends Module {
    constructor(id) {
        super(id);
    }

    onCursorMove() {

        const updateCursorInfos = (infos, statusbar) =>{
            const null_to_str = (a) => a === null ? "" : a
            statusbar.querySelector('#playing').innerHTML = null_to_str(infos.playing);
            statusbar.querySelector('#loop').innerHTML = null_to_str(infos.loop);
            statusbar.querySelector('#project_name').innerHTML = null_to_str(infos.project_name);
            statusbar.querySelector('#frm_idx').innerHTML = null_to_str(infos.frm);
            statusbar.querySelector('#layer_idx').innerHTML = null_to_str(infos.layer);
            statusbar.querySelector('#anim_name').innerHTML = null_to_str(infos.anim);
        }
        fetch('/view/get_cursor_infos/', initOptions())
        .then(response => response.json())
        .then(json => updateCursorInfos(json, this.elmt));
    }
}
