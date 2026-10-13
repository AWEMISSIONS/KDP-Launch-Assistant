from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
from pathlib import Path
import math

OUT=Path('dist/books/machine-draw'); OUT.mkdir(parents=True,exist_ok=True)
W,H=612,792
NAVY=HexColor('#173447'); TEAL=HexColor('#0D7580'); ORANGE=HexColor('#E39C28'); GRAY=HexColor('#647780')
projects=[
('Dump truck','A dump bed tips to unload gravel.','truck','truck','dump','Add gravel falling from the raised bed.'),
('Bulldozer','A wide blade pushes soil across a site.','box','track','blade','Show a mound of dirt in front of the blade.'),
('Excavator','A long arm digs with a bucket.','box','track','arm','Draw a trench below the bucket.'),
('Wheel loader','A front bucket scoops loose material.','box','wheel','loader','Fill the bucket with stones.'),
('Road roller','Heavy drums flatten a new road.','box','drum','roller','Add a smooth road behind the roller.'),
('Cement mixer','A turning drum mixes concrete.','truck','truck','mixer','Add a chute and wet concrete.'),
('Forklift','Two metal forks lift a pallet.','box','wheel','fork','Stack three boxes on a pallet.'),
('Skid steer','A compact loader turns in tight spaces.','box','wheel','shortbucket','Show the machine inside a narrow gate.'),
('Backhoe','A backhoe digs at the rear and loads at the front.','box','wheel','backhoe','Add dirt beside both ends.'),
('Mobile crane','A telescoping boom lifts heavy loads.','truck','truck','crane','Hang a safe load from the hook.'),
('Tower crane','A tall fixed crane works above buildings.','tower','none','tower','Draw a building beneath the hook.'),
('Paver','A paver spreads hot asphalt in a flat strip.','box','track','paver','Show the fresh road behind it.'),
('Motor grader','A center blade smooths and shapes the ground.','long','wheel','grader','Draw a crown in the road.'),
('Trencher','A digging chain makes a narrow trench.','box','track','trencher','Add a pipe that could fit the trench.'),
('Scraper','A scraper cuts, carries, and spreads soil.','long','wheel','scraper','Shade the soil in its bowl.'),
('Telehandler','A long lifting boom reaches high places.','box','wheel','tele','Put a crate on the forks.'),
('Scissor lift','Crossed supports raise a work platform.','box','wheel','scissor','Draw a worker wearing a hard hat.'),
('Boom lift','A jointed arm raises a small basket.','box','wheel','boomlift','Show a light being repaired.'),
('Concrete pump','A folding boom sends concrete through a hose.','truck','wheel','pump','Draw the foundation being poured.'),
('Drilling rig','A rotating drill makes deep holes.','box','track','drill','Extend the drill below the ground line.'),
('Pile driver','A tall mast guides a heavy hammer.','box','track','pile','Draw one pile entering the earth.'),
('Asphalt mill','A milling drum removes old pavement.','long','track','mill','Show broken pavement behind it.'),
('Snowplow','An angled blade clears snow from roads.','truck','wheel','snow','Show cleared and snowy lanes.'),
('Street sweeper','Brushes collect dust and debris.','truck','wheel','sweep','Add leaves in front of the brushes.'),
('Tow truck','A lifting arm moves a disabled vehicle.','truck','wheel','tow','Draw a small car behind it.'),
('Fire engine','Firefighters carry hoses and ladders.','truck','wheel','fire','Add a ladder and a hydrant.'),
('Farm tractor','Large rear tires give a tractor traction.','box','tractor','tractor','Attach a wagon behind the tractor.'),
('Combine harvester','A wide header cuts grain in a field.','box','tractor','combine','Add rows of wheat in front.'),
('Logging truck','Long trailers carry cut logs.','long','truck','logs','Draw wood rings on the log ends.'),
('Crawler crane','Tracks support a lattice lifting boom.','box','track','lattice','Draw a hook and counterweight.'),
]

def line(c,x1,y1,x2,y2): c.line(x1,y1,x2,y2)
def poly(c,pts):
 p=c.beginPath();p.moveTo(*pts[0]);[p.lineTo(*q) for q in pts[1:]];c.drawPath(p)
def text(c,x,y,s,size=11,color=NAVY,font='DejaVu'):
 c.setFont(font,size);c.setFillColor(color);c.drawString(x,y,s)
def fit(c,x,y,s,maxw,size=11,color=NAVY,font='DejaVu'):
 while stringWidth(s,font,size)>maxw:size-=.3
 text(c,x,y,s,size,color,font)
def wheel(c,x,y,r):
 c.circle(x,y,r);c.circle(x,y,r*.36);[line(c,x,y,x+math.cos(a)*r*.7,y+math.sin(a)*r*.7) for a in (0,math.pi/2,math.pi,3*math.pi/2)]
def draw_machine(c,project,stage,x,y,scale=1):
 from machine_art import draw
 c.saveState();c.translate(x,y);c.scale(scale,scale)
 draw(c,project[4],stage)
 c.restoreState()

def cover_excavator(c,x,y,scale=1,stage=4,color=True):
 """Progressive excavator drawing; the lesson uses open, colorable outlines."""
 c.saveState();c.translate(x,y);c.scale(scale,scale)
 dark=HexColor('#1B3647');steel=HexColor('#59737D');gold=HexColor('#E5A52F')
 light=HexColor('#F5C963');glass=HexColor('#D8EAF0');track=HexColor('#344C59')
 if not color:gold=light=glass=track=white
 def shape(points,fill,stroke=dark,width=2.2):
  c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(width)
  p=c.beginPath();p.moveTo(*points[0]);[p.lineTo(*pt) for pt in points[1:]];p.close()
  c.drawPath(p,stroke=1,fill=1)
 # A restrained job-site horizon sits behind the machine.
 c.setStrokeColor(HexColor('#B8D2D9'));c.setLineWidth(1.4)
 c.line(7,23,326,23)
 for xx,yy in [(19,25),(36,32),(313,31)]:
  c.line(xx,23,xx+9,yy);c.line(xx+9,yy,xx+18,23)
 # Track loop and individual rollers form a recognisable undercarriage.
 c.setFillColor(track);c.setStrokeColor(dark);c.setLineWidth(2)
 c.roundRect(18,24,183,38,18,stroke=1,fill=1)
 c.setFillColor(HexColor('#E9F0ED') if color else white);c.roundRect(28,32,163,22,11,stroke=0,fill=1)
 for center in (46,72,98,124,150,176):
  c.setFillColor(steel if color else white);c.circle(center,43,9,stroke=1,fill=1)
  c.setFillColor(white);c.circle(center,43,3,stroke=0 if color else 1,fill=1)
 c.setStrokeColor(light if color else dark);c.setLineWidth(2);c.line(31,60,188,60)
 # The body has a substantial rear counterweight, a centered slewing ring,
 # and a distinct glass cab rather than a generic box on tracks.
 if stage>=2:
  c.setFillColor(dark if color else white);c.roundRect(93,61,49,10,4,stroke=1,fill=1)
  shape([(45,69),(48,113),(65,123),(131,123),(150,114),(188,111),(195,84),(181,69)],gold)
  shape([(52,77),(56,134),(71,150),(108,149),(129,115),(127,77)],light)
  shape([(65,89),(69,132),(78,139),(103,138),(116,113),(116,89)],glass)
  c.setStrokeColor(dark);c.setLineWidth(2);c.line(81,139,78,90);c.line(62,76,132,76)
 if stage>=3:
  shape([(141,117),(159,130),(198,178),(219,179),(229,163),(196,117),(169,101)],gold)
  shape([(210,174),(233,166),(268,135),(261,116),(243,119),(194,143)],light)
  shape([(254,124),(270,132),(294,91),(286,70),(270,75)],gold)
  shape([(283,75),(301,79),(317,65),(316,45),(304,34),(281,42),(273,55)],light)
 if stage<4:
  c.restoreState();return
 shape([(129,121),(169,127),(191,112),(191,88),(167,83),(141,93)],light)
 c.setFillColor(dark if color else white);c.roundRect(93,61,49,10,4,stroke=0 if color else 1,fill=1)
 c.setStrokeColor(dark);c.setLineWidth(2);c.line(81,139,78,90);c.line(62,76,132,76)
 c.setFillColor(dark if color else white);c.circle(111,105,3,stroke=0 if color else 1,fill=1)
 # Boom: two large plates, visible pins, and a hydraulic cylinder.
 # Work through the joints and hydraulic cylinders after the large shapes.
 c.setStrokeColor(steel);c.setLineWidth(7);c.line(168,114,209,160)
 c.setStrokeColor(HexColor('#E6EBE9'));c.setLineWidth(3);c.line(171,117,206,158)
 c.setStrokeColor(steel);c.setLineWidth(6);c.line(226,151,260,119)
 c.setStrokeColor(HexColor('#E6EBE9'));c.setLineWidth(2.5);c.line(228,149,258,121)
 for xx,yy in [(155,123),(206,167),(255,125)]:
  c.setFillColor(dark);c.circle(xx,yy,5,stroke=0,fill=1)
  c.setFillColor(white);c.circle(xx,yy,2,stroke=0,fill=1)
 # Dipper and toothed bucket extend clearly away from the vehicle.
 c.setStrokeColor(dark);c.setLineWidth(2)
 for xx,yy in [(285,42),(296,37),(307,38)]:
  shape([(xx,yy),(xx+7,yy-10),(xx+10,yy+1)],dark,dark,1)
 c.setStrokeColor(steel);c.setLineWidth(3);c.line(279,94,294,63)
 c.restoreState()

def base(c,title,number,kicker='DRAWING PROJECT'):
 c.setFillColor(TEAL);c.rect(45,744,47,5,stroke=0,fill=1)
 text(c,46,720,kicker,9,TEAL,'DejaVu-Bold');fit(c,46,686,title,520,25,NAVY,'DejaVu-Bold')
 c.setStrokeColor(HexColor('#D6E2E3'));line(c,46,53,566,53)
 text(c,46,36,'HOW TO DRAW CONSTRUCTION MACHINES',8,GRAY,'DejaVu-Bold')
 c.setFont('DejaVu',9);c.setFillColor(GRAY);c.drawRightString(566,36,str(number))
def finish(c):c.showPage()
c=canvas.Canvas(str(OUT/'Machine_Draw_Interior.pdf'),pagesize=(W,H),pageCompression=1)
c.setTitle('How to Draw Construction Machines - Final Draft R15');c.setAuthor('Heath Tolley')
pages=0
def page():
 global pages
 pages+=1
def coverpage():
 global pages
 page();c.setFillColor(TEAL);c.rect(58,706,118,7,stroke=0,fill=1)
 text(c,58,638,'HOW TO DRAW',36,NAVY,'DejaVu-Bold');text(c,58,593,'CONSTRUCTION',36,NAVY,'DejaVu-Bold');text(c,58,548,'MACHINES',36,NAVY,'DejaVu-Bold')
 text(c,58,508,'Step-by-Step Trucks, Diggers, Cranes, and More',17,NAVY)
 text(c,58,479,'for Kids Ages 6-10',17,GRAY)
 c.setStrokeColor(HexColor('#CADADA'));c.setFillColor(white);c.roundRect(66,184,469,260,16,stroke=1,fill=1)
 cover_excavator(c,110,208,1.15,4,False)
 text(c,58,93,'30 PROJECTS  /  10 SCENE CHALLENGES',14,TEAL,'DejaVu-Bold');text(c,58,67,'Heath Tolley',13,NAVY)
 finish(c)
coverpage()
page();base(c,'Start with shapes',pages,'WELCOME')
for y,n,description in [(598,'01  Look','See the whole machine before you draw.'),(522,'02  Build','Copy the shapes in order. New parts appear each step.'),(446,'03  Check','Compare the final drawing with your own version.'),(370,'04  Invent','Finish the challenge with a useful scene.')]:
 text(c,55,y,n,20,TEAL,'DejaVu-Bold');text(c,55,y-25,description,13)
text(c,55,247,'You need a pencil, an eraser, and a sheet of paper.',15,NAVY,'DejaVu-Bold')
text(c,55,219,'Try light lines first. Trace darker lines after the machine looks right.',12)
text(c,55,184,'Your drawing can be different. That is part of learning.',12)
text(c,55,155,'Erase hidden lines when a new part covers an earlier shape.',11)
text(c,55,91,'Final draft | Revision 15 | 30 September 2026',8,GRAY)
finish(c)
page();base(c,'Your shape toolkit',pages,'WARM-UP')
for i,(label,desc) in enumerate([('BOX','truck bodies and cabins'),('CIRCLE','wheels and drums'),('LONG LINE','booms and blades'),('ZIGZAG','tracks, treads, and lifting arms')]):
 y=584-i*116;c.setStrokeColor(TEAL);c.setLineWidth(3)
 if i==0:c.roundRect(60,y-15,74,42,5)
 if i==1:c.circle(95,y+3,23)
 if i==2:line(c,58,y-6,139,y+23)
 if i==3:poly(c,[(58,y-12),(76,y+19),(94,y-12),(112,y+19),(134,y-12)])
 text(c,164,y+12,label,13,TEAL,'DejaVu-Bold');text(c,164,y-11,desc,12)
text(c,55,99,'Practice each shape five times, then combine a box and two circles.',11)
finish(c)
page();base(c,'How the lessons work',pages,'MAP')
for i,(a,b) in enumerate([('Level 1 / Shape builders','Projects 1-10: recognize the body and wheels.'),('Level 2 / Long machines','Projects 11-20: add arms, booms, and special parts.'),('Level 3 / Clever details','Projects 21-30: compare similar machines.'),('Finish / Scene challenges','Make whole construction scenes with a purpose.')]):
 y=585-i*112;text(c,55,y,a,17,TEAL,'DejaVu-Bold');text(c,55,y-29,b,12)
text(c,55,111,'Tip: Go back to an easier project whenever you need a warm-up.',11)
finish(c)
for idx,p in enumerate(projects):
 page();base(c,p[0],pages,'LEVEL '+str(1+idx//10)+'  /  PROJECT '+str(idx+1).zfill(2))
 fit(c,50,648,p[1],510,12,GRAY)
 from machine_art import LESSON_LABELS
 labels=[str(n+1)+'  '+t for n,t in enumerate(LESSON_LABELS[p[4]])]
 for st in range(1,5):
  col=(st-1)%2; row=(st-1)//2;bx=49+col*260;by=384-row*230
  c.setStrokeColor(HexColor('#CADADA'));c.roundRect(bx,by,244,205,8)
  text(c,bx+12,by+182,labels[st-1],10,TEAL,'DejaVu-Bold')
  if p[0]=='Excavator':
   cover_excavator(c,bx+13,by+43,.66,st,False)
  else:draw_machine(c,p,st,bx+14,by+22,.89)
 text(c,53,124,'TRY IT',10,TEAL,'DejaVu-Bold');fit(c,53,102,p[5],500,12)
 text(c,53,77,'Draw on your own paper. Change one detail to make it yours.',10,GRAY)
 finish(c)
 page();base(c,p[0]+': draw and color',pages,'PROJECT '+str(idx+1).zfill(2)+'  /  PRACTICE')
 text(c,53,650,'Study its main parts. Color the outline and add the job-site scene.',12,GRAY)
 c.setStrokeColor(HexColor('#CADADA'));c.roundRect(49,295,514,317,8)
 if p[0]=='Excavator':cover_excavator(c,100,360,1.27,4,False)
 else:draw_machine(c,p,4,110,322,1.58)
 text(c,53,256,'Make it your own:',12,TEAL,'DejaVu-Bold')
 fit(c,53,223,p[5],510,11)
 text(c,53,192,'Circle two moving parts. Add a person for scale.',11)
 text(c,53,146,'Use your own paper for a larger version of this machine.',11,GRAY)
 finish(c)
scenes=[
('A road under repair','Use a paver, roller, and dump truck.','Which machine arrives first? Show the old and new road.'),
('A new house foundation','Use an excavator, cement mixer, and pump.','Where will the truck stop so its chute can reach?'),
('A city at sunrise','Use a tower crane, loader, and delivery truck.','Place the crane behind the half-built building.'),
('A snowy street','Use a snowplow and road grader.','Show where the snow is pushed and where cars may drive.'),
('A tree cleanup','Use a logging truck, loader, and tow truck.','Keep people away from the moving equipment.'),
('A harvest day','Use a tractor, combine, and truck.','Show the grain moving from field to truck.'),
('A tall repair job','Use a scissor lift and boom lift.','Why is each lift useful at a different height?'),
('A trench for a pipe','Use a trencher, backhoe, and loader.','Make the trench narrow and place the soil beside it.'),
('A clean neighborhood','Use a street sweeper, fire engine, and forklift.','Make each machine do a different job.'),
('Invent a job site','Choose any four machines in this book.','Give every machine a task and show what changed.')]
for j,(title,cast,question) in enumerate(scenes):
 page();base(c,title,pages,'SCENE CHALLENGE '+str(j+1).zfill(2))
 text(c,55,643,cast,13,TEAL,'DejaVu-Bold');fit(c,55,614,question,510,12)
 c.setStrokeColor(HexColor('#C6D8DA'));c.rect(55,216,502,365)
 c.setDash(3,5);[line(c,55,216+i*73,557,216+i*73) for i in range(1,5)];c.setDash()
 text(c,55,175,'PLAN THE SCENE',10,TEAL,'DejaVu-Bold')
 text(c,55,149,'Near: __________________________  Far: __________________________',11)
 text(c,55,123,'What is each machine doing? ________________________________________',11)
 text(c,55,92,'Try one version here; make a larger drawing on separate paper.',10,GRAY)
 finish(c)
page();base(c,'The machine finder',pages,'REFERENCE')
for i,p in enumerate(projects):
 col=i//15;row=i%15;x=55+col*255;y=624-row*36
 text(c,x,y,str(i+1).zfill(2),10,TEAL,'DejaVu-Bold');fit(c,x+27,y,p[0],210,10)
finish(c)
page();base(c,'Keep drawing',pages,'NEXT STEPS')
for y,head,body in [(592,'Choose a favorite','Draw it three times: side view, working, and parked.'),(486,'Change the scale','Draw a tiny worker to show how large the machine is.'),(380,'Observe in real life','Look for hinges, windows, warning lights, and shadows.'),(274,'Tell a story','Put two machines in one scene and give each a job.')]:
 text(c,55,y,head,18,TEAL,'DejaVu-Bold');text(c,55,y-28,body,12)
text(c,55,117,'Remember: start with a shape, then let the details do the work.',12,NAVY,'DejaVu-Bold')
finish(c)
c.save()
assert pages==76,pages
spine=pages*.002252; CW=(17.25+spine)*72;CH=11.25*72
co=canvas.Canvas(str(OUT/'Machine_Draw_Full_Wrap_Cover.pdf'),pagesize=(CW,CH),pageCompression=1)
sw=spine*72; frontx=(8.625*72)+sw
co.setFillColor(NAVY);co.rect(0,0,CW,CH,stroke=0,fill=1)
co.setFillColor(TEAL);co.rect(0,0,8.625*72,CH,stroke=0,fill=1)
co.setFillColor(ORANGE);co.rect(frontx+45,CH-92,105,8,stroke=0,fill=1)
text(co,frontx+45,CH-159,'HOW TO DRAW',35,white,'DejaVu-Bold')
text(co,frontx+45,CH-203,'CONSTRUCTION',32,white,'DejaVu-Bold')
text(co,frontx+45,CH-245,'MACHINES',36,white,'DejaVu-Bold')
text(co,frontx+45,CH-283,'Step-by-Step Trucks, Diggers,',16,HexColor('#E7F2F0'))
text(co,frontx+45,CH-308,'Cranes, and More for Kids Ages 6-10',15,HexColor('#E7F2F0'))
co.setFillColor(HexColor('#EAF4F2'));co.roundRect(frontx+40,172,510,265,16,stroke=0,fill=1)
cover_excavator(co,frontx+80,190,1.3)
text(co,frontx+45,93,'30 PROJECTS  /  10 SCENE CHALLENGES',13,ORANGE,'DejaVu-Bold')
text(co,frontx+45,69,'Heath Tolley',12,white)
text(co,48,CH-129,'DRAW REAL MACHINES',22,white,'DejaVu-Bold')
text(co,48,CH-158,'ONE SHAPE AT A TIME.',22,white,'DejaVu-Bold')
for y,s in [(CH-218,'Start with simple boxes, circles, and lines.'),(CH-246,'Follow four clear drawing steps for each machine.'),(CH-274,'Learn what each machine does on a real job.'),(CH-302,'Build ten original scenes with your new skills.')]:
 text(co,49,y,s,12,white)
text(co,48,CH-373,'INSIDE',12,ORANGE,'DejaVu-Bold')
for k,s in enumerate(['30 different machine lessons','30 matching coloring pages','Three levels of drawing practice','Ten scenes that combine machines','A quick machine finder']):text(co,49,CH-402-k*29,'- '+s,12,white)
# A generous barcode zone remains free of text and art at lower right of back cover.
co.setFillColor(white);co.setFont('DejaVu',9);co.drawString(50,188,'For kids ages 6-10 | Paperback | Black-and-white interior')
co.showPage();co.save()
print('pages',pages,'cover inches',CW/72,CH/72,'spine',spine)
