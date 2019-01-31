const initOptions = (args) => {return{
    method: 'post',
    headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        cursor: cursor,
        args: args
    })
};}


let playing = false;
let cursor = 'default'

/****************
**** MODULES ****
****************/

class Module {
    constructor(id) {
        this.id = id;
        this.elmt = document.getElementById(id);
    }
}

const canvas    = new Module("canvas");
const timeline  = new Module("timeline");
const toolbar   = new Module("toolbar");
const statusbar = new Module("statusbar");

const modules = [canvas, timeline, toolbar, statusbar];
const callModulesMethod = me => {
    modules.forEach(mo => {
        if(mo[me]){
            mo[me]();
        }
    });
}

/***************
**** EVENTS ****
***************/

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

const onCanvasMouseDown = (e) => {
    canvas.pMouseX = e.offsetX;
    canvas.pMouseY = e.offsetY;
}

const onCanvasMouseMove = (e) => {
    if(canvas.pMouseX){
        let tool = document.getElementById('tool-selector').value
        fetch('/control/drawer/'+tool+'/', initOptions({
            x1:canvas.pMouseX,
            y1:canvas.pMouseY,
            x2:e.offsetX,
            y2:e.offsetY
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
/**************
**** SETUP ****
**************/

toolbar.setup = () => {
    document.querySelectorAll("#toolbar button")
    .forEach(control=>control.addEventListener('click', onControlClick));
}

canvas.setup = () => {
    canvas.ctx = canvas.elmt.getContext('2d');
    canvas.elmt.width  = 800;
    canvas.elmt.height = 600;
    // canvas.app = new PIXI.Application({view: canvas.elmt});
    // canvas.app.renderer.resize(800, 600);
    // canvas.app.renderer.backgroundColor = 0x222222;
    canvas.elmt.addEventListener('mousedown', onCanvasMouseDown);
    canvas.elmt.addEventListener('mousemove', onCanvasMouseMove);
    canvas.elmt.addEventListener('mouseup', onCanvasMouseUp);

}

/**************
**** UPDATE ****
**************/

canvas.onAnimChange = canvas.onDraw = canvas.onCursorMove = () => {
    /*
    Draw lines given by /view/get_lines/ 
    */
    const drawLines = (lines, style) => {
        canvas.ctx.lineWidth = style.lineWidth;
        canvas.ctx.strokeStyle = style.lineColor;
        canvas.ctx.beginPath();
        lines.forEach((line) => {
            canvas.ctx.moveTo(line[0], line[1]);
            canvas.ctx.lineTo(line[2], line[3]);
        });
        canvas.ctx.stroke();

    }
    const clearCanvas = () => {
        canvas.ctx.fillStyle = "#222222" ;
        canvas.ctx.fillRect(0,0,canvas.elmt.width,canvas.elmt.height);
    }
    fetch('/view/get_lines/', initOptions())
    .then(response => response.json())
    .then(lines => {
        if (playing) {
            clearCanvas();
            drawLines(lines, {lineWidth:2, lineColor:"#ffffff"});
        } else {
            fetch('/view/get_onion_skin/', initOptions())
            .then(response => response.json())
            .then(onionSkin => {
                clearCanvas();
                drawLines(onionSkin[-1], {lineWidth:1, lineColor:"#ff0000"});
                drawLines(onionSkin[1], {lineWidth:1, lineColor:"#00ff00"});
                drawLines(lines, {lineWidth:2, lineColor:"#ffffff"});
            });
        }
    });
};


timeline.onCursorMove = () => {
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
        document.querySelectorAll('.frms-row td')
        .forEach((e)=>setActiveElement('frm', cursor.frm, e));
        document.querySelectorAll('.layer-row')
        .forEach((e)=>setActiveElement('layer', cursor.layer, e));
    }
    fetch('/view/get_cursor_infos/',initOptions())
    .then(response => response.json())
    .then(json =>setActiveAll(json));
    
}

timeline.onAnimChange = () => {

    const createElement = (frm, element) => {
        let td = document.createElement("td");
        td.addEventListener('click', onElementClick);
        td.dataset.frm = frm;
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
    .then(json => createTimeline(json, timeline.elmt));
}

statusbar.onCursorMove = () => {

    const updateCursorInfos = (infos) =>{
        const null_to_str = (a) => a === null ? "" : a
        statusbar.elmt.querySelector('#playing').innerHTML = null_to_str(infos.playing);
        statusbar.elmt.querySelector('#loop').innerHTML = null_to_str(infos.loop);
        statusbar.elmt.querySelector('#project_name').innerHTML = null_to_str(infos.project_name);
        statusbar.elmt.querySelector('#frm_idx').innerHTML = null_to_str(infos.frm);
        statusbar.elmt.querySelector('#layer_idx').innerHTML = null_to_str(infos.layer);
        statusbar.elmt.querySelector('#anim_name').innerHTML = null_to_str(infos.anim);
    }
    fetch('/view/get_cursor_infos/', initOptions())
    .then(response => response.json())
    .then(json => updateCursorInfos(json));
}
     

///////////// SETUP
callModulesMethod('setup')
   
    
///////////// AUTOUPDATE
document.getElementById('play').addEventListener('click', autoUpdate)

function autoUpdate() {
    const fps = 24;
    fetch('/view/get_cursor_infos/', initOptions())
    .then(response=>response.json())
    .then(json=>{
        playing = json.playing;
        callModulesMethod('onCursorMove')
        if (playing){
            setTimeout(autoUpdate, 1000/fps);
        }
    });
}
