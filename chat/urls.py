from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('start/<int:business_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('conversation/<int:conversation_id>/messages/', views.get_messages, name='get_messages'),
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('business/inbox/', views.business_message_inbox, name='business_message_inbox'),

]