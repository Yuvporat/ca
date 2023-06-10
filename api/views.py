from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.response import Response

from .serializers import GroupSerializer, DeviceSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import Group, Device

import concurrent.futures
# import subprocess
# from scapy.all import IP, ICMP, sr1
import os
# Create your views here.

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceListByGroup(generics.ListCreateAPIView):
    # queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Device.objects.filter(group=pk)
@api_view(['GET'])
def PingDevicesByGroup(request,*args,**kwargs):
    
    devices = Device.objects.filter(group=kwargs['pk'])
    data=[]

    for device in devices:
        data.append({
            'name' : device.name,
            'ip': device.ip,
            'group': device.group.id,
            'status': device.status,
            'id' : device.id,
        })
    devices = ping_devices(data)
    
    return Response(data)

def ping_devices(devices):
    print(devices)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ping_device,device) for device in devices]
        updated_devices = [future.result() for future in concurrent.futures.as_completed(futures)]
    return updated_devices

def ping_devicesGroup(group):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ping_device,device) for device in group['devices']]
        updated_devices = [future.result() for future in concurrent.futures.as_completed(futures)]
    data = {
        'name': group['name'],
        'id' : group['id'],
        'tkulim' : len([device for device in updated_devices if device['status'] == False]),
        'devices' : updated_devices
    }
    return data

def ping_groups(groups):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ping_devicesGroup,group) for group in groups]
        updated_groups = [future.result() for future in concurrent.futures.as_completed(futures)]
    return updated_groups
def ping_device(device):
    print(device['ip'])
    # result = subprocess.Popen(['ping','-n','1',device['ip']], stdout= subprocess.PIPE, stderr=subprocess.PIPE)
    # print(result.returncode)
    # output,error = result.communicate()
    # status = result.returncode == 0
    
    # packet = IP(dst=device['ip']) / ICMP()
    # response = sr1(packet, timeout=2)
    # status = response and response[ICMP].type == 0
    response = os.popen(f"ping -n 2 {device['ip']}").read()
    # status = ("Request timed out." or "unreachable") not in response
    status = 'time=' in response
    print(response)
    # status = response == 0
    device['status'] = status
    updateDevice(device['id'], status)
    print(status)
    return device

@api_view(['GET'])
def getGroupsHome(request,*args,**kwargs):
    data=[]
    groups = Group.objects.all()
    for group in groups:
        data.append({
            'name': group.name,
            'tkulim': len(Device.objects.filter(group=group.id, status=False)),
            'id' : group.id,
        })  
    return Response(data)

@api_view(['GET'])
def getGroupsHomePing(request,*args,**kwargs):
    groupsdata=[] #groups
    for group in Group.objects.all():
        devicesdata =[]
        data =[]
        groupsdata.append({
            'name' : group.name,
            'tkulim' : 0,
            'id': group.id,
            'devices': [
                {'name' : device.name,
                    'ip': device.ip,
                    'group': device.group.id,
                    'status': device.status,
                    'id' : device.id
                     }
            for device in Device.objects.filter(group=group.id)]
        })

    pingedGroups = ping_groups(groupsdata)
    # for group in pingedGroups:
    #     print(group)
    # for pingedGroup in pingedGroups:
    #     # pingedGroup['tkulim'] = len([device for device in pingedGroup['devices'] if device['status'] == False])
    #     pingedGroup['tkulim'] = 2
    return Response(pingedGroups)
def updateDevice(id,newStatus):
    device = Device.objects.filter(id=id)[0]
    device.status = newStatus
    device.save()
    # print('dddd ',device.status,id)
    # pass
def index(request):
    return render(request,'index.html')
