from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Welcome
        yield Intro1
        yield Intro2
        yield Intro3Low
        yield Intro3High
        yield Intro3Med
        yield Intro3Unknown
        yield Intro4OtherBank
        yield Intro5Correlation
        yield Intro6Recommendation
        yield Intro7
        yield Intro8
        yield CQ1, dict(comprehension_q1='10')
        yield CQ2, dict(comprehension_q2='10-18')
        yield CQ3, dict(comprehension_q3='0-10')
        yield CQ4, dict(comprehension_q4='false')
        yield CQ5, dict(comprehension_q5='wsw')
        yield CQ6, dict(comprehension_q6='true')
        yield CQ7, dict(comprehension_q7='true')
        yield CQ8, dict(comprehension_q8='new')
