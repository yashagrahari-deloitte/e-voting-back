from election.models import Electiontiming
from datetime import date

class ElectionTimingHelper(object):

    def get_current_session():
        session = Electiontiming.objects.get(session_name=date.today().year)
        return session

    def generate_session_table(table_name,session_name):
        return table_name+session_name

