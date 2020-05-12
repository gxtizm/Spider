from django.shortcuts import render
from myapp.models import Album
from django.http import HttpResponse
from datetime import datetime
import time,os
from PIL import Image
from django.core.paginator import Paginator
# Create your views here.

def index(request):
	return render(request,"myapp/first.html")

def indexAlbum(request):
	list = Album.objects.all()
	context={"albumlist":list}
	return render(request,"myapp/album/scan.html",context)

def addAlbum(request):
	return render(request,"myapp/album/add.html")

def insertAlbum(request):
	try:
		album = Album()
		album.title = request.POST['title']
		album.name = request.POST['name']
		album.addtime = datetime.now()
		
		context = {"info":"添加成功！"}
		myfile = request.FILES.get("mypic",None)
		if not myfile:
			return HttpResponse("没有上传文件信息")
		filename = str(time.time())+"."+myfile.name.split('.').pop()
		destination = open("./static/pics/"+filename,"wb+")
		for chunk in myfile.chunks():      # 分块写入文件  
			destination.write(chunk)  
		destination.close()
		im = Image.open("./static/pics/"+filename)
    	# 缩放到75*75(缩放后的宽高比例不变):
		im.thumbnail((75, 75))
    	# 把缩放后的图像用jpeg格式保存: 
		im.save("./static/pics/s_"+filename,None)
		album.filename = filename
		album.save()
	except Exception as err:
		print(err)
		context = {"info":"添加失败！"}
	return render(request,"myapp/album/info.html",context)

def delAlbum(request,pid):
	try:
		ob = Album.objects.get(id=pid)
		os.remove("./static/pics/"+ob.filename)
		os.remove("./static/pics/s_"+ob.filename)
		ob.delete()
		context = {"info":"删除成功！"}
	except Exception as err:
		print(err)
		context = {"info":"删除失败！"}
	return render(request,"myapp/album/info.html",context)

def editAlbum(request,pid):
	try:
		temp = Album.objects.get(id=pid)
		context={"p":temp}
		return render(request,"myapp/album/edit.html",context)
	except Exception as err:
		print(err)
		context = {"info":"没有找到要修改的信息！"}
		return render(request,"myapp/album/edit.html",context)

def updateAlbum(request):
	try:
		p = Album.objects.get(id=request.POST['id'])
		p.title = request.POST['title']
		p.name = request.POST['name']
		p.filename = request.POST['filename']
		p.save()
		context = {"info":"修改成功！"}
	except Exception as err:
		print(err)
		context = {"info":"修改失败！"}
	return render(request,"myapp/album/info.html",context)

def pagAlbum(request,pIndex):
	list = Album.objects.all()
	p = Paginator(list,2)
	if pIndex == "":
		pIndex = "1"
	pIndex = int(pIndex)
	list2 = p.page(pIndex)
	plist = p.page_range
	context = {'ulist':list2,"plist":plist,"pIndex":int(pIndex)}
	return render(request,"myapp/album/pag.html",context)



from django.conf import settings
from django.core.mail import send_mail
 
...
def send(request):
    subject = '火星的问候'  #主题
    fp = open("myapp/resource/卜算子.html","rb")
    content = fp.read().decode("utf-8")
    message = content       #内容
    sender = settings.EMAIL_FROM        #发送邮箱，已经在settings.py设置，直接导入
    receiver = ['18829067972@163.com',]      #目标邮箱'aiken.guo@tapque.com','18829067229@163.com'
    html_message = '<h3>%s</h3><br/><br/><h4>.........来自火星的问候！</h4>'%message        #发送html格式
    send_mail(subject,message,sender,receiver,html_message=html_message)
    return HttpResponse("发送成功！请在邮箱收看！")
 
# send()      #使用函数

