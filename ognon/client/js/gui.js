const PRECISION = 1; // Min pixel length of a stroke

class OgnModule {
    constructor(el, app){
        this.app = app;
        this.el = el;

        this.onUpdate = [];

        // Menu
        this.el.querySelectorAll('div[data-menu]').forEach(menu=>{
            for (let a in this.app.actions){
                if(this.app.actions[a].menu == menu.dataset.menu){
                    let button = document.createElement('button');
                    button.dataset.action = a;
                    button.classList.add('text-button');
                    menu.appendChild(button);
                }
            }
        });
    
        // Buttons
        this.buttons = []
        this.el.querySelectorAll('button[data-action]').forEach(button=>{
            this.buttons.push(new ActionButton(button, app));
        });

        // Status
        this.el.querySelectorAll('span[data-status]').forEach(status=>{
            let data = status.dataset.status.split('.')
            this.onUpdate.push((viewInfos)=>{
                if(viewInfos[data[0]]){
                    status.innerHTML = viewInfos[data[0]][data[1]]
                }
            })
        });

        // LightboxCanvas
        if(this.el.querySelector('#lightbox-canvas')){
            this.canvas = new LightboxCanvas(this.el.querySelector('#lightbox-canvas'), app);
            this.onUpdate.push((viewInfos)=>{
                // console.log('debug', viewInfos)
                if(viewInfos['config']){
                    this.canvas.updateConfig(viewInfos['config']);
                }
                if(viewInfos['drawing']){
                    this.canvas.updateDrawing(viewInfos['drawing']);
                    

                }
                if(this.canvas.drawCoords.length>=2){
                    this.canvas.drawLines([this.canvas.drawCoords], this.canvas.stylesOf('draft'))
                }
            })
        }

        // TimelineTable
        if(this.el.querySelector('#timeline-table')){
            this.table = new TimelineTable(this.el.querySelector('#timeline-table'), app);
            this.onUpdate.push((viewInfos)=>{
                if(viewInfos['timeline']){
                    this.table.updateTimeline(viewInfos['timeline'])
                }
                if (viewInfos['cursor_infos']) {
                    this.table.updateActive(viewInfos['cursor_infos'])
                }
            })
        }

        // InputpanelForm
        if(this.el.querySelector('#inputpanel-form')){
            this.form = new InputpanelForm(this.el.querySelector('#inputpanel-form'), app);
        }
    }

    update(viewInfos){

        this.onUpdate.forEach((f)=>f(viewInfos))
    }
}


class ActionButton {
    constructor(el, app){
        this.app = app;
        this.el = el;


        this.action = app.actions[el.dataset.action];
        this.args = this.el.dataset.args ? JSON.parse(this.el.dataset.args) : {};
        this.el.addEventListener('click', ()=>app.doAction(el.dataset.action, this.args));


        if(this.el.classList.contains('text-button')){
            this.el.innerHTML = this.action.text
        }
    }
}


class LightboxCanvas {
    constructor(el, app){
        this.app = app;
        this.el = el;

        this.drawCoords = [];

        this.ctx = this.el.getContext('2d', {alpha:false});

        this.el.addEventListener('mousedown', (e)=>this.onMouseDown(e.offsetX, e.offsetY));
        this.el.addEventListener('touchstart', (e)=>{
            let rect = e.target.getBoundingClientRect();
            let x = e.targetTouches[0].pageX - rect.left;
            let y = e.targetTouches[0].pageY - rect.top;
            this.onMouseDown(x, y)
            e.preventDefault();
        });

        this.el.addEventListener('mousemove', (e)=>this.onMouseMove(e.offsetX, e.offsetY));
        this.el.addEventListener('touchmove', (e)=>{

            let rect = e.target.getBoundingClientRect();
            let x = e.targetTouches[0].pageX - rect.left;
            let y = e.targetTouches[0].pageY - rect.top;

            this.onMouseMove(x, y)
            e.preventDefault();
        });

        addEventListener('mouseup', (e)=>this.onMouseUp());
        addEventListener('touchend', (e)=>this.onMouseUp());

        this.zoomReset();
        this.selectTool('draw');
    }


    updateConfig(config) {
        this.config = config;
        this.el.width = config.view.width;
        this.el.height = config.view.height;
    }

    stylesOf(lineType){
        return {
            lineWidth:Number(this.config.view[lineType+'_width']),
            lineColor:this.config.view[lineType+'_color'],
        };
    }

    updateDrawing(drawing) {
        let bgColor = this.config.view[drawing.playing?'background_color':'edit_background_color'];
        this.clear(bgColor);

        this.el.dataset.bwContrast = rgbToBwContrast(hexToRgb(bgColor))

        drawing.lines.forEach((line)=>{
            if(!line.line_type){
                this.drawLines(line.coords, this.stylesOf(drawing.playing?'line':'edit'))
            } else {
                line.line_type.forEach(lineType=>{
                this.drawLines(line.coords, this.stylesOf(lineType))
            })
            }
        });
    }

    callDrawer(){
        //callDrawer only if not busy and at least 2 points in coords
        if(this.callDrawerBusy || this.drawCoords.length<4){
            return false;
        }
        this.callDrawerBusy = true;
        post('/control/drawer/'+this.tool+'/',{
            cursor:this.app.cursor,
            coords:this.drawCoords
        })
        .then(()=>{this.callDrawerBusy=false;})
        .catch((error)=>app.handleError(error));
        return true;
    }

    onMouseDown(x, y){
        this.drawCoords = [x, y];
    }

    onMouseUp(){
        this.callDrawer();
        this.drawCoords = [];
    }

    onMouseMove(x, y){
        if(this.drawCoords.length < 2) return;
        let px = this.drawCoords[this.drawCoords.length-2];
        let py = this.drawCoords[this.drawCoords.length-1];
        // store coords only if the distance between mouse and pMouse is greater than PRECISION
        if(Math.abs(px - x) > PRECISION || Math.abs(py - y) > PRECISION) {    
            this.drawCoords.push(x, y);
            if(this.callDrawer()){
                this.drawCoords = [x, y];
            }
        }
    }
    drawLines(lines, style){
        this.ctx.strokeStyle = style.lineColor;
        this.ctx.lineWidth = style.lineWidth;
        this.ctx.lineJoin = "round";
        this.ctx.beginPath();
        this.ctx.moveTo(lines[0], lines[1]);
        for (var i=2; i<lines.length; i+=2) this.ctx.lineTo(lines[i], lines[i+1]);
        this.ctx.stroke();
    }

    clear(bgColor){
        this.ctx.fillStyle = bgColor;
        this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
    }

    selectTool(tool){
        this.tool = tool;
        this.el.dataset.tool = tool
    }
    
    scale(value){
        this.el.style.transform='scale('+value+')';
    }

    zoomIn(){
        this.zoom += 0.1;
        this.scale(this.zoom)
    }

    zoomOut(){
        this.zoom -= 0.1;
        this.zoom = this.zoom > 0 ? this.zoom : 0.1;
        this.scale(this.zoom)
    }

    zoomReset(){
        this.zoom = 1;
        this.scale(this.zoom)
    }
}


class InputpanelForm {
    constructor(el, app){
        this.el = el;
        this.app = app;
        this.heading = this.el.querySelector('h2');
        this.inputContainer = this.el.querySelector('.input-container');
        this.el.querySelector('button[name=ok]')
        .addEventListener('click', ()=>this.ok());
        this.el.querySelector('button[name=cancel]')
        .addEventListener('click', ()=>this.close());
        this.close();
    }

    ask(title, fields, callback){
        this.el.style.display= 'flex';

        this.callback = callback;
        this.heading.innerHTML = title;
    
        this.inputs={}

        for (let field in fields) {
            let fieldDiv = document.createElement('div')
            let label = document.createElement('label');
            label.innerHTML = fields[field].description;

            this.inputs[field] = document.createElement('input');

            fieldDiv.appendChild(label);
            fieldDiv.appendChild(this.inputs[field]);



            if(fields[field].suggestionListFromServer){
                let select = document.createElement('select');
                select.appendChild(document.createElement('option'))
                select.addEventListener('change',(e)=>{this.inputs[field].value=e.target.value; console.log(e.target)})
                fieldDiv.appendChild(select);

                // populate
                post(fields[field].suggestionListFromServer, {cursor:app.cursor})
                .then(list=>{
                    list.forEach((item)=>{
                        let option = document.createElement('option');
                        option.value = item;
                        option.text = item;
                        select.appendChild(option);
                    })
                })
            }


            this.inputContainer.appendChild(fieldDiv);
        }
    }

    close() {
        this.inputContainer.innerHTML = '';
        this.heading.innerHTML = '';
        this.el.style.display= 'none';
    }

    ok() {
        let args = {};
        for (let field in this.inputs) {
            args[field] = this.inputs[field].value;
        }

        this.callback && this.callback(args);
        this.close();
    }
}


class TimelineTable {
    constructor(el, app) {
        this.app = app;
        this.el = el;
    }

    updateActive(cursorInfos) {
        /*
        Remove active class from frm-heading and layer-row.
        Set current layer and frm to active
        */
        this.el.querySelectorAll('.frms-row td')
        .forEach((e)=>this.setActiveElement('frm', cursorInfos.frm, e));
        this.el.querySelectorAll('.layer-row')
        .forEach((e)=>this.setActiveElement('layer', cursorInfos.layer, e));
        this.currentCursorPos = cursorInfos;
    }

    updateTimeline(timeline) {
        console.log('updateTimeline', timeline)
        this.createTimeline(timeline, this.el);
    }

    onFrmClick(e) {
        let i = Number(e.currentTarget.dataset.frm);
        post('/control/navigator/go_to_frm/', {cursor:this.app.cursor, i:i})
        .catch(app.handleError);
    }

    onLayerClick(e) {
        let layer = Number(e.currentTarget.dataset.layer);
        post('/control/navigator/go_to_layer/', {cursor:this.app.cursor, i:layer})
        .catch(app.handleError);
    }

    onElementClick(e) {
        let i = Number(e.currentTarget.dataset.frm);
        let layer = Number(e.currentTarget.parentNode.dataset.layer);
        post('/control/navigator/go_to_frm/', {cursor:this.app.cursor, i:i})
        .catch(app.handleError);
        post('/control/navigator/go_to_layer/', {cursor:this.app.cursor, i:layer})
        .catch(app.handleError);
    }

    createElement(frm, element) {
        let td = document.createElement("td");
        td.addEventListener('click', (e)=>this.onElementClick(e));
        td.dataset.frm = frm;
        td.dataset.type = element.type;
        if(element.name) td.dataset.name = element.name;
        td.dataset.tags = element.tags;
        td.setAttribute("colspan", element.len);
        return td;
    }

    createLayerHead() {
        let td = document.createElement("td");
        td.addEventListener('click', (e)=>this.onLayerClick(e));
        return td;
    }
    createFrmHead(i) {
        let td = document.createElement("td");
        td.addEventListener('click', (e)=>this.onFrmClick(e));
        td.dataset.frm = i;
        return td;
    }

    createLayerRow(i, elements) {
        let tdArray = [this.createLayerHead()];
        let frm = 0;
        for (let j = 0; j < elements.length; j++) {
            tdArray.push(this.createElement(frm, elements[j]));
            frm+=elements[j].len;
        }
        let layerRow = document.createElement("tr");
        layerRow.classList.add('layer-row')
        layerRow.dataset.layer = i;
        tdArray.forEach(td=>layerRow.appendChild(td));
        return layerRow;
    }

    createFrmsRow(len) {
        let tdArray = [this.createLayerHead()];
        for (let i = 0; i < len; i++) {
            tdArray.push(this.createFrmHead(i));
        }
        let frmsRow = document.createElement("tr");
        frmsRow.classList.add('frms-row');
        tdArray.forEach(td=>frmsRow.appendChild(td));
        return frmsRow;
    }

    createTimeline(timeline, table) {
        while(table.firstChild && table.removeChild(table.firstChild)); //empty
        table.appendChild(this.createFrmsRow(timeline.len));
        for (var i = 0; i < timeline.layers.length; i++) {
            table.appendChild(this.createLayerRow(i, timeline.layers[i]));
        }
    }

    setActiveElement(dataname, i, element) {
        if(element.dataset[dataname] == i){
            element.classList.add('active');
        } else {
            element.classList.remove('active');
        }
    }
}