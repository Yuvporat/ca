
from django.urls import path
from .views import (index , GroupList, GroupDetail, DeviceList, DeviceDetail, DeviceListByGroup, PingDevicesByGroup, getGroupsHome,getGroupsHomePing)


urlpatterns = [
    path('index/',index,name='index'),

    path('group/list/' , GroupList.as_view()),
    path('group/detail/<int:pk>/' , GroupDetail.as_view()),
    path('device/list/' , DeviceList.as_view()),
    path('device/detail/<int:pk>/' , DeviceDetail.as_view()),

    path('device/bygroup/<int:pk>/',DeviceListByGroup.as_view()),
    path('pingdevicesbygroup/<int:pk>/',PingDevicesByGroup),

    path('groupsHome/',getGroupsHome),
    path('groupsHomePing/', getGroupsHomePing)
    # path('', views.CheckList.as_view()),
    # path('create/', views.CheckCreate.as_view()),
    # path('update/<int:pk>/', views.CheckUpdate.as_view()),
    # path('delete/<int:pk>/', views.CheckDelete.as_view()),
    # ###
    # # path('mahlaka/<str:pk>/', views.CheckListByMahlaka.as_view()),
    # ###
    # path('mahlaka/<str:pk>/', views.CheckGetByMahlaka),
    # path('name/<str:pk>/', views.CheckGetByTitle),
]