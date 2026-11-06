"""Render report-content.json with ReportLab. Document generation only; no Swift execution."""
from pathlib import Path
import json,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Preformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing,Rect,String
import reportlab
O=Path(__file__).resolve().parent
F=Path(reportlab.__file__).parent/'fonts'
for n,f in [('Body','Vera.ttf'),('BodyBold','VeraBd.ttf'),('BodyItalic','VeraIt.ttf'),('Mono','/System/Library/Fonts/Supplemental/Courier New.ttf')]:pdfmetrics.registerFont(TTFont(n,str((F/f) if (F/f).exists() else F/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('Helvetica',str(F/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('Times-Roman',str(F/'Vera.ttf')))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.2,leading=14.7,spaceAfter=9,textColor=colors.HexColor('#233044')),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8.1,leading=11.2,spaceAfter=6,textColor=colors.HexColor('#334155')),
 'h1':ParagraphStyle('h1',fontName='BodyBold',fontSize=21,leading=26,spaceAfter=16,textColor=colors.HexColor('#123653')),
 'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=12,leading=17,spaceBefore=9,spaceAfter=7,textColor=colors.HexColor('#126678')),
 'title':ParagraphStyle('title',fontName='BodyBold',fontSize=27,leading=32,spaceAfter=14,textColor=colors.HexColor('#123653')),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=8.4,leading=12,spaceAfter=10),
 'table':ParagraphStyle('table',fontName='Body',fontSize=8.1,leading=11.2),
 'tablehead':ParagraphStyle('tablehead',fontName='BodyBold',fontSize=8,leading=11,textColor=colors.white)}
pages=json.loads((O/'report-content.json').read_text())['pages']
def para(s,sty='body'):return Paragraph(s,styles[sty])
def diagram(rows):
 d=Drawing(470,136)
 for i,(n,title,detail) in enumerate(rows):
  y=99-i*44;d.add(Rect(0,y-8,470,40,fillColor=colors.HexColor('#edf6f8'),strokeColor=None));d.add(String(12,y+7,n,fontName='BodyBold',fontSize=12,fillColor=colors.HexColor('#126678')));d.add(String(40,y+15,title,fontName='BodyBold',fontSize=9.1));d.add(String(40,y,detail,fontName='Body',fontSize=8.3))
 return d
story=[]
for i,x in enumerate(pages):
 story.append(para(x['title'],'title' if i==0 else 'h1'))
 for z in x['blocks']:
  if z['type']=='paragraph':story.append(para(z['text'],z['style']))
  elif z['type']=='code':story.append(Preformatted(z['text'],styles['code']))
  elif z['type']=='timeline':story.append(diagram(z['rows']));story.append(Spacer(1,8))
  else:
   cells=[[para(html.escape(c),'tablehead') for c in z['headers']]]+[[para(str(c),'table') for c in row] for row in z['rows']]
   t=Table(cells,colWidths=z['widths'],repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#123653')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f0f5f7'),colors.white]),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#c4d1d9'))]));story.append(t);story.append(Spacer(1,9))
 if i<len(pages)-1:story.append(PageBreak())
def furniture(c,doc):
 c.setTitle('What Swift Concurrency Repairs Actually Guarantee');c.setAuthor('Ehsan Azish');c.setSubject('Technical report: bounded regression evidence and targeted source review')
 c.setStrokeColor(colors.HexColor('#b9cbd4'));c.line(62,795,532,795);c.setFont('Body',8);c.setFillColor(colors.HexColor('#536b79'));c.drawString(62,804,'SWIFT CONCURRENCY | PRACTITIONER REPORT');c.drawString(62,32,'v1.0 - technical report - 6 November 2026');c.drawRightString(532,32,str(doc.page))
doc=SimpleDocTemplate(str(O/'swift-concurrency-repairs-v1.0.pdf'),pagesize=(595.276,841.89),rightMargin=63,leftMargin=62,topMargin=62,bottomMargin=55)
doc.build(story,onFirstPage=furniture,onLaterPages=furniture,canvasmaker=lambda *args,**kwargs: pdfcanvas.Canvas(*args,**{**kwargs,'initialFontName':'Body'}))
