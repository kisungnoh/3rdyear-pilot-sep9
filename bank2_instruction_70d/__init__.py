from otree.api import *
from otree.forms import widgets as otree_widgets


class HiddenFieldWidget(otree_widgets.BaseWidget):
    """Renders a form field as <input type="hidden">, for values set via JS rather than user input."""
    def get_html_fragments(self):
        yield '<input type="hidden" %s>' % self.attrs()


class C(BaseConstants):
    NAME_IN_URL = 'bank2_instruction_70d'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    PART1_ROUNDS = 3
    # user-defined constants
    ENDOWMENT = 10
    DELAY_COST = 1
    SUCCESS_PAYOFF = 18
    FAIL_PAYOFF = 0
    LOW_PROB = 15
    MEDIUM_PROB = 70
    HIGH_PROB = 15
    STATE_CORR = 70
    REAL_WORLD_CURRENCY_PER_POINT = 0.5


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Fields are numbered to match their page's position in page_sequence (CQ1..CQ7).
    comprehension_q1 = models.StringField(
        choices=[['10', "You receive 10, regardless of the state of your bank or the other participant's decision."],
                     ['depends', "Your payoff depends on the state of your bank or the other participant's decision."]],
        label="If you choose to withdraw in Period 1,",
        widget=widgets.RadioSelect)
    comprehension_q1_fail = models.IntegerField(
        initial=0, min=0, max=1, blank=True, widget=HiddenFieldWidget())
    comprehension_q2 = models.StringField(
        choices=[['10-10', "(10, 10)"],
                 ['10-18', "(10, 18)"],
                 ['18-10', "(18, 10)"],
                 ['18-18', "(18, 18)"]],
        label="",
        widget=widgets.RadioSelect)
    comprehension_q2_fail = models.IntegerField(
        initial=0, min=0, max=1, blank=True, widget=HiddenFieldWidget())
    comprehension_q3 = models.StringField(
        choices=[['10-10', "(10, 10)"],
                 ['10-0', "(10, 0)"],
                 ['0-10', "(0, 10)"],
                 ['18-18', "(18, 18)"]],
        label="",
        widget=widgets.RadioSelect)
    comprehension_q3_fail = models.IntegerField(
        initial=0, min=0, max=1, blank=True, widget=HiddenFieldWidget())
    comprehension_q4 = models.StringField(
        choices=[['true', "True"],
                 ['false', "False"]],
        label="Participants who were the customers of the Other Bank knew only the probability of their bank's state and not the exact state, just like in today's experiment.",
        widget=widgets.RadioSelect)
    comprehension_q4_fail = models.IntegerField(
        initial=0, min=0, max=1, blank=True, widget=HiddenFieldWidget())
    comprehension_q5 = models.StringField(
        choices=[['w', "Withdraw in Period 1 only (W)"],
                     ['sw', "Withdraw in Period 2 only (SW)"],
                     ['wsw', "Withdraw in either Period 1 or Period 2 (W or SW)"]],
        label="When making decisions, you will be informed of the Other Bank withdrawals, which shows the number of the Other Bank customers who chose",
        widget=widgets.RadioSelect)
    comprehension_q5_fail = models.IntegerField(
        initial=0, min=0, max=1, blank=True, widget=HiddenFieldWidget())
    comprehension_q6 = models.StringField(
        choices=[['true', "True"],
                 ['false', "False"]],
        label="Your Bank is likely to be in the same state as the Other Bank with 70% probability, but it can still be in a different state. For example, the Other Bank could be in the High state while Your Bank is in the Low state. Any combination of states is possible.",
        widget=widgets.RadioSelect)
    comprehension_q6_fail = models.IntegerField(
        initial=0, min=0, max=1, blank=True, widget=HiddenFieldWidget())
    comprehension_q7 = models.StringField(
        choices=[['true', "True"],
                     ['false', "False"]],
        label="You receive the recommendation only if you choose Stay in Period 1.",
        widget=widgets.RadioSelect)
    comprehension_q7_fail = models.IntegerField(
        initial=0, min=0, max=1, blank=True, widget=HiddenFieldWidget())
    comprehension_q8 = models.StringField(
        choices=[['same', 'The same participant'],
                 ['new', 'A new participant']],
        label='In each game, you are likely to be paired with:',
        widget=widgets.RadioSelect)
    comprehension_q8_fail = models.IntegerField(
        initial=0, min=0, max=1, blank=True, widget=HiddenFieldWidget())


class Welcome(Page):
    pass

# --- Progress bar shown on Intro1 through Intro6 (Intro3 variants all count as step 3) ---
INSTRUCTIONS_TOTAL_STEPS = 7

def progress_vars(step):
    return dict(
        progress_step=step,
        progress_total=INSTRUCTIONS_TOTAL_STEPS,
        progress_pct=round(100 * step / INSTRUCTIONS_TOTAL_STEPS),
    )

class Intro1(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            unmatched_corr=(100 - C.STATE_CORR) // 2,
            sw_payoff=C.ENDOWMENT - C.DELAY_COST,
            **progress_vars(1),
        )

class Intro2(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            unmatched_corr=(100 - C.STATE_CORR) // 2,
            sw_payoff=C.ENDOWMENT - C.DELAY_COST,
            **progress_vars(2),
        )

class Intro3(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            unmatched_corr=(100 - C.STATE_CORR) // 2,
            sw_payoff=C.ENDOWMENT - C.DELAY_COST,
            **progress_vars(3),
        )


class Intro3Low(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST, **progress_vars(3))

class Intro3Med(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST, **progress_vars(3))


class Intro3High(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST, **progress_vars(3))

class Intro3Unknown(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST, **progress_vars(3))

class Intro4OtherBank(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST, **progress_vars(4))

class Intro5Correlation(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            unmatched_corr=(100 - C.STATE_CORR) // 2,
            sw_payoff=C.ENDOWMENT - C.DELAY_COST,
            **progress_vars(5),
        )
class Intro6Recommendation(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            unmatched_corr=(100 - C.STATE_CORR) // 2,
            sw_payoff=C.ENDOWMENT - C.DELAY_COST,
            **progress_vars(6),
        )

class Intro7(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return progress_vars(7)

class Intro8(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(unmatched_corr=(100 - C.STATE_CORR) // 2)

class WaitForAll(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants.'

# --- Comprehension check pages (one question or group per page) ---
# Page class names match their template files, which are numbered by display order.

class CQ1(Page):
    form_model = 'player'
    form_fields = ['comprehension_q1', 'comprehension_q1_fail']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            sw_payoff=C.ENDOWMENT - C.DELAY_COST,
            unmatched_corr=(100 - C.STATE_CORR) // 2,
        )

class CQ2(Page):
    form_model = 'player'
    form_fields = ['comprehension_q2', 'comprehension_q2_fail']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            sw_payoff=C.ENDOWMENT - C.DELAY_COST,
            unmatched_corr=(100 - C.STATE_CORR) // 2,
        )

class CQ3(Page):
    form_model = 'player'
    form_fields = ['comprehension_q3', 'comprehension_q3_fail']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            sw_payoff=C.ENDOWMENT - C.DELAY_COST,
            unmatched_corr=(100 - C.STATE_CORR) // 2,
        )

class CQ4(Page):
    form_model = 'player'
    form_fields = ['comprehension_q4', 'comprehension_q4_fail']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(unmatched_corr=(100 - C.STATE_CORR) // 2)

class CQ5(Page):
    form_model = 'player'
    form_fields = ['comprehension_q5', 'comprehension_q5_fail']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(unmatched_corr=(100 - C.STATE_CORR) // 2)

class CQ6(Page):
    form_model = 'player'
    form_fields = ['comprehension_q6', 'comprehension_q6_fail']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(unmatched_corr=(100 - C.STATE_CORR) // 2)

class CQ7(Page):
    form_model = 'player'
    form_fields = ['comprehension_q7', 'comprehension_q7_fail']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(unmatched_corr=(100 - C.STATE_CORR) // 2)

class CQ8(Page):
    form_model = 'player'
    form_fields = ['comprehension_q8', 'comprehension_q8_fail']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(unmatched_corr=(100 - C.STATE_CORR) // 2)

page_sequence = [Welcome, Intro1, Intro2, Intro3Low, Intro3High, Intro3Med, Intro3Unknown, Intro4OtherBank, Intro5Correlation, Intro6Recommendation, Intro7, Intro8,
                 WaitForAll,
                 CQ1, CQ2, CQ3, CQ4, CQ5, CQ6, CQ7, CQ8]
