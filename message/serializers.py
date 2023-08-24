from rest_framework import serializers
from django.db.models import Q
from .models import *
from customAdmin.models import *
from accounts.models import *



class MessageEmployerSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    message_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"


    def get_last_message(self, obj):        
        request = self.context["request"]
        user_id = request.user.id
        
        m_data =  JobMessage.objects.filter(job_id=obj.id)
        m_data = m_data.filter(Q(receiver_id=user_id)|Q(sender_id=user_id)).order_by("updated_at")        
        return m_data[0].updated_at
    
    def get_user(self, obj):
        return User.objects.get(id=obj.user_id)
    

    def get_message_count(self, obj):
        request = self.context['request']
        if not request.user.is_authenticated:
            return 0
        
        m_list = Proposal.objects.filter(job_id=obj.id, user_id=request.user.id)
        if m_list.count() > 0:
            m_messages =  JobMessage.objects.filter(job_id=obj.id, receiver_id=request.user.id, receiver_readed=False)
            return m_messages.count()
        else:
            return 0  
        
class MessageEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField(read_only=True)
    message_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def get_employee(self, obj):
        return User.objects.get(id=obj.id).employee
    
    def get_message_count(self, obj):
        request = self.context['request']
        job_id = self.context['job_id']
        if not request.user.is_authenticated:
            return 0
    
        m_messages =  JobMessage.objects.filter(job_id=job_id, sender_id=obj.id, receiver_readed=False)
        return m_messages.count()
        