
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.decorators import method_decorator
from members.models import RICEvent
from members.forms import RICForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

from django.views import View
from .models import RICEvent, Comment
from .forms import CommentForm
from django.contrib.auth.mixins import UserPassesTestMixin

# Check if the user is in the Student group
def is_student(user):
    return user.groups.filter(name='Student').exists()

# Decorator for views accessible to students only
def student_required(view_func):
    decorated_view_func = user_passes_test(is_student)
    return decorated_view_func(view_func)

# Decorator for views accessible to students and editors
def student_or_editor_required(view_func):
    decorated_view_func = user_passes_test(lambda u: is_student(u) or is_editor(u))
    return decorated_view_func(view_func)



# Check if the user is in the Editor group
def is_editor(user):
    return user.groups.filter(name='Editor').exists()

# Decorator for views accessible to editors only
def editor_required(view_func):
    decorated_view_func = user_passes_test(is_editor)
    return decorated_view_func(view_func)
class ViewRICEventSubmissionView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Editor').exists()

    def get(self, request, event_id):
        event = get_object_or_404(RICEvent, pk=event_id)
        comments = Comment.objects.filter(ricevent=event)
        form = CommentForm()
        is_editor = self.request.user.groups.filter(name='Editor').exists()  # Check if the user is an editor
        context = {
            'event': event,
            'comments': comments,
            'form': form,
            'is_editor': is_editor,  # Pass the is_editor variable to the template
        }
        return render(request, 'editor/view_submission.html', context)

    def post(self, request, event_id):
        event = get_object_or_404(RICEvent, pk=event_id)
        comments = Comment.objects.filter(ricevent=event)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment_text']
            Comment.objects.create(ricevent=event, editor=request.user, comment_text=comment)
            return redirect('editor:view_submission', event_id=event_id)
        context = {
            'event': event,
            'comments': comments,
            'form': form,
            'is_editor': self.request.user.groups.filter(name='Editor').exists(),  # Check if the user is an editor
        }
        return render(request, 'editor/view_submission.html', context)

class ViewAllRICEventsView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Editor').exists()

    def get(self, request):
        events_list = RICEvent.objects.all().order_by('-id')
        paginator = Paginator(events_list, 10)  # Show 10 events per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj
        }
        return render(request, 'editor/view_all_submissions.html', context)

class ChangeStatusView(LoginRequiredMixin, View):
    @method_decorator(editor_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, event_id):
        event = get_object_or_404(RICEvent, pk=event_id)
        status = request.POST.get('status')
        if status == 'Accepted':
            event.selected = True
        event.status = status
        event.save()
        return redirect('editor:change_status', event_id=event_id)
