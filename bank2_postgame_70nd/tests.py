from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield PostSurveyQ1, dict(
            prior_state_belief_low=15, prior_state_belief_med=70, prior_state_belief_high=15,
            prior_state_certainty=60,
        )
        yield PostSurveyQ2, dict(prior_choice_belief=50, prior_choice_certainty=60)
        yield PostSurveyQ3, dict(
            period1_choice_0='stay', period1_certainty_0=60,
            period1_choice_1='stay', period1_certainty_1=60,
            period1_choice_2='withdraw', period1_certainty_2=60,
        )
        yield PostSurveyQ4, dict(
            period1_belief_choice_0='stay', period1_belief_certainty_0=60,
            period1_belief_choice_1='stay', period1_belief_certainty_1=60,
            period1_belief_choice_2='withdraw', period1_belief_certainty_2=60,
        )
        yield PostSurveyQ5, dict(
            period1_state_0='low', period1_state_certainty_0=60,
            period1_state_1='med', period1_state_certainty_1=60,
            period1_state_2='high', period1_state_certainty_2=60,
        )
        yield PostSurveyQ6, dict(sw_reason='test')
        yield CRT, dict(CRT1=1, CRT2=1, CRT3=1, crt_time_expired=False)
        yield Demographic, dict(age=25, gender='M', major='ECON')

        yield Payment
        expect(self.player.participant.b2_total_payment is not None, True)
