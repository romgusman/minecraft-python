from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import *
app = Ursina()
player = FirstPersonController()
Sky()
texture = ['ground.png', 'grass.png']
boxes = []
for i in range(50):
  for j in range(50):
    box = Button(color=color.white, model='cube', position=(j,0,i),
          texture=texture[randint(0,1)], parent=scene, origin_y=0.5)
    boxes.append(box)

def input(key):
  for box in boxes:
    if box.hovered:
      if key == 'left mouse down':
        new = Button(color=color.white, model='cube', position=box.position + mouse.normal,
                    texture='grass.png', parent=scene, origin_y=0.5)
        boxes.append(new)
      if key == 'right mouse down':
        boxes.remove(box)
        destroy(box)

app.run()