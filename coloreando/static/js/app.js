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
    stage.addEventListener('stagemousemove', function(e) {
      if (oldX) {
        draw(color, oldX, oldY, e.stageX, e.stageY);
      }
      /* Save event */
      saveEvent(color, oldX, oldY, e.stageX, e.stageY, dashboard_id);

      oldX = e.stageX;
      oldY = e.stageY;
    });
  });
  // need to get mouseup event working correctly...
  stage.update();

  replayEvents(dashboard_id);
});

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