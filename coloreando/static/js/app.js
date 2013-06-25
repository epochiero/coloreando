var stage, shape, oldX, oldY, size;

$(function() {
  stage = new createjs.Stage("dashboard-canvas");
  stage.enableDOMEvents = true;

  shape = new createjs.Shape();
  stage.addChild(shape);

  size = 3;

  stage.addEventListener('stagemousedown', function(e) {
    stage.addEventListener('stagemousemove', function(e) {
      if (oldX) {
        shape.graphics.beginStroke(color)
                      .setStrokeStyle(size, "round")
                      .moveTo(oldX, oldY)
                      .lineTo(e.stageX, e.stageY);
        stage.update();
      }
      
      /* Save event */
      saveEvent(color, oldX, oldY, e.stageX, e.stageY, dashboard_id);
      
      oldX = e.stageX;
      oldY = e.stageY;

    });
    stage.addEventListener('stagemouseup', function(e) {});
  });
  stage.update();
});

function saveEvent(color, oldX, oldY, newX, newY, dashboard_id) {
    endpoint = "/api/saveEvent";
    $.ajax({
      url: endpoint,
      method: "POST",
      headers: {'X-CSRFToken': $.cookie('csrftoken')},
      data: {'color': color, 'oldX': oldX, 'oldY': oldY, 'newX': newX, 'newY': newY, 'dashboard_id': dashboard_id},
      success: function() {}
    });
}

function replayEvents(dashboard_id) {
    endpoint = "/api/getEvents";
    $.ajax({
      url: endpoint,
      method: "POST",
      headers: {'X-CSRFToken': $.cookie('csrftoken')},
      data: {'dashboard_id': dashboard_id},
      success: function(data) {
        console.log(data);
        $.each(data.events, function(index, event) {
          event = JSON.parse(event);
          if (oldX) {
            shape.graphics.beginStroke(event.color)
                          .setStrokeStyle(size, "round")
                          .moveTo(event.oldX, event.oldY)
                          .lineTo(event.newX, event.newY);
            stage.update();
          }
          oldX = event.newX;
          oldY = event.newY;
        });
      }
    });
}

$(document).ready(function() {
  replayEvents(dashboard_id);
});
