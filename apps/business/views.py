import datetime
from django.http.response import JsonResponse
#from django.core import serializers
from django.http import Http404
import json
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from ..rbac.models import User
from .models import Project, Task, Task_User, Project_User,Article,Record,Task_Project,Task_User
import datetime
from rest_framework import serializers
from rest_framework import views
from rest_framework.response import Response
# 向前端返回json数据
def respondDataToFront(preData):
    data = {
        'code': 200,
        'message': "获取成功",
        'data': preData
    }
    print("完成发送任务")
    return JsonResponse(data=data, safe=False)

@csrf_exempt
def newProject(request):
    data = json.loads(request.body)
    projectName = data['prjectName']
    print(data)
    print(projectName)
    Project.objects.create(name=projectName, status='r', addTime=datetime.datetime.now())
    print("你好ssss")
    return HttpResponse("成功")


# 保存新建的项目
def saveProject(request):
    data = json.loads(request.body)
    print(data)
    phaseList = []
    phase1 = data["phase1"]
    phase2 = data["phase2"]
    phaseList.append(phase1)
    phaseList.append(phase2)
    projectId = data["projectId"]
    print(phase1)
    print(projectId)

    # 这样的话，多线程后面要加互斥锁
    # 取数据库中最后一个元组的id
    task = Task.objects.last()
    project = Project.objects.get(id=projectId)
    initialId = task.id + 1
    # initialId = 1
    print(initialId)
    ct = 1
    for phase in phaseList :
        for task in phase:
            ls = task['thisid']
            rb = task['thisFarther']
            # if int(task['leftSon']) != 0 :
            #     ls = int(task['leftSon']) + initialId
            # if int(task['rightBrother']) != 0 :
            #     rb = int(task['rightBrother']) + initialId
            tmp = Task.objects.create(name=task["name"], desc="00", addTime=datetime.datetime.now(), type=1,
                                      thisId=ls,
                                      thisFarther=rb, phase=ct)
            # 将task和project一一关联起来
            Task_Project.objects.create(task=tmp, project=project, number=1, addTime=datetime.datetime.now())
            #将task和user,project和user一一关联起来
            for obj in task['staffs']:
                user = User.objects.get(pk=obj)
                Task_User.objects.create(task=tmp,user=user,addTime=datetime.datetime.now())
                if  not Project_User.objects.filter(user_id=obj, project_id=projectId).exists():
                    Project_User.objects.create(project=project,user=user,addTime=datetime.datetime.now())
        ct += 1
        # initialId += ct
    return HttpResponse("成功")


# 根据用户id得到该用户所参加的所有项目列表
def getThisUserProjectList(request):
    thisUserId = request.GET.get("userId")
    print(thisUserId)
    projectList = Project_User.objects.filter(user=thisUserId).values("project__status",
                                                                           "project__name",
                                                                           "project__id",
                                                                           "project__addTime"
                                                                           ).distinct()
    print(projectList)
    return respondDataToFront(list(projectList))


# 根据项目的pid得到该项目下的任务列表以及各任务对应的人员分配信息
def getTasksFromTheProject(request):
    print(request.GET)
    projectId = request.GET.get("projectId")
    print(projectId)
    phases = 2
    projectInfo = {}
    # 假定现在就两个阶段
    for phase in range(phases):
        TaskList = Task_Project.objects.filter(project=projectId,task__phase=(phase+1)).values("task__id", "task__name", "task__status",
                                                                     "task__thisId",
                                                                     "task__thisFarther",
                                                                     "task__phase")
        userList = []
        applierList = []
        # 下面是默认两个阶段，每个阶段有若干个任务
        for task in TaskList:
            applierList.append(list(Task_User.objects.filter(task_id=task['task__id']).values("user__username")))
        TaskList = list(TaskList)
        for i in range(len(TaskList)):
            TaskList[i]['username'] = applierList[i]
        # print(applierList)
        # print(TaskList)
        projectInfo["phase"+str(phase+1)] = TaskList
        projectInfo["phase"+str(phase+1)+"Number"] = len(TaskList)
    print(projectInfo)
    return respondDataToFront(projectInfo)


def saveTask(request):
    taskName = "阶段一任务一"
    taskType = 1  # 表示当前任务处于第几阶段
    dic = request.POST.get("userIdProcedureMap")
    print(dic[2])
    print(request.POST.get("taskName"))
    print("这里是用户列表1111")
    userIdProcedureMap = {2: 1, 3: 2, 4: 3, 1: 4}  # 前端传递的用户项目
    pId = 1  # 由前端将数据传递过来
    project = Project.objects.get(id=pId)
    # models.task.objects.create(name=projectName, status=0, addTime=datetime.datetime.now())

    # 1保存当前任务(互斥锁需要)
    Task.objects.create(project=pId, number=0, name=taskName,  type=taskType)
    task = Task.objects.last()

    # 2保存当前项目下的人员分工（互斥锁）
    for key in userIdProcedureMap.keys():
        userInfor = User.objects.get(id=key)
        Project_User.objects.create(project=project, user=userInfor)

    # 3保存当前任务下的人员分工(这个地方需要加锁)
    for key, value in userIdProcedureMap.items():
        userInfor = User.objects.get(id=key)
        Task_User.objects.create(task=task, user=userInfor, step=value)
    return HttpResponse("成功")

def test(request):
    projectId = 1
    m = list(Project.objects.all().values())
    data = {
        'data': m,
        'code': 200,
        'message': "获取成功"
    }
    print("完成发送任务")
    return JsonResponse(data=data, safe=False)
    # for obj in  lst:
    #     print(obj)

    # return HttpResponse("成功")

def orm(request):
    # models.UserInfo.objects.create(name= "ws1",passWord="123",age = 19)
    # models.UserInfo.objects.create(name= "ws2",passWord="123",age = 19)
    # models.UserInfo.objects.create(name= "ws3",passWord="123",age = 19)
    # models.UserInfo.objects.create(name= "ws4",passWord="123",age = 19)
    # 删除
    # models.UserInfo.objects.filter(id=1).delete()

    # 获取数据
    datalist = User.objects.all()
    # jsondata = Js
    print(datalist)
    for obj in datalist:
        print(obj.pk, obj.name)

    return HttpResponse("成功")
#Project序列化器
#---------------------
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('addTime',)
#Task序列化器
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('addTime',)
#Article序列化器
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('addTime',)
#Record序列化器
class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ('addTime',)
#Project_User序列化器
class Project_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_User
        fields = '__all__'
        read_only_fields = ('addTime',)
#Task_Project序列化器
class Task_ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_Project
        fields = '__all__'
        read_only_fields = ('addTime',)
#Task_User序列化器
class Task_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_User
        fields = '__all__'
        read_only_fields = ('addTime',)
#Project的增删改查接口类
class ProjectView(views.APIView):
    def get(self,request):
        #print(123123)
        project_list = Project.objects.all()
        serializer = ProjectSerializer(instance = project_list,many = True)
        return Response(serializer.data)
    def post(self,request):
        print(12312312)
        serializer = ProjectSerializer(data = request.data)
        if serializer.is_valid():
            #new_project = Project.objects.create(**serializer.validated_data)
            #serializer.save(author=request.user)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class ProjectdetailView(views.APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    def get(self,request,id):
        project = self.get_object(pk = id)
        serializer = ProjectSerializer(instance=project,many = False)
        return Response(serializer.data)
    def put(self,request,id):
        update_project = self.get_object(pk = id)
        serializer = ProjectSerializer(instance=update_project,data=request.data)
        if serializer.is_valid():
            #Project.objects.filter(pk=id).update(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response()
#Task的增删改查接口类
class TaskView(views.APIView):
    def get(self,request):
        Task_list = Task.objects.all()
        serializer = TaskSerializer(instance = Task_list,many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            #new_project = Project.objects.create(**serializer.validated_data)
            #serializer.save(author=request.user)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class TaskdetailView(views.APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404
    def get(self,request,id):
        task = self.get_object(pk = id)
        serializer = TaskSerializer(instance=task,many = False)
        return Response(serializer.data)
    def put(self,request,id):
        update_Task = self.get_object(pk = id)
        serializer = TaskSerializer(instance=update_Task,data=request.data)
        if serializer.is_valid():
            #Project.objects.filter(pk=id).update(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response()
#Article的增删改查接口类
class ArticleView(views.APIView):
    def get(self,request):
        Article_list = Article.objects.all()
        serializer = ArticleSerializer(instance = Article_list,many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            #new_project = Project.objects.create(**serializer.validated_data)
            #serializer.save(author=request.user)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class ArticledetailView(views.APIView):
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404
    def get(self,request,id):
        article = self.get_object(pk = id)
        serializer = ArticleSerializer(instance=article,many = False)
        return Response(serializer.data)
    def put(self,request,id):
        update_Article = self.get_object(pk = id)
        serializer = ArticleSerializer(instance=update_Article,data=request.data)
        if serializer.is_valid():
            #Project.objects.filter(pk=id).update(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response()
#Record的增删改查接口类
class RecordView(views.APIView):
    def get(self,request):
        Record_list = Record.objects.all()
        serializer = RecordSerializer(instance = Record_list,many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = RecordSerializer(data = request.data)
        if serializer.is_valid():
            #new_project = Project.objects.create(**serializer.validated_data)
            #serializer.save(author=request.user)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class RecorddetailView(views.APIView):
    def get_object(self, pk):
        try:
            return Record.objects.get(pk=pk)
        except Record.DoesNotExist:
            raise Http404
    def get(self,request,id):
        record = self.get_object(pk = id)
        serializer = RecordSerializer(instance=record,many = False)
        return Response(serializer.data)
    def put(self,request,id):
        update_Record = self.get_object(pk = id)
        serializer = RecordSerializer(instance=update_Record,data=request.data)
        if serializer.is_valid():
            #Project.objects.filter(pk=id).update(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self, request, pk):
        record = self.get_object(pk)
        record.delete()
        return Response()
#Project_User的增删改查接口类
class Project_UserView(views.APIView):
    def get(self,request):
        Project_User_list = Project_User.objects.all()
        serializer = Project_UserSerializer(instance = Project_User_list,many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = Project_UserSerializer(data = request.data)
        if serializer.is_valid():
            #new_project = Project.objects.create(**serializer.validated_data)
            #serializer.save(author=request.user)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class Project_UserdetailView(views.APIView):
    def get_object(self, pk):
        try:
            return Project_User.objects.get(pk=pk)
        except Project_User.DoesNotExist:
            raise Http404
    def get(self,request,id):
        project_User = self.get_object(pk = id)
        serializer = Project_UserSerializer(instance=project_User,many = False)
        return Response(serializer.data)
    def put(self,request,id):
        update_Project_User = self.get_object(pk = id)
        serializer = Project_UserSerializer(instance=update_Project_User,data=request.data)
        if serializer.is_valid():
            #Project.objects.filter(pk=id).update(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self, request, pk):
        project_User = self.get_object(pk)
        project_User.delete()
        return Response()
#Task_Project的增删改查接口类
class Task_ProjectView(views.APIView):
    def get(self,request):
        Task_Project_list = Task_Project.objects.all()
        serializer = Task_ProjectSerializer(instance = Task_Project_list,many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = Task_ProjectSerializer(data = request.data)
        if serializer.is_valid():
            #new_project = Project.objects.create(**serializer.validated_data)
            #serializer.save(author=request.user)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class Task_ProjectdetailView(views.APIView):
    def get_object(self, pk):
        try:
            return Task_Project.objects.get(pk=pk)
        except Task_Project.DoesNotExist:
            raise Http404
    def get(self,request,id):
        task_Project = self.get_object(pk = id)
        print(task_Project)
        serializer = Task_ProjectSerializer(instance=task_Project,many = False)
        return Response(serializer.data)
    def put(self,request,id):
        update_Task_Project = self.get_object(pk = id)
        serializer = Task_ProjectSerializer(instance=update_Task_Project,data=request.data)
        if serializer.is_valid():
            #Project.objects.filter(pk=id).update(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self, request, pk):
        task_Project = self.get_object(pk)
        task_Project.delete()
        return Response()
#Task_User的增删改查接口类
class Task_UserView(views.APIView):
    def get(self,request):
        Task_User_list = Task_User.objects.all()
        serializer = Task_UserSerializer(instance = Task_User_list,many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = Task_UserSerializer(data = request.data)
        if serializer.is_valid():
            #new_project = Project.objects.create(**serializer.validated_data)
            #serializer.save(author=request.user)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class Task_UserdetailView(views.APIView):
    def get_object(self, pk):
        try:
            return Task_User.objects.get(pk=pk)
        except Task_User.DoesNotExist:
            raise Http404
    def get(self,request,id):
        task_User = self.get_object(pk = id)
        serializer = Task_UserSerializer(instance=task_User,many = False)
        return Response(serializer.data)
    def put(self,request,id):
        update_Task_User = self.get_object(pk = id)
        serializer = Task_UserSerializer(instance=update_Task_User,data=request.data)
        if serializer.is_valid():
            #Project.objects.filter(pk=id).update(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self, request, pk):
        task_User = self.get_object(pk)
        task_User.delete()
        return Response()

