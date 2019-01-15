
    let cursor_idx = 0;


$(document).ready(()=>{

    // Dom.
    let $controlButtons = $("#control button");
    let $projectButtons = $("#project button");
    let $timeline = $("#timeline");
    let $display = $("#display")

    // App vars.
    let pixiApp = new PIXI.Application({view: $display[0]});
    let playing = false;
    ///// Callbacks

    // To be called on loading page
    function setup(data) {
        setupDisplay(data.config)
        update(data);
    }
    
    // To be called on update
    function update(data) {
        if (data.cursor.playing != playing) updateOnPlay(data);
        playing = data.cursor.playing;
        if (playing) updateOnPlaying(data);
        else updateOnEditing(data);
    }

    function updateOnPlay(data) {
        updateToolbar(data.anims, data.cursor, data.cursors);
    }

    function updateOnPlaying(data) {
        updateDisplay(data.lines);
        updateStatusbar(data.cursor);
        updateTimelineOnPlaying();
        fps = data.config.gui.on_play_fps;
        setTimeout(()=>{
            post({cursor_idx:cursor_idx}, setup)}, 1000/fps);
    }

    function updateOnEditing(data) {
        updateDisplay(data.lines);
        updateTimeline(data.timeline, data.cursor);
        updateToolbar(data.anims, data.cursor, data.cursors);
        updateStatusbar(data.cursor);
    }

    ///// Post function
    function post(jsonMsg, callback) {
        callback = callback || update;        
        $.ajax({
            type: "POST",
            url: '/' + PROJECT,
            data: JSON.stringify(jsonMsg),
            contentType: "application/json; charset=utf-8",
            dataType: "text",
            success: (data)=>{
                jsondata = $.parseJSON(data);
                callback(jsondata)
            },
            failure: (err)=>{
                console.err(err);
            }
        });
    }

    // First post.
    post({cursor_idx:cursor_idx}, setup);

    /////////////////////////////
    /////////////////////////////
    /////////////////////////////
    ////////// TOOLBAR //////////
    /////////////////////////////
    /////////////////////////////
    /////////////////////////////

    ///// Events

    $controlButtons.click((e)=>{
        // Create a control request with elements id.
        let request = {
            method:'control',
            controller:e.currentTarget.parentElement.id,
            controller_method:e.currentTarget.id,
            cursor_idx:cursor_idx
        };
        // Add required args.

        if($(e.currentTarget).data("required")) {
            let required = $(e.currentTarget).data("required").split(" ");
            for (var i = 0; i < required.length; i++) {
                let value = $(e.currentTarget.parentElement)
                            .find('input[name=' + required[i] + ']')
                            .val()
                request[required[i]] = value;
            }
        }
        // Post.
        post(request, update);
    });

    $projectButtons.click((e)=>{
        // Post a request with elements id.
        let method = e.currentTarget.id;
        let request = {
            method:method,
            cursor_idx:cursor_idx
        };
        post(request, update);
    });

    $("#cursors").change(()=>{
        cursor_idx = Number($("#cursors").val()) ;
    })
    ///// Update function

    function updateToolbar(anims, cursor, cursors) {
        // Disable some controls on playing
        $('#animsmanager button').prop('disabled', cursor.playing);
        $('#organizer button').prop('disabled', cursor.playing);
        $('#drawer button').prop('disabled', cursor.playing);
        // Make the play button active on playing
        if (cursor.playing) {
            $('#play').addClass("active");
        } else {
            $('#play').removeClass("active");
        }
        // Fill the cursor select
        $("#cursors").empty();
        for (var i = 0; i < cursors; i++) {
            $("#cursors").append($("<option>").val(i).text(i));
        }
        $("#cursors").val(cursor_idx);


    }

    function updateStatusbar(cursor) {
        let null_to_str = (a) => {return a === null ? "" : a}
        $('.statusbar #cursor_idx').text(null_to_str(cursor_idx));
        $('.statusbar #frm_idx').text(null_to_str(cursor.frm_idx));
        $('.statusbar #layer_idx').text(null_to_str(cursor.layer_idx));
        $('.statusbar #anim_name').text(null_to_str(cursor.anim_name));

    }
    //////////////////////////////
    //////////////////////////////
    //////////////////////////////
    ////////// TIMELINE //////////
    //////////////////////////////
    //////////////////////////////
    //////////////////////////////

    ///// Update function

    function updateTimeline(timeline, cursor) {
        // Clear.
        $timeline.empty();
        // Create heading.
        let tr = $("<tr>", {class:'timeline-heading'});
        tr.append($("<th>").addClass('layer'));
        for (var i = 0; i < timeline.len; i++) {
            let th = $("<th>");
            th.click(()=>{post({
                method:'control',
                controller:'navigator',
                controller_method:'go_to_frm'
                cursor_idx:cursor_idx,
                i:i
            })}) //////////////////WORKING HERE
            if(cursor.frm_idx == i)
                th.addClass("active");
            tr.append(th);
        }
        $timeline.append(tr);
        // Create rows.
        for (var i = 0; i < timeline.elmnts.length; i++) {
            let tr = $("<tr>");
            tr.append($("<td>").addClass('layer'));
            if(cursor.layer_idx == i)
                tr.addClass("active");
            // Create cells.
            for (var j = 0; j < timeline.elmnts[i].length; j++) {
                let td = $("<td>", {
                    colspan:timeline.elmnts[i][j].len,
                    class:timeline.elmnts[i][j].type
                });
                tr.append(td);
            }
            $timeline.append(tr);
        }
    }

    function updateTimelineOnPlaying(timeline, cursor) {
        // Clear.
        $timeline.html('playing');
    }

    /////////////////////////////
    /////////////////////////////
    /////////////////////////////
    ////////// DYSPLAY //////////
    /////////////////////////////
    /////////////////////////////
    /////////////////////////////


    ///// Events

    $display.on('mousedown', (event) => {
        // Create a mousemove handler on mousedown.
        $display.on('mousemove', (event) => {
            // Post a start_line.
            post({
                method:'control',
                controller:'drawer',
                controller_method:'start_line',
                cursor_idx:cursor_idx,
                x:event.offsetX,
                y:event.offsetY
            }, update);
        });
    });

    $display.on('mouseup', (event) => {
        // Stop the mousemove handler on mouseup and post an end_line.
        $display.off('mousemove')
        post({
            method:'control',
            controller:'drawer',
            controller_method:'end_line',
            cursor_idx:cursor_idx,
        }, update)
    });

    ///// Update function

    function setupDisplay(config) {
        pixiApp.renderer.resize(config.display.width, config.display.height);
        pixiApp.renderer.backgroundColor = parseInt(config.display.background_color, 16);
        pixiApp.renderer.lineWidth = Number(config.display.line_width);
        pixiApp.renderer.lineColor = parseInt(config.display.line_color, 16);
    }

    function updateDisplay(lines) {
        // Helper function to create lines.
        function createLine(line,) {
            // PIXI.Graphics has an interactive mode.
            // May be better than the current eraser ???
            // see : pixijs.download/release/docs/PIXI.Graphics.html#interactive
            let l = new PIXI.Graphics()
            .lineStyle(pixiApp.renderer.lineWidth, pixiApp.renderer.lineColor)
            .moveTo(line[0].x, line[0].y);
            for (var i = 1; i < line.length; i++){
                l.lineTo(line[i].x, line[i].y);
            }
            return l;
        }
        // Clear.
        pixiApp.stage.removeChildren();
        // Create lines.
        for (var i = 0; i < lines.length; i++) {
            pixiApp.stage.addChild(createLine(lines[i]));
        }
    }
});
