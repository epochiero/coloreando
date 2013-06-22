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
      oldX = e.stageX;
      oldY = e.stageY;
    });
  });
  stage.update();
});