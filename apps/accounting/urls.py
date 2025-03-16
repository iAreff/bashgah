from django.urls import path
from . import views

app_name='accounting'

urlpatterns = [
    path('', views.index,name='index'),
    path('attendance/<int:course_id>',views.attendance,name='attendance'),
    # path('contact/', views.contact,name='contact'),
]