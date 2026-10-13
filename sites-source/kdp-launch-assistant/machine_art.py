"""Closed vector assemblies for the 30-machine drawing course.

All solid outlines are closed. Wheel mounts and attachment beams are explicit.
Coordinates are a common 240 x 180 drawing area, in points before scaling.
"""
import math
from reportlab.lib.colors import HexColor, white
INK=HexColor('#173447')

class Art:
    def __init__(self,c,stage):
        self.c=c; self.stage=stage
        c.setStrokeColor(INK);c.setFillColor(white);c.setLineWidth(1.8)
        c.setLineJoin(1);c.setLineCap(1)
    def path(self,pts,fill=True):
        p=self.c.beginPath();p.moveTo(*pts[0])
        for q in pts[1:]:p.lineTo(*q)
        p.close();self.c.setFillColor(white);self.c.drawPath(p,stroke=1,fill=int(fill))
    def line(self,*pts):
        p=self.c.beginPath();p.moveTo(*pts[0])
        for q in pts[1:]:p.lineTo(*q)
        self.c.drawPath(p,stroke=1,fill=0)
    def box(self,x,y,w,h,r=0):
        self.c.setFillColor(white)
        if r:self.c.roundRect(x,y,w,h,r,stroke=1,fill=1)
        else:self.c.rect(x,y,w,h,stroke=1,fill=1)
    def circle(self,x,y,r,fill=True):
        self.c.setFillColor(white);self.c.circle(x,y,r,stroke=1,fill=int(fill))
    def beam(self,a,b,width=8):
        dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy)
        nx=-dy/length*width/2;ny=dx/length*width/2
        self.path([(a[0]+nx,a[1]+ny),(b[0]+nx,b[1]+ny),(b[0]-nx,b[1]-ny),(a[0]-nx,a[1]-ny)])
    def pin(self,p,r=3):self.circle(*p,r)
    def wheel(self,x,y,r,mount):
        self.beam((x,mount),(x,y),6)
        self.circle(x,y,r);self.circle(x,y,r*.4)
        if self.stage>=4:
            for k in range(8):
                a=k*math.pi/4
                self.line((x+math.cos(a)*r*.65,y+math.sin(a)*r*.65),(x+math.cos(a)*r*.84,y+math.sin(a)*r*.84))
        self.circle(x,y,2)
    def track(self,x,y,w,mount):
        self.box(x+12,y+12,w-24,max(1,mount-y-12))
        self.box(x,y,w,24,11)
        for xx in range(int(x+15),int(x+w-6),20):
            self.circle(xx,y+12,7);self.circle(xx,y+12,2)
        if self.stage>=4:
            for xx in range(int(x+15),int(x+w-10),12):
                self.line((xx,y+2),(xx,y+5));self.line((xx,y+19),(xx,y+22))
    def cab(self,x,y,w=39,h=42):
        self.path([(x,y),(x+7,y+h),(x+w-7,y+h),(x+w,y)])
        self.path([(x+9,y+9),(x+13,y+h-8),(x+w-13,y+h-8),(x+w-8,y+9)])
        if self.stage>=4:self.line((x+w-8,y+6),(x+w-3,y+6))
    def vents(self,x,y,n=4):
        for j in range(n):self.line((x+j*5,y),(x+j*5,y+8))
    def hook(self,x,y):
        self.line((x,y),(x,y-5),(x+4,y-8),(x+8,y-4))
    def truck(self, forward_cab=False):
        self.box(18,48,190,19,3)
        if self.stage>=2:
            if forward_cab:
                # Rear wall is left; sloping windshield and nose face right.
                self.path([(157,67),(157,108),(185,108),(204,87),(204,67)])
                self.path([(165,85),(165,100),(181,100),(194,85)])
            else:
                self.path([(157,67),(157,87),(177,108),(204,108),(204,67)])
                self.path([(167,85),(181,100),(195,100),(195,85)])
            for xx in (44,79,181):self.wheel(xx,32,17,53)
        if self.stage>=4:
            self.box(183,71,12,4);self.line((163,75),(172,75));self.box(25,54,9,5)
    def crawler(self):
        self.box(25,47,125,24,4)
        if self.stage>=2:self.track(29,20,116,50)
    def compact(self):
        self.box(27,48,129,22,4)
        if self.stage>=2:
            self.wheel(53,33,18,53);self.wheel(130,33,18,53)
    def blade(self,points):self.path(points)


def draw(c,tool,stage):
    a=Art(c,stage)
    if tool in ('dump','mixer','crane','pump','snow','sweep','tow','fire','logs'):
        a.truck(forward_cab=tool=='fire')
        if tool=='dump':
            if stage>=3:a.path([(23,68),(142,68),(145,116),(43,130),(29,116)])
            if stage>=4:
                for x in (50,75,100,125):a.line((x,75),(x+5,119-(x-50)*.14))
                a.line((29,76),(140,76));a.pin((141,69))
        elif tool=='mixer':
            if stage>=3:
                a.box(39,67,100,10);a.path([(43,85),(58,117),(102,128),(138,106),(139,86),(111,77),(69,77)])
                a.path([(43,85),(22,72),(10,56),(19,54),(32,70),(54,80)])
            if stage>=4:
                a.line((63,80),(84,121));a.line((93,78),(115,118));a.pin((128,89))
        elif tool=='crane':
            if stage>=3:
                a.box(66,67,65,17,3);a.beam((100,85),(188,164),15)
                a.line((188,164),(216,164),(216,106));a.hook(216,106)
                a.pin((100,85),5)
            if stage>=4:
                a.box(40,68,25,18);a.beam((107,78),(146,120),5)
                a.line((158,138),(167,128))
                for x in (34,146):a.beam((x,56),(x,17),5);a.box(x-8,14,16,3)
        elif tool=='pump':
            if stage>=3:
                a.box(73,67,45,19);a.beam((99,86),(130,148),9)
                a.beam((130,148),(173,114),9);a.beam((173,114),(204,160),8)
                a.line((204,160),(223,160),(223,95),(219,84))
            if stage>=4:
                for p in ((99,86),(130,148),(173,114),(204,160)):a.pin(p)
                for x in (35,143):a.beam((x,57),(x-7,17),5);a.box(x-14,14,16,3)
                a.box(82,71,25,10)
        elif tool=='snow':
            if stage>=3:
                a.box(38,67,98,30,3);a.beam((198,53),(217,36),8)
                a.path([(215,62),(234,67),(231,17),(207,17)])
            if stage>=4:
                a.line((218,24),(229,24));a.pin((216,39));a.vents(52,78,5)
        elif tool=='sweep':
            if stage>=3:
                a.path([(36,67),(44,109),(132,109),(151,67)])
                # Hanging brush motors and bristle skirts, joined to the frame.
                for x in (101,136):
                    a.beam((x,49),(x,28),6);a.box(x-9,23,18,6,2)
                    a.path([(x-9,23),(x+9,23),(x+15,14),(x-15,14)])
            if stage>=4:
                for x in (101,136):
                    for dx in (-9,-3,3,9):a.line((x+dx*.65,21),(x+dx,15))
                a.box(51,80,51,14);a.line((44,103),(131,103))
        elif tool=='tow':
            if stage>=3:
                a.box(83,67,58,13,3);a.beam((105,80),(24,143),12)
                a.line((24,143),(12,143),(12,87));a.hook(12,87);a.pin((105,80),4)
            if stage>=4:
                a.beam((102,70),(67,106),5);a.pin((67,106));a.box(32,68,34,9)
        elif tool=='fire':
            if stage>=3:
                a.box(25,67,122,41,3);a.box(32,112,116,8)
                a.beam((40,108),(40,112),4);a.beam((132,108),(132,112),4)
            if stage>=4:
                for x in (29,62,95):a.box(x,73,29,27)
                a.circle(77,87,9);a.circle(77,87,5)
                for x in range(40,143,12):a.line((x,113),(x,119))
                a.box(164,108,16,5,2)
        elif tool=='logs':
            if stage>=3:
                for y in (67,81,95):a.box(29,y,117,14,7)
                a.box(25,66,4,51);a.box(146,66,4,51)
            if stage>=4:
                for y in (74,88,102):a.circle(139,y,5);a.circle(139,y,2)
                a.line((86,69),(86,111))
        return
    if tool in ('blade','trencher','drill','pile','lattice'):
        a.crawler()
        if stage>=2:a.cab(64,71,40,40)
        if tool=='blade':
            if stage>=3:
                a.beam((121,58),(183,33),10)
                a.path([(180,66),(207,69),(212,16),(181,16)])
            if stage>=4:
                a.beam((143,65),(187,47),5);a.pin((143,65));a.line((187,24),(207,24))
                a.box(31,72,31,18);a.vents(37,78)
        elif tool=='trencher':
            if stage>=3:
                a.beam((145,63),(215,26),23);a.pin((145,63),6);a.pin((215,26),6)
            if stage>=4:
                a.beam((145,63),(215,26),8)
                for k in range(1,7):
                    t=k/7;x=145+70*t;y=63-37*t
                    a.circle(x-5,y-10,2);a.circle(x+5,y+10,2)
                a.vents(113,57,4)
        elif tool in ('drill','pile'):
            if stage>=3:
                a.beam((143,56),(169,65),12);a.box(164,22,16,139)
                a.beam((129,65),(164,113),6);a.box(160,108,24,21)
                a.beam((172,108),(172,14),6 if tool=='drill' else 10)
            if stage>=4:
                a.pin((166,112));a.line((168,134),(168,157))
                if tool=='drill':
                    for y in range(25,101,12):a.line((168,y),(176,y+7))
                else:a.box(162,106,20,26);a.line((168,111),(176,111))
        elif tool=='lattice':
            if stage>=3:
                # The two rails and every brace share interpolated endpoints.
                u=(111,89);v=(181,164);q=(125,78);r=(195,153)
                a.box(108,71,16,15);a.path([u,v,r,q]);a.pin((116,85),5)
                a.line((188,159),(218,159),(218,100));a.hook(218,100)
            if stage>=4:
                for k in range(6):
                    t=k/6;s=(k+1)/6
                    top=(111+70*t,89+75*t);bot=(125+70*t,78+75*t)
                    top2=(111+70*s,89+75*s);bot2=(125+70*s,78+75*s)
                    a.line(top,bot2);a.line(bot,top2)
                a.box(29,72,31,17)
        return
    if tool=='tower':
        a.box(70,14,70,10);a.box(93,24,24,102)
        if stage>=2:
            for y in range(24,108,17):a.line((93,y),(117,y+17));a.line((117,y),(93,y+17))
            a.box(87,126,35,8);a.box(118,114,23,19);a.box(124,119,11,9)
        if stage>=3:
            a.box(20,134,205,11);a.path([(99,145),(105,169),(112,145)])
            a.line((105,169),(25,145));a.line((105,169),(220,145))
            a.box(176,129,13,5);a.line((183,129),(183,57));a.hook(183,57)
        if stage>=4:
            for x in range(20,219,17):a.line((x,134),(x+17,145))
            for x in (26,39,52):a.box(x,115,11,19)
        return
    if tool in ('loader','shortbucket','backhoe','fork','tele','scissor','boomlift'):
        a.compact()
        if stage>=2:
            if tool in ('scissor','boomlift'):pass
            elif tool=='fork':
                a.box(68,70,4,49);a.box(107,70,4,49);a.box(65,119,49,4)
                a.box(81,73,19,7);a.box(80,80,5,18)
            else:a.cab(65,70,39,43)
        if tool in ('loader','shortbucket'):
            if stage>=3:
                a.box(104,68,11,10);a.beam((109,76),(170,78),10);a.beam((170,78),(187,43),9)
                a.path([(182,51),(198,36),(225,36),(222,20),(183,25)])
                a.pin((109,76));a.pin((170,78));a.pin((187,43))
            if stage>=4:
                a.beam((132,57),(170,78),5)
                for x in (199,207,215):a.path([(x,23),(x+6,20),(x+3,17)])
                if tool=='shortbucket':
                    for x in (77,84,91):a.line((x,81),(x+2,103))
        elif tool=='backhoe':
            if stage>=3:
                # Rear excavating arm on the right; front bucket on the left.
                a.beam((143,63),(174,131),12);a.beam((174,131),(204,94),11)
                a.beam((204,94),(206,61),10)
                a.path([(205,65),(225,56),(218,39),(197,45)])
                a.beam((43,63),(18,43),8)
                a.path([(18,48),(9,46),(9,23),(34,23),(31,32)])
            if stage>=4:
                for p in ((143,63),(174,131),(204,94),(206,61)):a.pin(p)
                a.beam((151,65),(171,113),4);a.beam((37,58),(22,41),4)
        elif tool=='fork':
            if stage>=3:
                a.beam((146,61),(173,62),10);a.box(168,28,8,105);a.box(179,28,5,105)
                a.box(167,47,18,17);a.path([(181,60),(188,60),(188,42),(228,42),(228,37),(181,37)])
            if stage>=4:
                a.line((173,70),(173,126));a.pin((159,63));a.vents(35,57,4)
        elif tool=='tele':
            if stage>=3:
                a.beam((124,70),(198,126),13);a.pin((124,70),5)
                a.box(196,87,8,41);a.path([(200,97),(207,97),(207,81),(232,81),(232,76),(200,76)])
            if stage>=4:
                # A cylinder joins the chassis to the lifting boom.
                a.beam((139,59),(174,105),5);a.pin((139,59));a.pin((174,105))
                a.line((177,118),(184,108))
        elif tool=='scissor':
            if stage>=3:
                for y in (70,97):a.beam((58,y),(132,y+27),5);a.beam((132,y),(58,y+27),5)
                a.box(44,124,104,7)
                a.box(47,131,98,30,0)
            if stage>=4:
                for y in (83.5,110.5):a.pin((95,y))
                for x in (69,94,119):a.line((x,132),(x,160))
        elif tool=='boomlift':
            if stage>=3:
                a.box(75,70,32,12,3);a.beam((93,82),(128,136),10)
                a.beam((128,136),(179,103),9);a.beam((179,103),(189,111),7)
                # Closed basket floor and rails, directly attached to the jib.
                a.box(187,108,47,6);a.box(189,114,43,32)
            if stage>=4:
                for p in ((93,82),(128,136),(179,103)):a.pin(p)
                for x in (203,218):a.line((x,115),(x,145))
                a.beam((103,79),(122,122),4)
        return
    if tool=='roller':
        a.box(30,52,132,19,3)
        if stage>=2:
            a.wheel(57,33,18,58);a.cab(75,71,37,40)
            a.beam((153,60),(177,40),10);a.circle(180,38,23);a.circle(180,38,6)
        if stage>=3:a.box(117,71,33,20,3);a.beam((157,66),(180,38),6);a.pin((180,38))
        if stage>=4:a.vents(124,76)
        return
    if tool in ('paver','mill'):
        a.box(34,47,139,29,4)
        if stage>=2:
            a.track(39,20,50,49);a.track(119,20,50,49)
            a.box(87,76,47,25);a.box(96,82,14,13)
        if tool=='paver':
            if stage>=3:
                a.path([(34,72),(14,91),(59,91),(72,76)])
                a.beam((161,59),(197,33),9);a.path([(186,42),(222,42),(227,18),(188,18)])
                a.box(93,101,4,36);a.box(136,76,4,61);a.box(90,137,53,4)
            if stage>=4:a.line((191,24),(224,24));a.vents(44,57,5)
        else:
            if stage>=3:
                a.box(89,24,30,23,5)
                a.beam((163,70),(221,132),13);a.pin((163,70),4)
            if stage>=4:
                # Only a pinned support cylinder; no free trailing hook.
                a.beam((154,58),(187,96),5);a.pin((154,58));a.pin((187,96))
                for x in (94,101,108,115):a.line((x,25),(x,32))
                a.vents(140,60,4)
        return
    if tool=='grader':
        a.path([(20,68),(149,68),(149,81),(205,81),(212,56),(20,56)])
        if stage>=2:
            a.wheel(35,31,16,60);a.wheel(177,31,16,61);a.wheel(211,31,16,61)
            a.cab(113,68,36,42)
        if stage>=3:
            a.beam((97,62),(92,38),7);a.beam((134,62),(145,30),5)
            a.path([(74,41),(154,29),(157,21),(76,31)])
        if stage>=4:a.pin((97,62));a.vents(158,67,6);a.line((77,33),(154,22))
        return
    if tool=='scraper':
        a.box(20,56,195,14,3)
        if stage>=2:
            a.wheel(48,34,19,62);a.wheel(192,34,19,62);a.cab(27,70,40,41)
        if stage>=3:
            a.path([(79,70),(174,70),(166,39),(88,39)])
            a.beam((62,67),(88,60),8);a.beam((166,60),(191,63),7)
        if stage>=4:a.line((89,47),(164,47));a.pin((88,60));a.pin((166,60));a.line((101,43),(114,61),(144,61))
        return
    if tool=='tractor':
        a.path([(37,59),(45,77),(111,77),(120,94),(187,94),(201,78),(201,59)])
        if stage>=2:
            a.cab(62,77,48,49)
            a.wheel(71,39,24,68);a.wheel(177,31,16,68)
        if stage>=3:
            a.box(145,94,5,33);a.box(145,124,13,4)
            # Closed drawbar connected to the rear; no loose left-hand stroke.
            a.box(23,58,18,7);a.circle(27,61.5,1.8)
        if stage>=4:a.vents(170,78,4);a.box(118,68,24,14);a.line((115,78),(136,78))
        return
    if tool=='combine':
        a.path([(23,60),(29,107),(105,116),(112,102),(166,102),(166,60)])
        if stage>=2:
            # Cab sits flush on the front deck; windshield faces the header.
            a.path([(112,102),(112,142),(148,142),(166,102)])
            a.box(118,112,13,22)
            a.path([(137,112),(137,134),(144,134),(154,112)])
            a.wheel(56,32,17,70);a.wheel(140,39,24,75)
        if stage>=3:
            a.beam((157,77),(188,46),16)
            a.path([(177,50),(231,50),(234,24),(176,24)])
            a.beam((183,49),(208,65),5);a.circle(208,65,16);a.pin((208,65))
        if stage>=4:
            for ang in (0,math.pi/3,2*math.pi/3):
                dx=14*math.cos(ang);dy=14*math.sin(ang);a.line((208-dx,65-dy),(208+dx,65+dy))
            for x in range(178,228,8):a.path([(x,24),(x+4,17),(x+8,24)])
            a.box(39,78,37,14);a.vents(88,89,4)
        return
    raise ValueError('No machine geometry for '+tool)

LESSON_LABELS={
'dump':['Draw the truck frame','Add cab and tires','Build the tipping bed','Add ribs and hinge'],
'blade':['Draw the crawler body','Add tracks and cab','Attach the pushing blade','Add cylinder and engine'],
'arm':['Draw tracks and rollers','Add body and glass cab','Build the digging arm','Add pistons and teeth'],
'loader':['Draw the loader frame','Add tires and cab','Join lift arms and bucket','Add cylinder and teeth'],
'roller':['Draw the frame','Mount tire, drum, and cab','Add engine and drum fork','Finish vents and axle'],
'mixer':['Draw the truck frame','Add cab and tires','Mount drum and chute','Add drum bands and pins'],
'fork':['Draw the low body','Add tires, seat, and guard','Mount mast and forks','Add guides and hinge'],
'shortbucket':['Draw the compact frame','Add tires and cab','Mount arms and bucket','Add cylinder and cab bars'],
'backhoe':['Draw the main frame','Add tires and cab','Attach both working ends','Add pivots and cylinders'],
'crane':['Draw the truck frame','Add cab and tires','Mount boom and hook','Add cylinder and stabilizers'],
'tower':['Draw foundation and mast','Add mast braces and cab','Build jib and hoist','Add weights and bracing'],
'paver':['Draw the paver body','Mount tracks and controls','Add hopper and screed','Finish screed and vents'],
'grader':['Draw the closed frame','Mount tires and cab','Attach the center blade','Add joints and engine vents'],
'trencher':['Draw the crawler body','Mount tracks and cab','Attach the chain boom','Add chain and cutting teeth'],
'scraper':['Draw the long frame','Mount tires and cab','Build the soil bowl','Add blade and hinges'],
'tele':['Draw the carrier','Mount tires and cab','Attach boom and forks','Add lift cylinder and seam'],
'scissor':['Draw the low base','Mount the wheels','Build scissors and platform','Add pins and guardrails'],
'boomlift':['Draw the low base','Mount the wheels','Join arms and work basket','Add pivots and basket rails'],
'pump':['Draw the truck frame','Add cab and tires','Join boom and delivery hose','Add joints and stabilizers'],
'drill':['Draw the crawler body','Mount tracks and cab','Connect mast and drill','Add guide and spiral flutes'],
'pile':['Draw the crawler body','Mount tracks and cab','Connect mast and pile','Add hammer and guide'],
'mill':['Draw the machine body','Mount tracks and controls','Attach drum and conveyor','Add support and cutter teeth'],
'snow':['Draw the truck frame','Add cab and tires','Mount body and plow blade','Add hinge and blade edge'],
'sweep':['Draw the truck frame','Add cab and tires','Mount hopper and brushes','Add bristles and service hatch'],
'tow':['Draw the truck frame','Add cab and tires','Mount rear boom and hook','Add cylinder and toolbox'],
'fire':['Draw the truck frame','Add cab and tires','Build body and ladder','Add hose reel and lockers'],
'tractor':['Shape frame and hood','Mount cab and both tires','Add exhaust and rear hitch','Add grille and access panel'],
'combine':['Shape the grain body','Mount cab and both tires','Connect header and reel','Add reel spokes and teeth'],
'logs':['Draw the long carrier','Add cab and tires','Stack logs inside stakes','Add rings and load strap'],
'lattice':['Draw the crawler body','Mount tracks and cab','Attach boom and hoist','Add bracing and counterweight'],
}
