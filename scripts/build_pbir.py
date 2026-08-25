from pathlib import Path
import json, hashlib, shutil

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "LeadEjecutivo.Report" / "definition" / "pages"
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.11.0/schema.json"

PAGES = [
    ("a1executivejourney", "Resumen Ejecutivo - Journey"),
    ("b2grados", "Grados"),
    ("c3posgrados", "Posgrados"),
    ("d4asesores", "Asesores"),
]

def stable_id(*parts):
    return hashlib.sha1("|".join(map(str, parts)).encode("utf-8")).hexdigest()[:20]

def lit(v): return {"expr":{"Literal":{"Value":v}}}
def color(v): return {"solid":{"color":lit("'%s'" % v)}}
def mfield(entity, prop):
    return {"field":{"Measure":{"Expression":{"SourceRef":{"Entity":entity}},"Property":prop}},"queryRef":f"{entity}.{prop}","nativeQueryRef":prop}
def cfield(entity, prop):
    return {"field":{"Column":{"Expression":{"SourceRef":{"Entity":entity}},"Property":prop}},"queryRef":f"{entity}.{prop}","nativeQueryRef":prop}

def base(vtype, x, y, w, h, title=None, key=""):
    name = stable_id(vtype,x,y,w,h,title or "",key)
    return {
        "$schema": SCHEMA,
        "name": name,
        "position": {"x":x,"y":y,"z":10,"height":h,"width":w,"tabOrder":10},
        "visual": {
            "visualType": vtype,
            "visualContainerObjects": {
                "background":[{"properties":{"show":lit("true"),"color":color("#FFFFFF"),"transparency":lit("0D")}}],
                "border":[{"properties":{"show":lit("true"),"color":color("#E6E0EA"),"radius":lit("8D")}}],
                "title":[{"properties":{"show":lit("true" if title else "false"),"text":lit("'%s'" % (title or ""))}}]
            }
        }
    }

def write(page, d):
    ddir = REPORT/page/"visuals"/d["name"]
    ddir.mkdir(parents=True, exist_ok=True)
    (ddir/"visual.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def text(page, txt, x, y, w, h, size=18, bold=False, bg=None, key=""):
    name = stable_id("textbox",x,y,w,h,txt,key)
    d={"$schema":SCHEMA,"name":name,"position":{"x":x,"y":y,"z":2,"height":h,"width":w,"tabOrder":2},"visual":{"visualType":"textbox","objects":{"general":[{"properties":{"paragraphs":[{"textRuns":[{"value":txt,"textStyle":{"fontFamily":"Segoe UI","fontSize":f"{size}pt","fontWeight":"bold" if bold else "normal","color":"#FFFFFF" if bg else "#2B2036"}}]}]}}]},"visualContainerObjects":{"background":[{"properties":{"show":lit("true" if bg else "false"),"color":color(bg or "#FFFFFF"),"transparency":lit("0D")}}],"border":[{"properties":{"show":lit("false")}}],"title":[{"properties":{"show":lit("false")}}]}}}
    write(page,d)

def slicer(page, entity, col, x, y, w, h, title):
    d=base("slicer",x,y,w,h,title,key=f"{entity}.{col}")
    d["visual"]["query"]={"queryState":{"Values":{"projections":[cfield(entity,col)]}}}
    write(page,d)

def card(page, measure, x, y, w, h, title):
    d=base("card",x,y,w,h,title,key=measure)
    d["visual"]["query"]={"queryState":{"Values":{"projections":[mfield("Candidato",measure)]}}}
    write(page,d)

def chart(page,vtype,measure,entity,col,x,y,w,h,title):
    d=base(vtype,x,y,w,h,title,key=f"{measure}|{entity}.{col}")
    d["visual"]["query"]={"queryState":{"Category":{"projections":[cfield(entity,col)]},"Values":{"projections":[mfield("Candidato",measure)]}}}
    write(page,d)

def multi_chart(page,vtype,measures,entity,col,x,y,w,h,title):
    d=base(vtype,x,y,w,h,title,key="|".join(measures)+f"|{entity}.{col}")
    d["visual"]["query"]={"queryState":{"Category":{"projections":[cfield(entity,col)]},"Values":{"projections":[mfield("Candidato",m) for m in measures]}}}
    write(page,d)

def funnel(page,x,y,w,h):
    d=base("funnel",x,y,w,h,"Journey de Leads por estado",key="journey")
    d["visual"]["query"]={"queryState":{"Category":{"projections":[cfield("Candidato","Status")]},"Y":{"projections":[mfield("Candidato","Total Leads")]}}}
    write(page,d)

def table(page, cols, x, y, w, h, title):
    d=base("tableEx",x,y,w,h,title,key="|".join(p for _,_,p in cols))
    projections=[]
    for typ,ent,prop in cols:
        projections.append(mfield(ent,prop) if typ=="m" else cfield(ent,prop))
    d["visual"]["query"]={"queryState":{"Values":{"projections":projections}}}
    write(page,d)

def common(page,title):
    text(page,title,0,0,1280,75,28,True,"#3C235F","header")
    slicer(page,"DimFecha","Date",25,88,235,62,"Rango de fechas")
    slicer(page,"Candidato","UI_Periodo__c",275,88,235,62,"Período académico")
    slicer(page,"Candidato","UI_Sede__c",525,88,200,62,"Sede")
    slicer(page,"Candidato","UI_Modalidad__c",740,88,200,62,"Modalidad")
    slicer(page,"Candidato","UI_UnidadNegocio__c",955,88,300,62,"Unidad de negocio")

def build():
    for pid,title in PAGES:
        v=REPORT/pid/"visuals"
        if v.exists(): shutil.rmtree(v)
        v.mkdir(parents=True,exist_ok=True)
        common(pid,title)

    p="a1executivejourney"
    for i,(m,t) in enumerate([("Total Leads","Leads"),("Total Proyectados","Proyectados"),("Total Inscritos","Inscritos"),("Total Matriculas","Matrículas"),("Matriculas YTD","Matrículas YTD")]):
        card(p,m,25+i*245,165,225,100,t)
    funnel(p,25,285,420,310)
    multi_chart(p,"lineChart",["Leads YTD","Gestionados YTD","Citas Efectivas YTD","Perdidos YTD"],"DimFecha","Date",465,285,790,145,"Comparación YTD: Leads, gestionados, citas y perdidos")
    chart(p,"clusteredColumnChart","Total Matriculas","Candidato","UI_Periodo__c",465,445,380,150,"Matrículas por período académico")
    chart(p,"clusteredBarChart","Total Matriculas","Candidato","UI_CarreraPrimeraOpcionWeb__c",860,445,395,150,"Carreras que más matriculan")
    text(p,"Storytelling: Captación → Gestión → Cita efectiva → Proyección → Inscripción → Matrícula. Rango operativo por defecto: 01/05/2026 hasta hoy. La línea compara acumulados YTD de Leads, gestionados, citas efectivas y perdidos. Matrícula/inscripción/proyección siguen pendientes de mapear contra objetos transaccionales reales de Salesforce.",25,615,1230,70,10,False,None,"story")

    for p,label in [("b2grados","Grados"),("c3posgrados","Posgrados")]:
        for i,(m,t) in enumerate([("Total Leads","Total Leads"),("Leads Perdidos","Perdidos"),("Total Matriculas","Matrículas"),("% Perdidos","% Perdidos"),("% Lead a Matricula","% Lead → Matrícula")]):
            card(p,m,25+i*235,165,220 if i<4 else 290,100,t)
        chart(p,"clusteredBarChart","Total Leads","Candidato","UI_Origen__c",25,285,385,155,"Orígenes con mayor volumen")
        chart(p,"clusteredBarChart","Total Leads","Candidato","UI_Campana__c",430,285,385,155,"Canales / campañas")
        chart(p,"clusteredBarChart","Total Leads","Candidato","UI_CarreraPrimeraOpcionWeb__c",835,285,420,155,"Ranking de carreras por Leads")
        chart(p,"clusteredBarChart","Total Matriculas","Candidato","UI_CarreraPrimeraOpcionWeb__c",25,460,385,155,"Carreras que más matriculan")
        chart(p,"clusteredBarChart","Leads Perdidos","Candidato","UI_RazonPerdido__c",430,460,385,155,"Dónde se pierden los Leads")
        chart(p,"clusteredBarChart","Leads Sin Actividad 7d","Candidato","UI_CarreraPrimeraOpcionWeb__c",835,460,420,155,"Queda menos: Leads sin actividad 7d")
        text(p,f"Página {label}: el modelo intenta resolver automáticamente nombres alternativos de origen/campaña/carrera. Unidad de negocio permanece sin equivalencia hardcodeada hasta validar su catálogo real en Salesforce.",25,630,1230,55,10,False,None,"footnote")

    p="d4asesores"
    for i,(m,t) in enumerate([("Total Leads","Leads asignados"),("Leads Gestionados","Gestionados"),("Leads Perdidos","Perdidos"),("Total Matriculas","Matrículas"),("Leads Sin Actividad 7d","Sin actividad 7d")]):
        card(p,m,25+i*235,165,220 if i<4 else 290,100,t)
    chart(p,"clusteredBarChart","Total Leads","Candidato","OwnerName",25,285,385,160,"Carga de Leads por asesor")
    chart(p,"clusteredBarChart","Total Matriculas","Candidato","OwnerName",430,285,385,160,"Matrículas por asesor")
    chart(p,"clusteredBarChart","Leads Perdidos","Candidato","OwnerName",835,285,420,160,"Leads perdidos por asesor")
    chart(p,"clusteredBarChart","Leads Sin Actividad 7d","Candidato","OwnerName",25,465,385,155,"Backlog sin actividad 7d")
    chart(p,"clusteredBarChart","Leads Sin Actividad 30d","Candidato","OwnerName",430,465,385,155,"Backlog crítico 30d")
    table(p,[("c","Candidato","OwnerName"),("m","Candidato","Total Leads"),("m","Candidato","Leads Gestionados"),("m","Candidato","Leads Perdidos"),("m","Candidato","Total Matriculas")],835,465,420,155,"Matriz ejecutiva de asesores")

if __name__ == "__main__":
    build()
    print("PBIR visuals generated")
