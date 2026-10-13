"""A practical 90-day deacon field guide. Original prose and templates."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether,CondPageBreak,Table,TableStyle,HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor,white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from xml.sax.saxutils import escape
import fitz

pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
OUT=Path('dist/books/guide-deacon');OUT.mkdir(parents=True,exist_ok=True)
INK=HexColor('#213747');TEAL=HexColor('#137C81');MUTED=HexColor('#526875');GOLD=HexColor('#DA9B34')
TITLE='The First 90 Days as a Church Deacon'
SUB='A Biblical, Practical Guide to Serving the Pastor, Church, and Community'
W,H=432,648 # 6 x 9 inches
style={
 'title':ParagraphStyle('title',fontName='DejaVu-Bold',fontSize=24,leading=30,textColor=INK,spaceAfter=18),
 'subtitle':ParagraphStyle('subtitle',fontName='DejaVu',fontSize=11.5,leading=17,textColor=TEAL,spaceAfter=17),
 'h1':ParagraphStyle('h1',fontName='DejaVu-Bold',fontSize=19,leading=24,textColor=INK,spaceAfter=15),
 'h2':ParagraphStyle('h2',fontName='DejaVu-Bold',fontSize=11.5,leading=16,textColor=TEAL,spaceBefore=12,spaceAfter=6),
 'body':ParagraphStyle('body',fontName='DejaVu',fontSize=9.8,leading=15,textColor=INK,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='DejaVu',fontSize=8.7,leading=13,textColor=MUTED,spaceAfter=8),
 'bullet':ParagraphStyle('bullet',fontName='DejaVu',fontSize=9.4,leading=14,textColor=INK,leftIndent=15,firstLineIndent=-9,spaceAfter=6),
}

weeks=[
('Listen before acting','Acts 6:1-7; 1 Timothy 3:8-13',
 'Ask your pastor or chair how your congregation describes a deacon\'s work. Read the bylaws and any current ministry policies. Ask which responsibilities are shared with staff, committees, and other volunteers. A willing servant can still create confusion by promising help that someone else has already arranged.',
 'Make a short map of who receives requests, who may approve spending, who may speak for the church, and who follows up. Keep your own first-week notes private. Meet one experienced deacon and ask for a concrete example of good follow-through. Ask a member where care is working well before asking where it has failed.',
 'A member says, “Can you tell the pastor that our class needs a new room?” Answer: “I can pass on the request and find out who makes that decision. I will tell you when I have an answer.” Record the request and date. Do not promise the room.',
 'Who has authority to assign this task? What can I promise today?'),
('Know the biblical shape of service','Mark 10:42-45; 1 Timothy 3:8-13',
 'The New Testament emphasizes tested character and trustworthy service. Do not treat the title as a supervisory rank or a reward for attendance. A deacon serves alongside other members, under the congregation\'s own governance. Acts 6 describes a distribution problem answered by selecting trusted servants; churches differ on how directly they connect that episode to the later office.',
 'Read the passages slowly and list traits that would be visible at home, at work, and in church. Ask whether your conduct makes difficult conversations safer. Speak truthfully, decline gossip, handle money carefully, and keep your commitments. The daily test is often reliability in small matters.',
 'A friend asks what confidential issue the deacons discussed. Say: “We are working on it, but I cannot share another person\'s details. If the church needs to announce a decision, the right person will do that.”',
 'Does this action serve a person or protect my position?'),
('Build a prayer and contact rhythm','James 5:13-16; Philippians 1:3-6',
 'Prayer can be steady without becoming a performance. Ask people what they are comfortable sharing and whether a name may be circulated. A request for prayer is not consent to broadcast a diagnosis. Establish a small list of people assigned to your care and a dependable time to make contact.',
 'Schedule two brief check-ins, one pastor check-in, and time for your own family. Use a contact method each member prefers. If no answer comes, leave a simple message and try once later. Keep only the minimum facts needed for follow-through; avoid collecting sensitive detail in a shared spreadsheet.',
 'A member texts, “Please pray; I am at the hospital, but do not tell anyone yet.” Reply: “I will pray. I will keep this private. Would you like a call or help contacting a family member?”',
 'Did I ask what can be shared, with whom, and when?'),
('Visit without taking over','Matthew 25:35-40; Romans 12:15',
 'A useful visit begins with permission. Ask if a visit is welcome, whether the person has energy for it, and what time works. In a hospital, follow the facility\'s rules, hygiene requests, and visitor limits. A quiet presence can be more helpful than a long explanation of why suffering happened.',
 'Introduce yourself to the patient and caregiver. Ask one open question, listen, and offer a short prayer only if wanted. Do not interpret symptoms, promise recovery, discuss medicines, or interfere with clinicians. Offer a concrete next action such as a meal, ride, or call through the church\'s normal process.',
 'If a caregiver says, “We are exhausted,” try: “That sounds hard. What task would make this week easier? I can check what help our church can arrange.” Then make exactly that follow-up.',
 'Did I leave with a clear next action and the person\'s permission?'),
('Guard privacy and trust','Proverbs 11:13; Ephesians 4:25-32',
 'Ministry is not a reason to circulate private information. Discuss a care need only with the people who must act. Follow your church\'s child protection, safeguarding, and records policies. When someone describes abuse, threats, or immediate danger, use the church\'s safety process and applicable reporting requirements; do not promise secrecy that you cannot keep.',
 'Separate a brief service record from personal impressions. Record the date, the help requested, the approved action, and who owns the next step. Avoid diagnoses, rumor, and speculation. Store notes securely and remove them when no longer needed under church policy.',
 'A volunteer asks why a family received help. Answer: “I cannot discuss their situation. I can explain how our church reviews requests generally.”',
 'Would I be comfortable if the person read what I recorded?'),
('Respond to a practical need','Galatians 6:2; 1 John 3:16-18',
 'Care requests deserve both compassion and a reliable process. Clarify the immediate need, timing, available community resources, and what the church may authorize. Financial help can involve fraud risk or conflicts of interest. Never personally promise church funds before the authorized decision maker has approved them.',
 'Use one request owner and a date for follow-up. Ask what the person has already tried without making the conversation an interrogation. For rent, utilities, food, transportation, or repairs, connect the person to the appropriate ministry team and verify completion. If you cannot help, say so promptly and offer the next useful contact.',
 'A caller says the power will be cut off today. Ask for the deadline and the best callback number. Tell the designated benevolence contact immediately. Say, “I will call you by 3 p.m. with what I learn,” even if the answer may be no.',
 'Is the next step both authorized and time bound?'),
('Care for homebound members','Hebrews 10:24-25; Romans 12:10-13',
 'Homebound people can be overlooked when ministry is built around attendance. Ask whether they prefer a visit, call, card, or help joining worship. Learn who their regular caregiver is, but do not assume that a caregiver may speak for them or receive their information.',
 'Coordinate with the care team so one person does not receive six visits in a day while another receives none for a month. Ask about access, mobility, hearing, and visit length. Include the person in church news they want to receive. Record only agreed follow-ups, such as a ride inquiry or a phone call after an appointment.',
 'At the door, ask: “Is this still a good time? I can stay ten minutes or come back later.” The member, not the visitor, sets the pace.',
 'Who has not been contacted this month?'),
('Handle conflict without becoming a judge','Matthew 18:15-17; James 1:19',
 'A deacon may hear competing stories. Resist the urge to adjudicate from a hallway conversation. Listen without endorsing rumors; ask what the person wants to happen and what direct conversation has already occurred. Follow the church\'s process for disputes and refer pastoral or safeguarding concerns promptly.',
 'Separate facts you witnessed from what someone reported. State your limits: “I can listen and help identify the next appropriate conversation.” If two parties need a meeting, obtain consent and an appropriate facilitator. Do not promise that a conflict will be resolved quickly.',
 'Two members disagree about a ministry purchase. Summarize the shared goal, identify the policy and decision maker, and ask each to put a specific proposal in writing. A vote without clear facts is not a shortcut to peace.',
 'Am I carrying a message that should be spoken directly?'),
('Make meetings useful','1 Corinthians 14:40; Philippians 2:3-4',
 'Meetings should move care and service forward. Read the agenda, minutes, and relevant policy before arriving. Bring facts, a proposed action, a cost if applicable, and a named owner. Care stories should be anonymized when possible. Matters needing confidentiality belong in the proper setting, not a group text.',
 'At the end of a meeting, restate decisions aloud: what was approved, who will act, by when, and who will communicate with the affected person. Send a concise record to the agreed channel. If no decision was made, record the next information needed and the date it will be gathered.',
 'Instead of “We should help the Smith family,” propose: “May I arrange two meals through the care team by Friday, after confirming the family wants them?”',
 'Will someone know what to do tomorrow morning?'),
('Support the pastor without overloading him','Hebrews 13:17; 1 Peter 5:2-3',
 'Ask the pastor what information is genuinely useful and what can be handled by the assigned team. Support includes truthful feedback, prayer, practical help, and healthy boundaries. It does not require agreement with every preference or using deacon meetings to manage the pastor by rumor.',
 'Build a brief update rhythm: urgent concerns immediately, ordinary care needs at a predictable time, and completed work in a short summary. When offering criticism, state the observed issue, its effect, and one constructive question. Respect the pastor\'s time and family commitments.',
 'Try: “Three families asked about transportation. The care team can coordinate volunteers. Are there pastoral concerns we should account for before we do that?”',
 'Am I bringing a decision, a fact, or just anxiety?'),
('Serve beyond the building','Matthew 5:13-16; Luke 10:25-37',
 'A church can notice local needs without pretending it can solve all of them. Learn what trusted local agencies already do. Ask ministry leaders where the congregation has capacity, and design service with the people affected rather than for them without listening.',
 'Choose one bounded opportunity: a food delivery partnership, a school supply request, a maintenance day, or a neighbor visit. Clarify insurance, safeguarding, transportation, funding, and the volunteer leader before announcing it. Count completed service, not only sign-ups.',
 'A community partner requests twenty volunteers next weekend. Say: “I will check our capacity and give you a firm number tomorrow.” An honest five is better than a promised twenty who do not arrive.',
 'What existing relationship can we strengthen?'),
('Prepare a durable handoff','2 Timothy 2:2; Colossians 3:23-24',
 'No ministry should depend on one person\'s memory. Make recurring tasks easy to understand without exposing private stories. A useful handoff tells a successor the purpose, decision path, contacts by role, normal timing, and where approved records are kept.',
 'Review your active commitments: completed, waiting, or needing escalation. Verify with the person served that a new contact is welcome before transferring details. Ask whether the process can be simplified. A deacon who records the next step serves beyond the current term.',
 'A volunteer moves away while coordinating meal deliveries. Transfer only the household\'s current preferences and upcoming commitment through the authorized team, not months of private messages.',
 'If I were absent for a month, what would stop?'),
('Review the first 90 days','Psalm 90:12; Philippians 1:9-11',
 'The goal of the first 90 days is a faithful rhythm, not an impressive list. Reflect on reliability, prayer, listening, family balance, respect for others\' roles, and whether care requests receive a real response. Ask your pastor and one fellow deacon for a specific improvement.',
 'Choose two practices to keep, one to stop, and one to learn. Close old promises or transfer them clearly. Thank volunteers by name with appropriate privacy. Set a sustainable calendar for the next quarter and leave room for unexpected needs.',
 'In the review meeting, say: “I followed up on eight assigned requests, missed one deadline, and changed my reminder process. I need help learning our benevolence policy.” That honesty is more useful than a polished report.',
 'Who is better cared for because I followed through?'),
]
daily=[
['Read Acts 6 and the church bylaws.','Ask the chair to explain approval paths.','Find the safeguarding contact.','Meet an experienced deacon.','List active requests and owners.','Follow up on one open promise.','Review who may speak for the church.'],
['Read the deacon qualifications in context.','Ask where you need more consistency.','Practice a truthful response to a rumor.','Check your household commitments.','Serve in an unnoticed task.','Thank a fellow volunteer.','Reflect on character before title.'],
['Ask two people for contact preferences.','Confirm consent before sharing prayer.','Make one brief care call.','Record the promised next step securely.','Give the pastor a useful update.','Check back on an older request.','Pray and protect a family rest period.'],
['Ask permission for a visit.','Check facility rules or home access.','Prepare one open question.','Visit and listen without rushing.','Offer one practical next action.','Coordinate with the care team.','Check whether the action happened.'],
['Review the church privacy policy.','Remove unnecessary detail from notes.','Learn the abuse escalation path.','Practice a response to gossip.','Check access to shared records.','Ask whether consent covers a request.','Close a record that is no longer needed.'],
['Locate the benevolence policy.','Identify who approves an expense.','Practice documenting a deadline.','Identify one community resource.','Follow up with an applicant on time.','Check for unfinished requests.','Review one case without private detail.'],
['Review the homebound contact list.','Ask each person about preferred contact.','Coordinate visits across the care team.','Make one short call or visit.','Share desired church news.','Check a caregiver need with permission.','Confirm next month\'s contact plan.'],
['Read the conflict process.','Practice separating fact from report.','Listen without carrying a rumor.','Ask what outcome is sought.','Refer safety concerns promptly.','Help plan a direct conversation.','Check whether a next step is owned.'],
['Read the agenda before meeting.','Gather facts for one open item.','Name the decision being requested.','Attend and listen for action owners.','Confirm decisions and deadlines.','Send an authorized concise update.','Close or carry forward each item.'],
['Ask the pastor\'s update preference.','Send only an urgent item urgently.','Summarize routine needs clearly.','Offer one practical help request.','Give constructive feedback privately.','Protect the pastor\'s family time.','Review the next update cadence.'],
['Meet a trusted community partner.','Ask what help is already working.','Choose one bounded service idea.','Check policy and volunteer capacity.','Confirm owner, cost, and timing.','Serve with the affected people.','Measure completed help, not sign-ups.'],
['List recurring tasks you own.','Find current instructions and contacts.','Close one old promise.','Transfer one task with permission.','Remove unneeded private messages.','Ask a successor to test the process.','Correct an unclear handoff.'],
['List completed and open commitments.','Ask the pastor for one improvement.','Ask another deacon for feedback.','Choose two habits to keep.','Choose one task to stop or share.','Set next quarter\'s calendar.','Thank the people who served with you.'],
]

def P(s,kind='body'):return Paragraph(escape(s),style[kind])
def para(s,kind='body'):story.append(P(s,kind))
def bullet(s):story.append(Paragraph('&#8226; '+escape(s),style['bullet']))
def br(n=1):story.append(Spacer(1,n*8))
def newpage():story.append(PageBreak())

story=[]
para(TITLE,'title');para(SUB,'subtitle');br(5);para('A 13-week field guide for humble, dependable service','h2')
para('Heath Tolley','body')
para('This guide is an original practical resource. It is not a substitute for your church\'s bylaws, safeguarding policy, pastoral direction, or applicable law. Scripture references invite readers to open a Bible and read each passage in context.','small')
newpage()
para('How to use this field guide','h1')
para('Each week gives a Scripture reading, a concrete service task, a worked situation, and a question for self-examination. Begin at week one even if you have served before: clarifying how this congregation makes decisions prevents duplicated or unauthorized work. Use the reference pages when a real request arrives.','body')
para('A simple weekly rhythm','h2')
for s in ['Read the listed passages in context and pray before contacting anyone.','Check the assigned care list and follow up on earlier promises.','Complete one small service task that someone actually requested.','Tell the correct person what was done and what remains open.','Protect your household schedule so service remains sustainable.']:bullet(s)
para('A promise tracker can be as simple as date, person or request code, consent to share, next step, owner, deadline, and completion. Keep it within the church\'s approved system; this book should not contain personal medical or financial information.','body')
newpage()
para('Before day one: clarify your role','h1')
for h,b in [
 ('Ask for the current documents','Get bylaws, deacon ministry description, benevolence policy, child and vulnerable-adult safeguarding procedures, spending approvals, and the church\'s preferred contact channel.'),
 ('Agree on decision rights','A deacon can notice needs and propose action. Only the authorized person or group can approve spending, speak for the church, share private information, or change policy.'),
 ('Choose a safe record','Store just enough information to complete a task. Do not put diagnoses, account numbers, passwords, or unverified stories in a general meeting packet.'),
 ('Name an escalation route','Know whom to call when a person is at risk, a report is required, an expense is urgent, or a concern involves a leader.')]:para(h,'h2');para(b)
newpage()
para('Thirteen weeks at a glance','h1')
for i,(name,*_) in enumerate(weeks):
 para('Week '+str(i+1).zfill(2)+'  '+name,'small')
newpage()
for i,(name,ref,learn,do,case,question) in enumerate(weeks):
 story.append(CondPageBreak(170))
 para('WEEK '+str(i+1).zfill(2)+'  /  DAYS '+str(i*7+1)+'-'+str(min(90,(i+1)*7)),'small')
 para(name,'h1');para('READ  '+ref,'subtitle')
 para('What to understand','h2');para(learn)
 para('This week in practice','h2');para(do)
 para('A situation to work through','h2');para(case)
 para('Seven small actions','h2')
 for day,task in enumerate(daily[i][:6] if i==12 else daily[i]):bullet('Day '+str(i*7+day+1)+': '+task)
 para('Ask yourself','h2');para(question)
 if i<12:br(2)
br(3)
para('A ten-minute care call','h1')
for h,b in [
 ('Before','Check permission to call. Read only the current assignment. Find a private place to speak. Know the limits of what the church has authorized.'),
 ('Open','“Hello, this is [name] from [church]. Is this a good time for a short check-in?” If the answer is no, offer a later time.'),
 ('Listen','“How has this week been for you?” and “Is there one practical need you would like help with?” Do not rush to solve a problem you have not understood.'),
 ('Confirm','“May I share this request with the care coordinator? What details may I include?” Repeat the agreed next step and deadline.'),
 ('Close','“I will contact [role] today and update you by [time]. Would prayer be welcome?” After the call, record only the agreed service facts.')]:para(h,'h2');para(b)
br(3)
para('A visit in a hospital or home','h1')
para('Arrange the visit through the patient or caregiver. Check the hospital\'s current visitor rules. Use required infection-control measures. Be ready to leave promptly when a nurse, clinician, or family member needs the room. A person who is unwell may appreciate five attentive minutes more than forty minutes of conversation.','body')
for s in ['Ask whether the visit is still wanted when you arrive.','Listen before offering a Scripture passage, prayer, or practical help.','Do not give medical interpretations or promise a particular outcome.','Do not post photos or updates without explicit consent and church approval.','Clarify the next action and who owns it.']:bullet(s)
para('If the person requests urgent medical help, use the facility staff or emergency service rather than trying to manage the problem yourself.','body')
br(3)
para('When a member is grieving','h1')
para('Loss changes what people can absorb. Offer a calm presence and a specific next action: a meal at an agreed time, a ride, help with a service, or a later check-in. Ask who is coordinating the family\'s wishes. Do not assume they want visitors, a public prayer request, or a social media tribute.','body')
para('A useful sentence','h2');para('“I am sorry for your loss. I can sit with you, or I can help with a practical task. Which would serve you best today?”')
para('A follow-through plan','h2');para('The first week often brings attention. Consider a call several weeks later after visitors have gone home. Record the promised date privately and honor it. Coordinate with the pastor and care team so help does not become a parade of unplanned contacts.')
br(3)
para('Benevolence without confusion','h1')
para('Use your church\'s policy. A fair process identifies the request, deadline, documentation needed, decision maker, available resources, and how the outcome is communicated. It protects both the person asking and the people entrusted with church funds.','body')
for s in ['Ask what is due, when, and how the bill can be verified.','Explain the review process without suggesting that approval is certain.','Avoid handling cash or private account information outside approved channels.','Consider practical or community assistance when a payment is not possible.','Confirm a decision and close the loop by the promised time.']:bullet(s)
para('Worked example','h2');para('A family requests help with a $180 utility bill due Friday. On Tuesday, the deacon gathers the deadline and consent to contact the benevolence team. The authorized team reviews the policy and decides on Wednesday. The family is told the result that day, leaving time to call the utility company if needed.')
br(3)
para('Confidentiality decision tree','h1')
for h,b in [
 ('Is someone in immediate danger?','Use emergency services or the church\'s safeguarding route. Never promise absolute secrecy.'),
 ('Is there a reporting duty or policy?','Follow applicable law and church procedure. Ask the designated safeguarding leader if unsure.'),
 ('Does another person need details to act?','Ask what minimum facts they need and whether the person served has consented, where consent is appropriate.'),
 ('Is this curiosity, gossip, or broad distribution?','Do not share. A prayer request can be general without naming private circumstances.')]:para(h,'h2');para(b)
br(3)
para('A meeting that ends with action','h1')
para('Before the meeting, read the agenda and send factual updates to the chair. During the meeting, identify the decision requested. After discussion, repeat the actual outcome: approved, declined, referred, or awaiting information. Record an owner and deadline for each open item.','body')
para('Example action record','h2')
for s in ['Need: transportation for three appointments next month.','Consent: member agreed to be contacted by the rides coordinator.','Decision: care team may recruit vetted drivers under church policy.','Owner: rides coordinator. Deadline: call the member by Thursday.','Review: confirm the first ride happened before closing the item.']:bullet(s)
para('Avoid recording the member\'s unrelated medical history in the meeting minutes.','small')
br(3)
para('A difficult conversation','h1')
para('When someone complains about another leader, seek clarity without becoming a messenger for accusations. Ask what happened, what was directly observed, and whether the person has spoken with the other party. If there is a safety issue, use the safety route; otherwise, encourage the church\'s ordinary process for direct, respectful conversation.','body')
para('Language that keeps the door open','h2')
for s in ['“I hear that this matters to you. What outcome are you hoping for?”','“Which part did you witness yourself?”','“Would you be willing to raise this with the person involved?”','“I can help identify the appropriate next step, but I cannot promise the result.”']:bullet(s)
para('Do not conduct your own secret investigation. Document only what the right process requires.','small')
br(3)
para('A 90-day review page','h1')
para('Read your open commitments before answering these questions. If a promise remains unfinished, set a date and notify the person affected.','body')
for h in ['Where did I follow through reliably?','Which request waited too long?','What ministry am I doing that belongs to another person or team?','What did I learn from someone whose need was easy to overlook?','Which two habits will I keep next quarter?']:
 para(h,'h2');para('Write a short, specific answer in your own notes; protect people\'s private details.','small')
br(3)
para('Scripture and source notes','h1')
para('Read Scripture in your preferred translation. This book refers to passages rather than reproducing copyrighted Bible text. Acts 6:1-7, 1 Timothy 3:8-13, Mark 10:42-45, Romans 12:10-15, James 1:19, and Galatians 6:2 are central starting points. Interpret them with your congregation\'s teaching and in their surrounding context.','body')
para('The Baptist Faith and Message (2000), Article VI, describes a congregation\'s scriptural offices as pastor/elder/overseer and deacon. It also describes congregational accountability. Local church bylaws govern practical procedures; consult your own church leadership for those details.','body')
para('Further reading','h2')
for s in ['Southern Baptist Convention, The Baptist Faith and Message 2000: bfm.sbc.net/bfm2000/','LifeWay, Effective Pastor-Deacon Relationships: lifeway.com/articles/church-ministry-effective-deacon-pastor-relationships','Bible passages: Acts 6:1-7 and 1 Timothy 3:8-13 in a trusted Bible edition.']:bullet(s)
def decorate(c,doc):
 n=doc.page;c.saveState();c.setStrokeColor(TEAL);c.setLineWidth(1);c.line(42,612,390,612)
 c.setFont('DejaVu',7.5);c.setFillColor(MUTED);c.drawString(42,28,'THE FIRST 90 DAYS AS A CHURCH DEACON');c.drawRightString(390,28,str(n));c.restoreState()

target=OUT/'First_90_Days_Church_Deacon_Interior.pdf'
doc=SimpleDocTemplate(str(target),pagesize=(W,H),leftMargin=51,rightMargin=45,topMargin=53,bottomMargin=52,title=TITLE,author='Heath Tolley',pageCompression=1)
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
d=fitz.open(target);pages=len(d);print('pages',pages)
assert pages>=24
spine=pages*.002252;CW=(12.25+spine)*72;CH=9.25*72;front=6.125*72+spine*72
co=canvas.Canvas(str(OUT/'First_90_Days_Church_Deacon_Full_Wrap_Cover.pdf'),pagesize=(CW,CH),pageCompression=1)
co.setFillColor(INK);co.rect(0,0,CW,CH,stroke=0,fill=1)
co.setFillColor(TEAL);co.rect(0,0,6.125*72,CH,stroke=0,fill=1)
co.setFillColor(GOLD);co.rect(front+39,CH-91,92,7,stroke=0,fill=1)
for j,line in enumerate(['THE FIRST','90 DAYS','AS A CHURCH','DEACON']):
 co.setFillColor(white);co.setFont('DejaVu-Bold',26 if j!=2 else 23);co.drawString(front+39,CH-145-j*44,line)
co.setFont('DejaVu',11);co.drawString(front+39,CH-353,'A biblical, practical guide to serving');co.drawString(front+39,CH-372,'the pastor, church, and community')
co.setFillColor(GOLD);co.roundRect(front+39,128,345,59,6,stroke=0,fill=1)
co.setFillColor(INK);co.setFont('DejaVu-Bold',12);co.drawString(front+53,160,'13 WEEKS  /  REAL SITUATIONS')
co.drawString(front+53,141,'SCRIPTS  /  CARE TOOLS')
co.setFillColor(white);co.setFont('DejaVu',10);co.drawString(front+39,76,'Heath Tolley')
co.setFont('DejaVu-Bold',20);co.drawString(39,CH-138,'SERVE WITH CARE.')
co.drawString(39,CH-170,'FOLLOW THROUGH.')
co.setFont('DejaVu',10)
for j,s in enumerate(['Start with the biblical shape of service.','Work through 13 weekly priorities.','Practice visits, meetings, and difficult calls.','Protect privacy and finish what you promise.']):co.drawString(39,CH-233-j*28,s)
co.setFont('DejaVu-Bold',11);co.setFillColor(GOLD);co.drawString(39,CH-393,'A FIELD GUIDE FOR NEW DEACONS')
co.showPage();co.save()
print('cover inches',CW/72,CH/72)
