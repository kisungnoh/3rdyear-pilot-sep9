from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'bank2_postgame_70d'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PARTICIPATION_FEE = 5
    REAL_WORLD_CURRENCY_PER_POINT = 0.5

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # Prior belief — likelihood of each state if Other Bank withdrawals were unknown
    prior_state_belief_low  = models.IntegerField(blank=True, label="")
    prior_state_belief_med  = models.IntegerField(blank=True, label="")
    prior_state_belief_high = models.IntegerField(blank=True, label="")
    prior_state_certainty   = models.IntegerField(min=50, max=100, blank=True, label="")

    # Prior belief — likelihood of other's Period 1 choice, if Other Bank withdrawals were unknown
    prior_choice_belief    = models.IntegerField(blank=True, label="")
    prior_choice_certainty = models.IntegerField(min=50, max=100, blank=True, label="")

    # Period 1 — by Other Bank withdrawal count (0, 1, 2)
    period1_choice_0 = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_certainty_0 = models.IntegerField(min=50, max=100, blank=True, label="")

    period1_choice_1 = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_certainty_1 = models.IntegerField(min=50, max=100, blank=True, label="")

    period1_choice_2 = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_certainty_2 = models.IntegerField(min=50, max=100, blank=True, label="")

    # Period 1 — belief about the other participant's choice, by Other Bank withdrawal count (0, 1, 2)
    period1_belief_choice_0 = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_belief_certainty_0 = models.IntegerField(min=50, max=100, blank=True, label="")

    period1_belief_choice_1 = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_belief_certainty_1 = models.IntegerField(min=50, max=100, blank=True, label="")

    period1_belief_choice_2 = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_belief_certainty_2 = models.IntegerField(min=50, max=100, blank=True, label="")

    # Period 1 — belief about the state of Your Bank, by Other Bank withdrawal count (0, 1, 2)
    period1_state_0 = models.StringField(
        choices=[['low', 'Low'], ['med', 'Medium'], ['high', 'High']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_state_certainty_0 = models.IntegerField(min=50, max=100, blank=True, label="")

    period1_state_1 = models.StringField(
        choices=[['low', 'Low'], ['med', 'Medium'], ['high', 'High']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_state_certainty_1 = models.IntegerField(min=50, max=100, blank=True, label="")

    period1_state_2 = models.StringField(
        choices=[['low', 'Low'], ['med', 'Medium'], ['high', 'High']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_state_certainty_2 = models.IntegerField(min=50, max=100, blank=True, label="")

    # Explanation
    sw_reason = models.LongStringField(
        blank=True,
        label=""
    )

    # CRT
    CRT1 = models.FloatField(blank=True)
    CRT2 = models.FloatField(blank=True)
    CRT3 = models.FloatField(blank=True)
    crt_time_expired = models.BooleanField(initial=False, blank=True, widget=widgets.CheckboxInput, label="")

    # Demographics
    age = models.IntegerField(label="What is your age?")
    gender = models.StringField(
        choices=[['M', 'Male'], ['F', 'Female'], ['NB', 'Non-binary'], ['PNTS', 'Prefer not to say']],
        label="How do you describe your gender?",
        widget=widgets.RadioSelect
    )
    major = models.StringField(
        choices=[
            ['ECON', 'Economics or Business (Kelley School)'],
            ['PSY', 'Psychology and Brain Sciences'],
            ['SOC', 'Other Social Sciences'],
            ['HUM', 'Humanities'],
            ['NAT', 'Natural Sciences, Mathematics'],
            ['TECH', 'Technology, Computer Science, or Engineering (e.g., Luddy School)'],
            ['OTHERS', 'Other major (not listed)'],
            ['PNTS', 'Prefer not to say']],
        label="What is your field of study?"
    )


def path_label(path):
    if path == 'early':
        return 'Withdraw in Period 1 (W)'
    elif path == 'late':
        return 'Stay in Period 1 → Withdraw in Period 2 (SW)'
    else:  # stay
        return 'Stay in Period 1 → Stay in Period 2 (SS)'


class PostSurveyQ1(Page):
    form_model = 'player'
    form_fields = [
        'prior_state_belief_low', 'prior_state_belief_med', 'prior_state_belief_high',
        'prior_state_certainty',
    ]


class PostSurveyQ2(Page):
    form_model = 'player'
    form_fields = ['prior_choice_belief', 'prior_choice_certainty']


class PostSurveyQ3(Page):
    form_model = 'player'
    form_fields = [
        'period1_choice_0', 'period1_certainty_0',
        'period1_choice_1', 'period1_certainty_1',
        'period1_choice_2', 'period1_certainty_2',
    ]


class PostSurveyQ4(Page):
    form_model = 'player'
    form_fields = [
        'period1_belief_choice_0', 'period1_belief_certainty_0',
        'period1_belief_choice_1', 'period1_belief_certainty_1',
        'period1_belief_choice_2', 'period1_belief_certainty_2',
    ]

class PostSurveyQ5(Page):
    form_model = 'player'
    form_fields = [
        'period1_state_0', 'period1_state_certainty_0',
        'period1_state_1', 'period1_state_certainty_1',
        'period1_state_2', 'period1_state_certainty_2',
    ]


class PostSurveyQ6(Page):
    form_model = 'player'
    form_fields = ['sw_reason']

class CRT(Page):
    form_model = 'player'
    form_fields = ['CRT1', 'CRT2', 'CRT3', 'crt_time_expired']

class Demographic(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major']

class Payment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Game payoffs
        part1_payoff        = int(player.participant.b2_part1_payoff)
        part2_payoff        = int(player.participant.b2_part2_payoff)

        # Period 1 belief — other's choice (BQSR)
        belief_period1_payoff    = int(player.participant.b2_belief_period1_payoff)
        belief_period1_withdraw  = int(player.participant.b2_belief_period1choice)
        belief_period1_stay      = 100 - belief_period1_withdraw
        belief_period1_actual_choice = player.participant.b2_belief_period1_actual_choice
        belief_period1_draw1  = int(player.participant.b2_belief_period1_draw1)
        belief_period1_draw2  = int(player.participant.b2_belief_period1_draw2)
        belief_period1_rewarded = belief_period1_payoff > 0

        # State belief (BQSR)
        belief_state_payoff  = int(player.participant.b2_belief_state_payoff)
        belief_actual_state  = player.participant.b2_belief_actual_state
        belief_picked_state  = player.participant.b2_belief_picked_state
        belief_state         = int(player.participant.b2_belief_state)
        belief_state_comp    = 100 - belief_state
        belief_state_draw1    = int(player.participant.b2_belief_state_draw1)
        belief_state_draw2    = int(player.participant.b2_belief_state_draw2)
        belief_state_rewarded = belief_state_payoff > 0

        # USD conversions
        part1_payoff_usd        = round(part1_payoff        * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        part2_payoff_usd        = round(part2_payoff        * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        belief_period1_payoff_usd    = round(belief_period1_payoff    * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        belief_state_payoff_usd = round(belief_state_payoff * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        # bret_payoff_usd      = player.participant.bret_payoff_dollars or 0.0
        total_earnings_usd   = round(
            (part1_payoff + part2_payoff + belief_period1_payoff + belief_state_payoff) * C.REAL_WORLD_CURRENCY_PER_POINT, 2
        )
        total_payment = round(total_earnings_usd + C.PARTICIPATION_FEE, 0)
        player.participant.b2_total_payment = total_payment

        return dict(
            # Part 1 game
            part1_round=player.participant.b2_part1_round,
            part1_payoff=part1_payoff,
            part1_payoff_usd=part1_payoff_usd,
            part1_state=player.participant.b2_part1_state,
            part1_path=path_label(player.participant.b2_part1_path),
            part1_other_path=path_label(player.participant.b2_part1_other_path),

            # Part 2 game
            part2_round=player.participant.b2_part2_round,
            part2_payoff=part2_payoff,
            part2_payoff_usd=part2_payoff_usd,
            part2_state=player.participant.b2_part2_state,
            part2_path=path_label(player.participant.b2_part2_path),
            part2_other_path=path_label(player.participant.b2_part2_other_path),

            # Period 1 belief — other's choice
            belief_period1_round=player.participant.b2_belief_period1_round,
            belief_period1_payoff=belief_period1_payoff,
            belief_period1_payoff_usd=belief_period1_payoff_usd,
            belief_period1_withdraw=belief_period1_withdraw,
            belief_period1_stay=belief_period1_stay,
            belief_period1_actual_choice=belief_period1_actual_choice,
            belief_period1_draw1=belief_period1_draw1,
            belief_period1_draw2=belief_period1_draw2,
            belief_period1_rewarded=belief_period1_rewarded,

            # State belief
            belief_state_round=player.participant.b2_belief_state_round,
            belief_state_payoff=belief_state_payoff,
            belief_state_payoff_usd=belief_state_payoff_usd,
            belief_actual_state=belief_actual_state,
            belief_picked_state=belief_picked_state,
            belief_state=belief_state,
            belief_state_comp=belief_state_comp,
            belief_state_draw1=belief_state_draw1,
            belief_state_draw2=belief_state_draw2,
            belief_state_rewarded=belief_state_rewarded,

            # Bret game
            # bret_boxes_collected=player.participant.bret_boxes_collected,
            # bret_bomb=player.participant.bret_bomb,
            # bret_payoff_usd=bret_payoff_usd,
            total_earnings_usd=total_earnings_usd,
            total_payment=total_payment,
        )

page_sequence = [Payment]
