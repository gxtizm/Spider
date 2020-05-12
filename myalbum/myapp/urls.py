from django.contrib import admin
from django.urls import path,re_path
from .import views

urlpatterns = [
	#首页
    path('',views.index,name="index"),

    #相册信息路由
    path('album',views.indexAlbum,name="album"),#浏览相册
    path('album/add',views.addAlbum,name="addalbum"),#发布相册信息
    path('album/insert',views.insertAlbum,name="insertalbum"),#执行添加操作
    re_path('^album/del/(?P<pid>[0-9]+)$',views.delAlbum,name="delalbum"),#删除相册
    re_path('^album/edit/(?P<pid>[0-9]+)$',views.editAlbum,name="editalbum"),#修改相册信息
    path('album/update',views.updateAlbum,name="updatealbum"),#执行信息修改
    re_path('album/pag/(?P<pIndex>[0-9]+)$',views.pagAlbum,name="pagalbum"), #分页
    path('album/send',views.send,name="send"),
]
