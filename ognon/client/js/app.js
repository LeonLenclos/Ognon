const url = new URL(window.location.href);
const FPS = 24// fps

class App {
    constructor(){
        this.clientId = undefined;
        this.cursor = url.searchParams.get("cursor") || 'default';
        this.modules = {};
        this.actions = {};

        let promises = [this.fetchClientId()];
        window.onload = () => {
            document.querySelectorAll('ogn-module').forEach((el)=>{
                promises.push(this.fetchModule(el));
            })
            Promise.all(promises)
            .then((res)=>this.startAutoUpdate())
            .catch(error=>this.handleError(error));
        }

        // Shortcuts
        this.shortcuts = shortcutsSets.std;
        this.keysPressed = new Set();

        window.addEventListener("keydown", e =>{
            if(e.target.localName == 'input') return;
            this.keysPressed.add(e.key)
            let repr = shortcutRepresentation(Array.from(this.keysPressed))
            console.log(repr)

            if(this.shortcuts[repr]){
                this.doAction(this.shortcuts[repr].action, this.shortcuts[repr].args);
                e.preventDefault();
            }
        }); 

        window.addEventListener("keyup", e =>{
            // Test : clear keyPressed on key Up
            this.keysPressed.clear();
            // keysPressed = keysPressed.filter(item => item != e.key);
        });

    }

    handleError(error, message){
        console.log(message || 'oups...', error);
    }

    selectCursor(cursor){
        console.log('cursor', cursor)
        this.cursor=cursor;
        this.fetchClientId()
        .catch(error=>this.handleError(error));
    }
    fetchClientId(){
        return post('/clients/new_client/', {cursor:this.cursor})
        .then(json=>{
            this.clientId = json;
        })
    }

    fetchModule(el){
        return get(el.getAttribute('src'))
        .then(html=>{
            el.innerHTML = html;
            this.modules[el.id] = new OgnModule(el, this);
            // resolve(666)
        })
    }

    update(){
        if(this.updateBusy) {console.log('update busy'); return;}
        this.updateBusy = true;
        post('/clients/whats_up/', {client_id:this.clientId})
        .then((viewInfos) => {
            // console.log(viewInfos)
            for(let id in this.modules){
                this.modules[id].update(viewInfos)
            }
            this.updateBusy = false;
        })
        .catch(error=>this.handleError(error));
    }

    autoUpdate(timestamp) {
        if (!this.autoUpdating) return;
        if(this.time == null) this.time=timestamp;
        let seg = Math.floor((timestamp - this.time)/(1000/FPS));
        if(seg > this.frame){
            this.frame = seg;
            this.update();
        }
        requestAnimationFrame(t=>this.autoUpdate(t));
    }

    startAutoUpdate(){
    if(!this.autoUpdating){
        this.time=null;
        this.frame=-1;
        this.autoUpdating = true;
        this.autoUpdate();
        }
    }

    stopAutoUpdate(){
        this.autoUpdating = false;
    }

    addAction(actionName, actionOptions){
        this.actions[actionName] = actionOptions
    }

    doAction(actionName, passedArgs){
        let action = this.actions[actionName];

        let completedArgs = {};
        let toBeCompletedArgs = {};
        for (let k in action.args) {
            if(action.args[k].hasOwnProperty('value')){
                completedArgs[k]=action.args[k].value;
            }
            else if(passedArgs.hasOwnProperty(k)){
                completedArgs[k]=passedArgs[k]
            }
            else {
                toBeCompletedArgs[k]=action.args[k];
            }
        }
        if (Object.keys(toBeCompletedArgs).length > 0) {
            console.log('open popup!')
            this.modules['inputpanel'].form.ask(action.description, toBeCompletedArgs, (args)=>this.doAction(actionName, args));
        }
        else {
            if(action.hasOwnProperty('serverCursorFunction')){
                post(action.serverCursorFunction, Object.assign(completedArgs, {cursor:this.cursor}))
                .catch((error)=>this.handleError(error));
            }
            else if(action.hasOwnProperty('serverFunction')){
                post(action.serverFunction, completedArgs)
                .catch((error)=>this.handleError(error));
            }
            else if(action.hasOwnProperty('clientFunction')){
                action.clientFunction(completedArgs);
            }
        }
    }
}



let app = new App();




