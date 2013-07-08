var stage, shape, oldX, oldY, size;
var socket = io.connect('/coloreando');
socket.on('draw_response', function(_event) {
  draw_event = JSON.parse(_event).event;
  draw(draw_event.color, draw_event.oldX, draw_event.oldY, draw_event.newX, draw_event.newY);
});

socket.on('get_buddies_response', function(message){console.log(message);});

$(function() {
  stage = new createjs.Stage("dashboard-canvas");
  stage.enableDOMEvents = true;

  shape = new createjs.Shape();
  stage.addChild(shape);

  size = 3;

  stage.addEventListener('stagemousedown', function(e) {
    oldX = e.stageX;
    oldY = e.stageY;
    stage.addEventListener('stagemousemove', handleMouseMove);
  });
  stage.update();
  replayEvents(dashboard_id);

  stage.addEventListener('stagemouseup', function(e) {
    stage.removeEventListener('stagemousemove', handleMouseMove);
  });
});

function handleMouseMove(e) {
  if (oldX) {
    draw(color, oldX, oldY, e.stageX, e.stageY);
  }
  /* Save event */
  saveEvent(color, oldX, oldY, e.stageX, e.stageY, dashboard_id);

  oldX = e.stageX;
  oldY = e.stageY;
}

function saveEvent(color, oldX, oldY, newX, newY, dashboard_id) {
  socket.emit('draw', {'color': color, 'oldX': oldX, 'oldY': oldY,
              'newX': newX, 'newY': newY, 'dashboard_id': dashboard_id});
}

function draw(color, oldX, oldY, newX, newY) {
   shape.graphics.beginStroke(color)
                      .setStrokeStyle(size, "round")
                      .moveTo(oldX, oldY)
                      .lineTo(newX, newY);
   stage.update();
}

function replayEvents(dashboard_id) {
  socket.on('get_events_response', function(data){
    $.each(data.events, function(index, event) {
        event = JSON.parse(event);
        if (oldX) {
          draw(color, oldX, oldY, event.newX, event.newY);
        }
        oldX = event.newX;
        oldY = event.newY;
      });
  });

  socket.emit('get_events', {'dashboard_id': dashboard_id});
}