from rest_framework import serializers
from .models import *
from customAdmin.models import *
from accounts.models import *
from proposal.models import *
from message.models import *


class JobSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    work_at = serializers.SerializerMethodField(read_only=True)
    work_hour = serializers.SerializerMethodField(read_only=True)
    work_type = serializers.SerializerMethodField(read_only=True)
    skills = serializers.SerializerMethodField(read_only=True)
    proposal_status = serializers.SerializerMethodField(read_only=True)
    message_count = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)
    is_favourite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"

    def get_user(self, obj):        
        m_data =  User.objects.get(id=obj.user_id)        
        return m_data
    
    def get_category(self, obj):       
        m_data =  Category.objects.get(id=obj.category_id)        
        return m_data
    
    def get_work_at(self, obj):          
        m_data =  Prefecture.objects.get(id=obj.work_at_id)        
        return m_data
    
    def get_work_hour(self, obj):          
        m_data =  WorkHour.objects.get(id=obj.work_hour_id)        
        return m_data
    
    def get_work_type(self, obj):        
        m_data =  WorkType.objects.get(id=obj.work_type_id)        
        return m_data
    
    def get_skills(self, obj):        
        m_skills =  JobSkill.objects.filter(job_id=obj.id)        
        return m_skills

    def get_proposal_status(self, obj):   
        request = self.context['request']
        if not request.user.is_authenticated:
            return 0
        
        m_list = Proposal.objects.filter(job_id=obj.id, user_id=request.user.id)
        if m_list.count() > 0:
            return m_list[0].status
        else:
            return 0
    
    def get_message_count(self, obj):
        request = self.context['request']
        if not request.user.is_authenticated:
            return 0
        
        if request.user.user_type == "employee":            
            m_list = Proposal.objects.filter(job_id=obj.id, user_id=request.user.id)
            if m_list.count() > 0:
                m_messages =  JobMessage.objects.filter(job_id=obj.id, receiver_id=request.user.id, receiver_readed=False)
                return m_messages.count()
            else:
                return 0        
        else:
            m_messages =  JobMessage.objects.filter(job_id=obj.id, receiver_id=request.user.id, receiver_readed=False)
            return m_messages.count()
    
    def get_like_count(self, obj):
        m_likes = JobLike.objects.filter(job_id=obj.id)
        return m_likes.count()
    
    def get_is_like(self, obj):
        request = self.context['request']
        if not request.user.is_authenticated:
            return False
        
        try:
            JobLike.objects.get(job_id=obj.id, user_id=request.user.id)
            return True
        except JobLike.DoesNotExist:
            return False
    
    def get_is_favourite(self, obj):
        request = self.context['request']
        if not request.user.is_authenticated:
            return False
        
        try:
            JobFavourite.objects.get(job_id=obj.id, user_id=request.user.id)
            return True
        except JobFavourite.DoesNotExist:
            return False
        
        




class JobDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"

    def get_author(self, obj):
        # category_id = self.context["category_id"]
        
        try:
            m_user =  User.objects.get(id=obj.author_id)
        except User.DoesNotExist:
            return {
                "username" : ""
            }
        
        return m_user
