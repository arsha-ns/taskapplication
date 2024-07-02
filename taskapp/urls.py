from django.urls import path

from taskapp import views

urlpatterns=[
    path('task/add/',views.TaskCreatedView.as_view(),name="task-add"),
    path('task/<int:pk>/edit/',views.TaskUpdateView.as_view(),name="task-update"),
    path('task/<int:pk>/detail/',views.TaskDetailView.as_view(),name="task-detail"),
    path('task/<int:pk>/delete/',views.TaskDeleteView.as_view(),name="task-delete"),
    path('task/summary/',views.TaskSummaryView.as_view(),name="task-summary"),
    
    path('register/',views.SignUpView.as_view(),name="signup"),
    path('',views.SignInView.as_view(),name="signin"),
    path('logout/',views.SignOutView.as_view(),name="signout"),
]