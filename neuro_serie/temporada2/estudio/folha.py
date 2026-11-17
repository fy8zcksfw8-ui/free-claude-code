import sys, glob, json
from PIL import Image, ImageDraw
# monta folha de quadros com a faixa segura do HyperFrames (168-1330 px) marcada
fs=sorted(glob.glob("out/f*.png")); ims=[Image.open(f).convert("RGB") for f in fs]
w,h=ims[0].size; k=w/1080; cols=8; rows=(len(ims)+cols-1)//cols
sheet=Image.new("RGB",(w*cols,h*rows),"white")
for i,im in enumerate(ims):
    d=ImageDraw.Draw(im)
    for y in (168,1330): d.line([0,y*k,w,y*k],fill=(255,0,0),width=2)
    sheet.paste(im,((i%cols)*w,(i//cols)*h))
sheet.save(sys.argv[1])
