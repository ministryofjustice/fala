from django.views.generic import TemplateView
# from django.shortcuts import render
from django.template import loader, Context
from django.conf import settings
from .forms import FeedbackForm
from feedback import zendesk


ZENDESK_CUSTOM_FIELD_USERAGENT = 23791776
ZENDESK_CUSTOM_FIELD_REFERRER = 26047167


class FeedbackView(TemplateView):
    template_name = 'feedback/index.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = FeedbackForm(data=request.POST or None)

        context.update({'form': form})

        if form.is_valid():
            user_agent = request.META.get('HTTP_USER_AGENT')

            feedback_data = {
                'feedback': form.data['feedback'],
                'referrer': form.data['referrer'],
                'user_agent': user_agent
            }

            template = loader.get_template('feedback/email.html')
            feedback = template.render(feedback_data)

            ticket = {
                'requester_id': settings.ZENDESK_DEFAULT_REQUESTER,
                'subject': '[TEST] FALA feedback',
                'comment': {
                    'body': feedback
                },
                'group_id': settings.ZENDESK_DEFAULT_GROUP_ID,
                'tags': ['feedback', 'fala'],
                'custom_fields': [
                    {
                        'id': ZENDESK_CUSTOM_FIELD_USERAGENT,
                        'value': user_agent,
                    },
                    {
                        'id': ZENDESK_CUSTOM_FIELD_REFERRER,
                        'value': form.data['referrer'],
                    }
                ],
            }

            zendesk.create_ticket({'ticket': ticket})

        return self.render_to_response(context)
