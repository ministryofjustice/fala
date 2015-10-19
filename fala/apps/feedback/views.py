from django.shortcuts import redirect
from django.views.generic import TemplateView
from .forms import FeedbackForm
from fala.apps.feedback.zendesk import zendesk_client


class FeedbackView(TemplateView):
    template_name = 'feedback/index.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        return self.post(request)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = FeedbackForm(data=request.POST or None)
        context.update({'form': form})

        if form.is_valid():
            response = zendesk_client.create_ticket(
                feedback_data={
                    'feedback': form.data.get('feedback'),
                    'referrer': form.data.get('referrer'),
                    'user_agent': request.META.get('HTTP_USER_AGENT')
                })

            if response['status'] < 300:
                return redirect('feedback_confirmation')
            else:
                context.update({'error': {
                    'message': 'Something went wrong. Please try again.',
                    'json': response['json']
                }})

        return self.render_to_response(context)


class FeedbackConfirmationView(TemplateView):
    template_name = 'feedback/confirmation.html'
