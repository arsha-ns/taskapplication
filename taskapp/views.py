from django.shortcuts import render,redirect
from django.views.generic import View
from taskapp.models import Task
from taskapp.forms import TaskForm,RegisterForm,LoginForm,SummaryForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count,Sum
from django.contrib.auth import authenticate,login,logout
from taskapp.decorators import signin_required

from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
import datetime
# Create your views here.

@method_decorator(signin_required,name="dispatch")
class TaskCreatedView(View):
    def get(self,request,*args,**kwargs):
        form_instance=TaskForm()
        qs=Task.objects.filter(user_object=request.user)
        return render(request,"task_add.html",{"form":form_instance,"data":qs})
    

    def post(self,request,*args,**kwargs):
        form_instance=TaskForm(request.POST)
        if form_instance.is_valid():
            form_instance.instance.user_object=request.user
            form_instance.save()
            messages.success(request,"task has been created")

            return redirect("task-add")
            
        
        else:
            return render(request,"task_add.html",{"form":form_instance})
        
method_decorator(signin_required,name="dispatch")
class TaskUpdateView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        task_object=Task.objects.get(id=id)

        form_instance=TaskForm(instance=task_object)
        return render(request,"task_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        task_object=Task.objects.get(id=id)

        form_instance=TaskForm(instance=task_object,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"task has beenupdated")

            return redirect("task-add")
        else:
            return render(request,"task-edit.html",{"form":form_instance})
        
@method_decorator(signin_required,name="dispatch")
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)

       

        return render(request,"task_detail.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.get(id=id).delete()
        messages.success(request,"deleted")
        return redirect("task-add")
    


@method_decorator(signin_required,name="dispatch")    
class TaskSummaryView(View):
    def get(self,request,*args,**kwargs):
      current_month=timezone.now().month
      current_year=timezone.now().year
      task_list=Task.objects.filter(created_date__month=current_month,created_date__year=current_year,user_object=request.user)
      task_total=task_list.aggregate(total=Count("status"))
    #   task_total=task_list.values("status").annotate(total=Sum("status"))
      print(task_total)

      
      status_summary=task_list.values("status").annotate(total=Count("status"))  
      print(status_summary)   

      data={"task_total":task_total,"status_summary":status_summary}
      return render(request,"status_summary.html",data)
    
# --------------------------------------------------------------------------------------------------------------------------------------

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form_instance=RegisterForm()
        return render(request,"register.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):
        form_instance=RegisterForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            User.objects.create_user(**data)
            print("user object created")
            return redirect("signin")
        else:
            print("faild")
            return render(request,"register.html",{"form":form_instance})
        


class SignInView(View):
    def get(self,request,*args,**kwargs):
        form_instance=LoginForm()
        return render(request,"login.html",{"form":form_instance})

    
    def post(self,request,*args,**kwargs):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            print(uname,pwd)


            user_object=authenticate(request,username=uname,password=pwd)
            print(user_object)


            if user_object:
                
                login(request,user_object)

                return redirect("task-add")
        messages.error(request,"authentication failed in valid credemption")
        return render(request,"login.html",{"form":form_instance})
    



@method_decorator(signin_required,name="dispatch") 
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    



# class DashBoardView(View):
    def get(self,request,*args,**kwargs):
        form_instance=SummaryForm()
        current_month=timezone.now().month
        current_year=timezone.now().year
        task_list=Task.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)
        task_total=task_list.aggregate(total=Count("status"))
        print("total tasks:",task_total)
        status_summary=task_list.values("status").annotate(total=Count("status"))  
        



        monthly_task={}


        for month in range(1,13):
            start_date=datetime.date(current_year,month,1)

            if month==12:
                end_date=datetime.date(current_year+1,1,1)
            else:
                end_date=datetime.date(current_year,month+1,1)

            monthly_task_total=Task.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)
            
            monthly_task[start_date.strftime('%B')]=monthly_task_total if monthly_task_total else 0
        print(monthly_task)


        
      
        return render(request,"dashboard.html",{"task_total":task_total,"status_summary":status_summary,"form":form_instance,"monthly_task":monthly_task})
    


    def post(self,request,*args,**kwargs):

        form_instance=SummaryForm(request.POST)

        if form_instance.is_valid():
            data=form_instance.cleaned_data

            start_date=data.get("start_date")

            end_date=data.get("end_date")


            task_list=Task.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)


            print("task:",task_list)


            task_total=task_list.aggregate(total=Count("status"))
            print("expense total:",task_total)


       

        return render(request,"dashboard.html",{"expense":task_total,"form":form_instance})
    



    



    
    


