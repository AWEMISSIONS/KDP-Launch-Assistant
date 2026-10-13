"""Original art-and-emotion course, with reusable vector diagrams and print checks."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
from math import sin,cos,pi

O=Path('dist/books/draw-feelings');O.mkdir(parents=True,exist_ok=True)
W,H=612,792
INK=HexColor('#243448');TEAL=HexColor('#087E86');YELLOW=HexColor('#E7A53C');MUTED=HexColor('#637583');PALE=HexColor('#D4E3E4')
EMOTIONS=[
('Calm','relaxed','easy breath','The rain taps the window while Maya reads.','Show a quiet smile and shoulders at rest.','Calm can be quiet without being happy.','I feel settled and ready to listen.'),
('Joyful','lifted','wide smile','Sam sees his friend return after a long trip.','Lift the cheeks; open both arms.','Joy may fill the whole body.','I am glad you are here!'),
('Excited','high','open grin','A class is about to begin its field trip.','Open the eyes wider and tilt the body forward.','Excitement can feel fast and buzzy.','I can hardly wait to start.'),
('Proud','steady','small smile','Nora finally rides her bicycle without help.','Keep the chin up and posture tall.','Pride can follow patient practice.','I worked hard on this.'),
('Curious','one up','small open','A box with a strange label arrives.','Raise one brow and turn the head.','Curiosity asks what might be inside.','I wonder how this works.'),
('Surprised','arched','round','A hidden birthday banner drops from the doorway.','Lift both brows and make a round mouth.','Surprise can be pleasant or unpleasant.','Oh! I did not expect that.'),
('Confused','uneven','crooked','A map seems to point in two directions.','Make the brows uneven and tilt the head.','Confusion is a cue to ask for help.','Could you show me another way?'),
('Worried','inner high','pressed','A late bus has not arrived at the stop.','Lift the inner brows; bring hands together.','Worry is often about what might happen.','I hope the bus comes soon.'),
('Afraid','high','open small','A loud thunderclap shakes the windows.','Widen the eyes; lean the body back.','A person may also freeze when afraid.','That sound startled me.'),
('Sad','inner high','down','A favorite toy is broken.','Turn the mouth down and lower the shoulders.','Sadness can invite comfort and time.','I miss how it used to be.'),
('Lonely','soft','flat','Everyone has a partner except Eli.','Look aside; turn the body a little away.','Loneliness is about missing connection.','Could I join you?'),
('Disappointed','flat','down small','The picnic is canceled because of rain.','Let the shoulders sag and the smile fade.','Disappointment follows a hoped-for outcome.','I was looking forward to that.'),
('Frustrated','low','pressed','A puzzle piece will not fit after many tries.','Angle the brows and tense the hands.','Frustration can signal a need for a pause.','I need a break before trying again.'),
('Angry','sharp down','flat hard','Someone tears up a drawing without asking.','Lower the brows and square the shoulders.','Anger is real; actions still matter.','Please stop. That was mine.'),
('Embarrassed','inner high','uneven smile','Tara trips during a quiet assembly.','Add warm cheeks and a hand near the face.','Embarrassment may make someone look away.','That was awkward. I am okay.'),
('Shy','soft','closed smile','A new student is invited to introduce himself.','Keep the smile small and arms close.','A shy person may want more time.','Can I go after someone else?'),
('Hopeful','lifted','small smile','Seeds have been planted in a garden bed.','Lift the gaze slightly toward the future.','Hope looks toward a possible good outcome.','I think these seeds could grow.'),
('Grateful','soft','warm smile','A friend helps carry heavy books.','Relax the eyes; offer an open palm.','Gratitude notices a gift or kindness.','Thank you for helping me.'),
('Tired','droop','small flat','After a long hike, Jo sits beside the trail.','Lower the eyelids; let the body rest.','Tiredness can look like several feelings.','I need water and a little rest.'),
('Sleepy','closed','open yawn','A bedtime story reaches its last page.','Close the lids and open the mouth in a yawn.','Sleepiness is a body cue.','I am ready to sleep.'),
('Silly','one up','side grin','Two cousins invent an upside-down dance.','Make the face asymmetrical and pose playful.','Silly can be shared with a willing friend.','Want to try this goofy move?'),
('Playful','lifted','open grin','A puppy brings back a toy for another round.','Let the smile and hands invite a game.','Playfulness can be gentle and welcoming.','Let us play again!'),
('Focused','low flat','neutral','Ben follows the tiny lines of a drawing.','Aim the eyes at the task; lean in.','Focus may look serious even when enjoyable.','Just a moment; I am finishing this.'),
('Determined','angled','firm','The hill is steep, but Ada keeps hiking.','Set the jaw and keep the body upright.','Determination means continuing with care.','I will take it one step at a time.'),
('Nervous','inner high','tight smile','It is time to speak in front of the class.','Show an uncertain smile and hands held close.','Nerves and excitement can appear together.','I am nervous, so I will breathe first.'),
('Relieved','soft','exhale','The missing library book is found.','Relax the shoulders and draw an exhale.','Relief follows the end of a worry.','I am glad we found it.'),
('Thoughtful','one up','neutral','Lee listens before answering a hard question.','Look to one side and put a hand near the chin.','Thinking can take time without a clear face.','Let me consider that.'),
('Impatient','low','pressed','The line for the ride has hardly moved.','Tilt the body forward and tap one foot.','Waiting can make the body feel restless.','How much longer will it be?'),
('Kind','soft','warm smile','A child shares an umbrella with a classmate.','Use gentle eyes and an open hand.','Kindness is shown by an action.','You can stand under here with me.'),
('Brave','steady','firm smile','Rae asks for help when something feels wrong.','Keep the posture steady despite worry.','Bravery can happen while afraid.','I need help with this.'),
]

def write(c,x,y,s,size=11,color=INK,bold=False,maxwidth=None):
 font='DejaVu-Bold' if bold else 'DejaVu'; c.setFont(font,size);c.setFillColor(color)
 if maxwidth:
  while stringWidth(s,font,size)>maxwidth:size-=.25;c.setFont(font,size)
 c.drawString(x,y,s)
def wrap(c,x,y,s,width,size=11,leading=16,color=INK,bold=False):
 words=s.split();line='';out=[];font='DejaVu-Bold' if bold else 'DejaVu'
 for word in words:
  candidate=(line+' '+word).strip()
  if stringWidth(candidate,font,size)>width and line:out.append(line);line=word
  else:line=candidate
 if line:out.append(line)
 for n,line in enumerate(out):write(c,x,y-n*leading,line,size,color,bold)
 return y-len(out)*leading
def curve(c,pts):
 p=c.beginPath();p.moveTo(*pts[0]);[p.lineTo(*v) for v in pts[1:]];c.drawPath(p)

def face(c,idx,x,y,scale=1,stage=4,intensity=1,variant=0):
 """Draw distinctive expressions using continuous facial and body cues."""
 name,brow,mouth,*_=EMOTIONS[idx]
 c.saveState();c.translate(x,y);c.scale(scale,scale);c.setLineWidth(2.2);c.setStrokeColor(INK);c.setLineCap(1)
 shift=(-6,0,6)[variant%3]
 # Head contours vary: round, oval, angular, broad.
 style=idx%4
 if style==0:c.ellipse(44,72,154,188)
 elif style==1:c.ellipse(38,75,160,183)
 elif style==2:
  curve(c,[(63,178),(99,196),(139,177),(159,128),(146,89),(111,72),(68,88),(40,127),(63,178)])
 else:c.roundRect(43,74,112,111,46)
 if stage>=2:
  # Eyes use variable aperture and gaze, not identical dot pairs.
  if name in ('Sleepy',):
   c.arc(59,123,86,137,180,180);c.arc(111,123,138,137,180,180)
  elif name in ('Tired','Relieved','Calm','Shy'):
   c.arc(59,124,88,139,180,160);c.arc(110,124,139,139,180,160)
   c.circle(74+shift/3,126,2);c.circle(126+shift/3,126,2)
  elif name in ('Surprised','Afraid','Excited'):
   c.ellipse(61,118,85,146);c.ellipse(113,118,137,146)
   c.circle(73+shift/4,131,4);c.circle(125+shift/4,131,4)
  elif name in ('Angry','Determined','Focused','Impatient','Frustrated'):
   c.ellipse(59,124,88,138);c.ellipse(110,124,139,138)
   c.circle(75+shift/3,131,3);c.circle(125+shift/3,131,3)
  else:
   c.ellipse(59,119,87,140);c.ellipse(112,119,140,140)
   c.circle(73+shift/3,129,3);c.circle(126+shift/3,129,3)
  curve(c,[(97,119),(95,105),(102,103)])
 if stage>=3:
  # Signed angles of both brows and distinct mouth geometry.
  if brow in ('high','arched'):curve(c,[(56,151+intensity*3),(72,156+intensity*6),(87,151+intensity*3)]);curve(c,[(110,151+intensity*3),(126,156+intensity*6),(141,151+intensity*3)])
  elif brow=='inner high':curve(c,[(57,149),(86,151+intensity*7)]);curve(c,[(111,151+intensity*7),(140,149)])
  elif brow=='sharp down':curve(c,[(56,157),(87,145-intensity*2)]);curve(c,[(110,145-intensity*2),(141,157)])
  elif brow in ('low','low flat','angled'):curve(c,[(55,147+intensity*2),(87,143)]);curve(c,[(110,143),(142,147+intensity*2)])
  elif brow in ('one up','uneven'):curve(c,[(55,157+intensity*3),(86,152)]);curve(c,[(110,145),(141,150)])
  elif brow=='droop':curve(c,[(58,147),(86,144)]);curve(c,[(111,144),(139,147)])
  else:curve(c,[(57,151),(85,154)]);curve(c,[(112,154),(140,151)])
  if 'grin' in mouth or 'wide smile' in mouth:
   c.arc(66,83,133,113,189,162);c.line(78,100,124,100)
  elif mouth in ('small smile','warm smile','closed smile','firm smile'):
   c.arc(76,88,124,110,195,150)
  elif mouth in ('round','open small','open yawn'):c.ellipse(88,80,111,105)
  elif mouth in ('down','down small'):c.arc(76,82,124,106,12,160)
  elif mouth=='crooked':curve(c,[(78,91),(105,96),(125,100)])
  elif mouth=='uneven smile':curve(c,[(77,97),(104,91),(125,103)])
  elif mouth=='side grin':c.arc(77,86,125,109,195,115)
  elif mouth=='exhale':c.ellipse(90,86,105,97);curve(c,[(107,90),(127,88),(144,84)])
  elif mouth=='tight smile':
   if intensity>=2:
    curve(c,[(79,96),(89,91),(98,97),(108,91),(120,96)])
    c.line(156,118,167,113);c.line(164,123,171,118)
   else:c.arc(83,90,118,105,196,144)
  else:c.line(83,94,119,94)
  if name=='Embarrassed':
   for q in (58,130):c.line(q,106,q+7,103);c.line(q+2,112,q+9,109)
 if stage>=4:
  # Arms and trunk carry as much meaning as mouth.
  curve(c,[(70,75),(64,64),(57,44),(53,18)]);curve(c,[(130,75),(135,60),(144,39),(147,18)])
  c.arc(37,-45,161,51,5,170)
  if name in ('Joyful','Excited','Playful','Silly'):
   curve(c,[(57,47),(25,102),(15,108)]);curve(c,[(145,44),(178,104),(187,109)])
  elif name in ('Worried','Nervous','Shy','Lonely'):
   curve(c,[(56,47),(98,45),(108,31)]);curve(c,[(145,47),(109,40),(101,32)])
  elif name in ('Angry','Frustrated','Impatient'):
   curve(c,[(53,50),(106,20),(146,51)]);curve(c,[(144,49),(91,22),(54,48)])
  elif name in ('Kind','Grateful','Relieved'):
   curve(c,[(53,50),(20,25),(12,24)]);curve(c,[(146,50),(179,27),(190,27)])
  elif name in ('Curious','Thoughtful','Confused'):
   curve(c,[(145,51),(138,83),(116,91)]);curve(c,[(54,49),(33,23)])
  elif name in ('Proud','Brave','Determined','Hopeful'):
   curve(c,[(56,50),(31,28)]);curve(c,[(144,50),(168,28)]);c.line(100,38,100,59)
  elif name in ('Sad','Disappointed','Tired','Sleepy'):
   curve(c,[(55,50),(43,23)]);curve(c,[(143,49),(158,21)])
  else:curve(c,[(55,50),(37,22)]);curve(c,[(144,50),(161,22)])
  if intensity>=2:
   if name in ('Afraid','Worried','Nervous','Surprised','Excited'):
    c.line(22,126,35,134);c.line(18,111,31,116)
    c.line(165,134,178,128);c.line(170,116,183,112)
   elif name in ('Angry','Frustrated','Determined','Proud','Brave'):
    c.line(24,145,35,137);c.line(168,137,179,145)
   elif name in ('Sad','Tired','Sleepy','Disappointed'):
    c.arc(143,31,169,55,180,120)
 c.restoreState()

def pagebase(c,title,kicker,n):
 c.setFillColor(TEAL);c.rect(48,746,44,5,stroke=0,fill=1)
 write(c,48,718,kicker.upper(),9,TEAL,True)
 write(c,48,680,title,26,INK,True,maxwidth=510)
 c.setStrokeColor(PALE);c.line(48,52,564,52)
 write(c,48,36,'HOW TO DRAW FACES & FEELINGS',8,MUTED,True)
 c.setFillColor(MUTED);c.setFont('DejaVu',9);c.drawRightString(564,36,str(n))

pages=0;pdf=O/'How_to_Draw_Faces_and_Feelings_Interior.pdf';c=canvas.Canvas(str(pdf),pagesize=(W,H),pageCompression=1)
def new(title,kicker):
 global pages;pages+=1;pagebase(c,title,kicker,pages)
def done():c.showPage()
new('How to Draw Faces & Feelings','A drawing course for kids')
write(c,49,622,'30 expressions  /  90 variations  /  10 story scenes',16,TEAL,True)
face(c,2,148,202,1.55);write(c,49,122,'A face gives clues. A pose gives more.',15,INK,True)
write(c,49,93,'Heath Tolley',12);done()
new('A face is a clue','Start here')
for j,(h,s) in enumerate([('Look','Notice the eyebrows, eyes, and mouth.'),('Look again','A pose and setting can change what the face means.'),('Ask','We cannot know exactly what someone feels just by looking.'),('Draw','Use the clues, then make a character with a story.')]):
 y=600-j*117;write(c,55,y,h,19,TEAL,True);wrap(c,55,y-29,s,485,13)
write(c,55,100,'Many feelings can be mixed. Every person shows them differently.',12,INK,True);done()
new('The expression toolkit','Warm-up 1')
for j,(h,s) in enumerate([('EYEBROWS','Try two high, two low, and one uneven pair.'),('EYES','Try wide, narrow, looking aside, and closed.'),('MOUTHS','Try a smile, an O, a flat line, and a frown.'),('POSTURE','Draw shoulders raised, dropped, open, and turned away.')]):
 y=594-j*114;write(c,55,y,h,15,TEAL,True);write(c,55,y-29,s,12)
done()
new('Change one clue','Warm-up 2')
for j,i in enumerate((0,5,13)):
 x=48+j*176;face(c,i,x+4,331,.69);write(c,x+6,311,EMOTIONS[i][0],12,TEAL,True)
write(c,55,206,'Try keeping the eyes but changing only the mouth.',13)
write(c,55,178,'Then keep the mouth but change the brows.',13)
write(c,55,125,'Which change was easiest for you to recognize?',12,MUTED);done()
new('Your practice plan','Warm-up 3')
for j,s in enumerate(['Lessons 01-10: begin with easy-to-read expressions.','Lessons 11-20: draw quieter or mixed clues.','Lessons 21-30: add action, posture, and context.','Story scenes: combine two people and a cause for each feeling.']):write(c,55,586-j*92,s,12)
write(c,55,138,'Draw with a pencil first. Keep the sketch lines light.',12,INK,True);done()
for i,(name,brow,mouth,situation,cue,insight,dialogue) in enumerate(EMOTIONS):
 new(name,'Lesson '+str(i+1).zfill(2)+'  /  See the clues')
 wrap(c,49,645,situation,505,12,16,MUTED)
 for stage in (1,2,3,4):
  bx=49+((stage-1)%2)*258;by=384-((stage-1)//2)*230
  c.setStrokeColor(PALE);c.roundRect(bx,by,243,206,7)
  write(c,bx+11,by+181,['1  Head outline','2  Set the eyes','3  Shape brows and mouth','4  Add the body cue'][stage-1],10,TEAL,True)
  face(c,i,bx+42,by+26,.72,stage)
 write(c,52,111,'DRAWING CLUE',10,TEAL,True);wrap(c,52,91,cue,500,11)
 done()
 new(name+': three strengths','Lesson '+str(i+1).zfill(2)+'  /  Apply it')
 write(c,49,642,'The same feeling can appear softly or strongly.',12,MUTED)
 for k,label in enumerate(('A hint','Easy to see','Strong')):
  bx=49+k*174;c.setStrokeColor(PALE);c.roundRect(bx,339,164,269,7)
  write(c,bx+12,584,label,12,TEAL,True)
  face(c,i,bx+1,397,.8,3 if k==0 else 4,k,variant=k)
  note=(('Brow: '+brow+'.') if k==0 else ('Mouth: '+mouth+'.') if k==1 else cue)
  wrap(c,bx+12,372,note,140,9,12,MUTED)
 write(c,52,296,'IN THIS STORY',10,TEAL,True);wrap(c,52,273,situation,500,11)
 write(c,52,231,'A CHARACTER COULD SAY',10,TEAL,True);wrap(c,52,208,'"'+dialogue+'"',500,11)
 write(c,52,166,'YOUR TURN',10,TEAL,True);wrap(c,52,143,insight+' Draw another cause for this feeling.',500,11)
 done()
scenes=[
('A missed invitation','Lonely','Kind','One child notices another sitting alone.'),('The broken project','Frustrated','Thoughtful','A model falls apart just before display time.'),('A new place','Nervous','Curious','Two children arrive at an unfamiliar club.'),('Waiting for news','Worried','Relieved','The family dog has wandered out and returns.'),('An unexpected gift','Surprised','Grateful','A friend shares something handmade.'),('The difficult climb','Afraid','Brave','A child asks for help on a steep path.'),('A hard goodbye','Sad','Hopeful','Friends promise to write after a move.'),('Not yet','Impatient','Calm','A long line moves one small step at a time.'),('A fresh start','Embarrassed','Determined','Someone tries again after a public mistake.'),('Your own story','Joyful','Confused','Choose the story that joins two different feelings.')]
for j,(title,one,two,setup) in enumerate(scenes):
 new(title,'Story scene '+str(j+1).zfill(2))
 write(c,52,636,one+'  +  '+two,14,TEAL,True);wrap(c,52,606,setup,510,12)
 a=next(i for i,e in enumerate(EMOTIONS) if e[0]==one);b=next(i for i,e in enumerate(EMOTIONS) if e[0]==two)
 face(c,a,73,311,.9);face(c,b,322,311,.9)
 c.setStrokeColor(PALE);c.roundRect(53,239,505,291,8)
 write(c,60,261,'Characters: '+one+' and '+two,10,MUTED)
 write(c,52,207,'1. Show the setting.  2. Add a reason.  3. Draw the next action.',11)
 write(c,52,158,'How could each person describe what they feel?',11,INK,True)
 write(c,52,123,'Make a bigger version on separate paper.',10,MUTED)
 done()
new('Expression finder','Reference')
for i,e in enumerate(EMOTIONS):
 x=52+(i//15)*258;y=622-(i%15)*36
 write(c,x,y,str(i+1).zfill(2),10,TEAL,True);write(c,x+28,y,e[0],10)
done()
new('When clues are unclear','Reference')
for j,(h,s) in enumerate([('Look for context','A wide eye can mean fear, surprise, or excitement.'),('Avoid guessing','Ask kindly when you need to know how someone feels.'),('Notice change','A small shift in pose can tell part of the story.'),('Let characters disagree','Two people can feel differently about one event.')]):
 y=588-j*112;write(c,55,y,h,16,TEAL,True);wrap(c,55,y-27,s,485,12)
done()
new('Make your own character','Final project')
for j,s in enumerate(['Choose an event from your day or invent one.','Draw the person before the event and afterward.','Change two facial clues and one body cue.','Give the person a sentence in their own words.']):write(c,55,593-j*105,str(j+1)+'.  '+s,12)
write(c,55,118,'Your character can feel more than one thing at once.',12,INK,True)
done();c.save()
assert pages==78,pages

spine=pages*.002252;CW=(17.25+spine)*72;CH=11.25*72;FRONT=8.625*72+spine*72
co=canvas.Canvas(str(O/'How_to_Draw_Faces_and_Feelings_Full_Wrap_Cover.pdf'),pagesize=(CW,CH),pageCompression=1)
co.setFillColor(INK);co.rect(0,0,CW,CH,stroke=0,fill=1)
co.setFillColor(TEAL);co.rect(0,0,8.625*72,CH,stroke=0,fill=1)
write(co,FRONT+44,CH-153,'HOW TO DRAW',36,white,True)
write(co,FRONT+44,CH-198,'FACES & FEELINGS',32,white,True)
write(co,FRONT+44,CH-244,'A step-by-step drawing and emotion',15,white)
write(co,FRONT+44,CH-267,'vocabulary book for kids',15,white)
co.setFillColor(white);co.roundRect(FRONT+38,184,510,265,16,stroke=0,fill=1)
for j,i in enumerate((1,5,13)):
 co.saveState();co.translate(FRONT+43+j*168,237);co.scale(.75,.75);face(co,i,0,0,1);co.restoreState()
write(co,FRONT+44,112,'30 EXPRESSIONS  /  90 VARIATIONS',14,YELLOW,True)
write(co,FRONT+44,88,'10 STORY SCENES',14,YELLOW,True)
write(co,FRONT+44,65,'Heath Tolley',12,white)
write(co,46,CH-141,'DRAW THE CLUES',25,white,True)
write(co,46,CH-178,'TELL THE STORY',25,white,True)
for j,s in enumerate(['Learn how eyebrows, eyes, and mouths change.','Show the feeling through posture and action.','Compare a hint, a clear cue, and a strong cue.','Use words and context to tell a fuller story.']):
 write(co,46,CH-240-j*31,s,11,white)
write(co,46,CH-413,'INSIDE',12,YELLOW,True)
for j,s in enumerate(['30 two-page drawing lessons','90 variations to compare','10 guided story scenes','An expression reference']):write(co,46,CH-441-j*29,'- '+s,12,white)
co.showPage();co.save()
print('pages',pages,'cover inches',CW/72,CH/72)
