from PIL import Image, ImageChops

def compare_images(actual, baseline, threshold=2, max_mismatch=0.0001, diff=None):
    a=Image.open(actual).convert("L"); b=Image.open(baseline).convert("L")
    if a.size!=b.size: return False,{"reason":f"size mismatch {a.size} != {b.size}"}
    d=ImageChops.difference(a,b); hist=d.histogram(); total=a.width*a.height
    changed=sum(hist[threshold+1:]); mismatch=changed/total; mean=sum(i*n for i,n in enumerate(hist))/total; maximum=max((i for i,n in enumerate(hist) if n),default=0)
    if mismatch>max_mismatch and diff: d.point(lambda p:min(255,p*6)).save(diff)
    return mismatch<=max_mismatch,{"mismatch":mismatch,"mean_delta":mean,"max_delta":maximum}
