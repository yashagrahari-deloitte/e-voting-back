from election.models import Electiontiming
from datetime import date

class ElectionTimingHelper(object):

    def get_current_session_id():
        session = Electiontiming.objects.get(session_name=date.today().year)
        return session.uid

    def get_session_from_id(session_id):
        session = Electiontiming.objects.get(uid=session_id)
        return session