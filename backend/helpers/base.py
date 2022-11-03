from django.views.generic.base import View
from election.models import Electiontiming
from datetime import date

class APIResponseBase(View):

    def __init__(self, **kwargs) -> None:
        super(APIResponseBase, self).__init__(**kwargs)

        self._context = None
        self._header_context = None
        self._data = {}

        self.include_header = False

        self.status = 'success'
        self.status_code = 200
        self.message = ''
        self.error_code = ''
        self.error_message = ''

    def get_request(self):
        return self.request

    def get_profile(self):
        return self.request.user if self.request.user.is_authenticated else None

    def get_request_args(self):
        return self.args

    def get_request_kwargs(self):
        return self.kwargs

    def get_param(self,p):
        r = self.get_request()
        if r.method == 'POST':
            return r.POST.getlist(p)
        if r.method == 'GET':
            return r.GET.getlist(p)
