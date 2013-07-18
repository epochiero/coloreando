var stage, shape, oldX, oldY, size;
socket.emit('join_dashboard', {'dashboard_id': window.dashboard_id});

socket.on('draw_response', function(_event) {
  draw_event = JSON.parse(_event).event;
  draw(draw_event.color, draw_event.size, draw_event.shapeType, draw_event.oldX, draw_event.oldY, draw_event.newX, draw_event.newY);
  stage.update();
});


$(function() {
  stage = new createjs.Stage("dashboard-canvas");
  stage.enableDOMEvents = true;

  shape = new createjs.Shape();
  stage.addChild(shape);

  size = 3;
  shapeType = "round";

  stage.addEventListener('stagemousedown', function(e) {
    oldX = e.stageX;
    oldY = e.stageY;
    stage.addEventListener('stagemousemove', handleMouseMove);
  });
  stage.update();
  replayEvents(dashboard_id);
  stage.update();

  stage.addEventListener('stagemouseup', function(e) {
    stage.removeEventListener('stagemousemove', handleMouseMove);
  });

  $(".eraser").click(function() {
    size = 20;
    shapeType = "square";
    original_color = color;
    color = "#FFFFFF";
  });

  $(".pencil").click(function() {
    size = 3;
    shapeType = "round";
    color = original_color;
  });

  $("#color-selector-dashboard").minicolors({
    control: 'wheel',
    defaultValue: color,
    change: function(hex, opacity) {
        color = hex;
    }
  });

});

function handleMouseMove(e) {
  if (oldX) {
      draw(color, size, shapeType, oldX, oldY, e.stageX, e.stageY);
      stage.update();
  }
  /* Save event */
  saveEvent(color, size, shapeType, oldX, oldY, e.stageX, e.stageY, dashboard_id);

  oldX = e.stageX;
  oldY = e.stageY;
}

function saveEvent(color, size, shapeType, oldX, oldY, newX, newY, dashboard_id) {
  socket.emit('draw', {'color': color, 'size': size, 'shapeType': shapeType, 'oldX': oldX, 'oldY': oldY,
              'newX': newX, 'newY': newY, 'dashboard_id': dashboard_id});
}

function draw(color, size, shapeType, oldX, oldY, newX, newY) {
   shape.graphics.beginStroke(color)
                      .setStrokeStyle((color == "#FFFFFF" ? 20 : 3), (color=="#FFFFFF"?"square":"round"))
                      .moveTo(oldX, oldY)
                      .lineTo(newX, newY);
}

function replayEvents(dashboard_id) {
  socket.on('get_events_response', function(data){
    $.each(data.events, function(index, event) {        
        event = JSON.parse(event);
        if (oldX) {
          draw(event.color, event.size, event.shapeType, event.oldX, event.oldY, event.newX, event.newY);
          stage.update();
        }
        oldX = event.newX;
        oldY = event.newY;
      });
  });
  

  socket.emit('get_events', {'dashboard_id': dashboard_id});
}
