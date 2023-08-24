
from message.models import *

class NotificationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_count = 0

    def __call__(self, request):
        
        self.checkMessagesIncoming(request)
        request.session['message_count'] = self.message_count
        response = self.get_response(request)
        return response
    
    # Check if client IP is allowed
    def process_request(self, request):
        
       # If IP is allowed we don't do anything
        return None
    
    def process_response(self, request, response):
        self.message_count = 30
        return response
    

    def checkMessagesIncoming(self, request):
        try:
            if not request.user.is_authenticated:
                self.message_count = 0
                return
            
            
            user_id = request.user.id
            user_type = request.user.user_type
            is_superuser = request.user.is_superuser
            
            if is_superuser:
                new_jobs = Job.objects.filter(is_active=False)
                self.message_count = new_jobs.count()
                return
            else:
                if user_type == "employee":
                    m_messages = JobMessage.objects.filter(receiver_id=user_id, receiver_readed=False)
                    self.message_count =  m_messages.count()
                    return
                else:
                    m_messages = JobMessage.objects.filter(receiver_id=user_id, receiver_readed=False)
                    self.message_count =  m_messages.count()
                    return
        except:
            self.message_count = 0
            return 