from election.models import Electiontiming
from datetime import date

class ElectionTimingHelper(object):

    def get_current_session():
        session = Electiontiming.objects.get(session_name=date.today().year)
        return session

