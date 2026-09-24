import base64, json, glob, io, os, sys
from PIL import Image, ImageOps
exec(open('items_en.py',encoding='utf-8').read())
exec(open('items_batch2.py',encoding='utf-8').read())
exec(open('items_batch3.py',encoding='utf-8').read())
exec(open('items_batch4.py',encoding='utf-8').read())
exec(open('items_batch5.py',encoding='utf-8').read())
exec(open('items_batch6.py',encoding='utf-8').read())
exec(open('items_batch7.py',encoding='utf-8').read())
exec(open('items_batch8.py',encoding='utf-8').read())
exec(open('items_batch9.py',encoding='utf-8').read())
exec(open('items_batch10.py',encoding='utf-8').read())
items = items + [(a,b,c,d,e,f,'',h,i) for (a,b,c,d,e,f,g,h,i) in items2+items3+items4+items5+items6+items7+items8+items9+items10]
cat = {i[0]: i for i in items}
dups = {"0535":"0534","0547":"0546", **dups2, **dups3, **dups4, **dups5, **dups6, **dups7, **dups8, **dups9, **dups10}
ids = sorted(os.path.basename(f)[6:10] for f in glob.glob('batch1/SA_PA_*.jpg'))
mode = sys.argv[1]  # 'embed' or 'site'
os.makedirs('site/images', exist_ok=True); os.makedirs('site/thumbs', exist_ok=True)
data=[]
for i in ids:
    src=f'batch1/SA_PA_{i}.jpg'
    im=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    if mode=='embed':
        t=im.copy(); t.thumbnail((420,420), Image.LANCZOS)
        b=io.BytesIO(); t.save(b,'JPEG',quality=55,optimize=True,progressive=True)
        img="data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode(); thumb=None
    else:
        full=im.copy(); full.thumbnail((1400,1400), Image.LANCZOS); full.save(f'site/images/{i}.jpg','JPEG',quality=78,optimize=True,progressive=True)
        t=im.copy(); t.thumbnail((480,480), Image.LANCZOS); t.save(f'site/thumbs/{i}.jpg','JPEG',quality=70,optimize=True,progressive=True)
        img=f'images/{i}.jpg'; thumb=f'thumbs/{i}.jpg'
    if i in cat:
        _,t_,m,p,g,d,f,c,n=cat[i]
        e=dict(id=i,title=t_,motif=m,press=p,group=g,date=d,format=f,cond=c,note=n)
    elif i in dups:
        o=cat[dups[i]]
        e=dict(id=i,title=o[1],motif=o[2],press=o[3],group=o[4],date=o[5],format=o[6],cond=o[7],note=f"Appears to be a second photo of no. {dups[i]}.")
    else:
        e=dict(id=i,title=f"Print no. {i}",motif="",press="",group="todo",date="",format="",cond="",note="Not yet catalogued.")
    tags=[]
    if 'dvertis' in (e['press']+e['title']) or 'Glaxo' in e['press']: tags.append('ads')
    if i in PORTRAITS: tags.append('portraits')
    if tags: e['tags']=tags
    e['img']=img
    if thumb: e['thumb']=thumb
    data.append(e)
json.dump(data,open(f'data_{mode}.json','w'),ensure_ascii=False)
print(mode,len(data),sum(1 for d in data if d['group']!='todo'))
