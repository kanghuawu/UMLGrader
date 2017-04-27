from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return HttpResponseRedirect(reverse(tenant_grader.view, args=[request.user.username]))
