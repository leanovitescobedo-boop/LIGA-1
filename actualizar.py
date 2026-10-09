import requests,bs4,re,json,datetime,pathlib
urls={"clausura":"https://www.futbolperuano.com/liga-1/clausura/tabla-de-posiciones","acumulado":"https://www.futbolperuano.com/liga-1/tabla-acumulada/tabla-de-posiciones"}
def read(url):
 response=requests.get(url,timeout=30,headers={"User-Agent":"Mozilla/5.0"});response.raise_for_status()
 soup=bs4.BeautifulSoup(response.text,"html.parser");found=[]
 for tr in soup.select("tr"):
  cells=tr.find_all("td")
  if len(cells)<10:continue
  # Typical layout: Pos, Equipo, Pts, PJ, PG, PE, PP, GF, GC, DG
  txt=[x.get_text(" ",strip=True) for x in cells]
  for offset in range(min(3,len(txt)-9)):
   try:
    rank=int(txt[offset]);name=txt[offset+1].strip()
    nums=[int(x.replace("+","").strip()) for x in txt[offset+2:offset+10]]
    pts,pj,g,e,p,gf,gc,dif=nums
    if not (1<=rank<=18 and name and 0<=pj<=40 and g+e+p==pj and gf-gc==dif):continue
    found.append(dict(club=name,pts=pts,pj=pj,g=g,e=e,p=p,gf=gf,gc=gc,dif=dif));break
   except (ValueError,IndexError):continue
 if len(found)!=18 or len({x["club"] for x in found})!=18:raise ValueError("No se encontraron 18 clubes válidos; no se alterará data.json")
 return found
result={key:read(url) for key,url in urls.items()}
result["updated"]=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).isoformat(timespec="seconds")
result["source"]="https://www.futbolperuano.com/liga-1/"
pathlib.Path("data.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
