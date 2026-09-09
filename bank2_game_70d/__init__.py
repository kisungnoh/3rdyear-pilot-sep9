from otree.api import *
import random

doc = ''
class C(BaseConstants):
    # built-in constants
    NAME_IN_URL = 'bank2_game_70d'
    PLAYERS_PER_GROUP = 2
    PART1_ROUNDS = 3
    NUM_ROUNDS = 8
    # user-defined constants
    ENDOWMENT = 10
    DELAY_COST = 1
    SUCCESS_PAYOFF = 18
    FAIL_PAYOFF = 0
    LOW_PROB = 15
    MEDIUM_PROB = 70
    HIGH_PROB = 15
    STATE_CORR = 70
    RAND_MAX = 100
    BELIEF_REWARD = 4  # payment for correct belief report
    REAL_WORLD_CURRENCY_PER_POINT = 0.5
    # Set to True to re-enable the recommendation treatment (kept for the 'd' variant parity).
    RECOMMENDATION_ENABLED = True
    # Set to True to re-enable the Period 2 belief elicitation on SecondPeriod.
    SECOND_PERIOD_BELIEF_ENABLED = True

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    otherbank_state = models.StringField()
    otherbank_withdrawals = models.IntegerField(blank=True)
    yourbank_state = models.StringField()
    
class Player(BasePlayer):
    first_choice = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        label='',
        widget=widgets.RadioSelect)
    second_choice = models.StringField(
        blank=True,
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        label='',
        widget=widgets.RadioSelect)

    # Choice path
    path = models.StringField(blank=True)
    other_path = models.StringField(blank=True)

    # Period 1 belief - other's choice
    belief_period1choice = models.IntegerField(
        blank=True,
        label='How likely do you think the other participant chose Withdraw in Period 1? (%)')
    belief_period1_draw1 = models.IntegerField(blank=True)
    belief_period1_draw2 = models.IntegerField(blank=True)
    belief_period1_rewarded = models.BooleanField(blank=True)

    # Period 1 belief - state
    belief_low = models.IntegerField(blank=True, label='Probability the state is Low (%)')
    belief_med = models.IntegerField(blank=True, label='Probability the state is Medium (%)')
    belief_high = models.IntegerField(blank=True, label='Probability the state is High (%)')
    belief_state_draw1 = models.IntegerField(blank=True)
    belief_state_draw2 = models.IntegerField(blank=True)
    belief_state_rewarded = models.BooleanField(blank=True)

    # Period 2 belief - other's choice (elicited only, not paid)
    belief_period2choice = models.IntegerField(
        blank=True,
        label='How likely do you think the other participant will choose Withdraw in Period 2? (%)')

    # Recommendation
    recommendation = models.StringField(blank=True, label='Recommendation (if any):')

# --- bank1_game data pool ---
# Plug in the collected bank1_game data here before running the actual experiment.
# Each entry is [otherbank_state, otherbank_withdrawals] where otherbank_state is 'Low'/'Medium'/'High' and
# otherbank_withdrawals is the number of withdrawals (early + late) in the selected game.
# Example: OTHERBANK_DATA = [['Low', 2], ['Medium', 1], ['High', 0], ...]
# When non-empty, each group's otherbank_state and otherbank_withdrawals are drawn by random.choice().
# When empty (default), falls back to probability-based random draw with hardcoded DEMO_OTHERBANK_WITHDRAWALS
# (Low→2, Medium→1, High→0).
OTHERBANK_DATA = []

DEMO_WITHDRAWALS = {'Low': 2, 'Medium': 1, 'High': 0}

# --- Helper functions ---

def draw_state(rand):
    if rand <= C.LOW_PROB:
        return 'Low'
    elif rand <= C.LOW_PROB + C.MEDIUM_PROB:
        return 'Medium'
    else:
        return 'High'


def draw_correlated_state(otherbank_state):
    rand = random.randint(1, C.RAND_MAX)
    if rand <= C.STATE_CORR:
        return otherbank_state
    else:
        other_states = [s for s in ['Low', 'Medium', 'High'] if s != otherbank_state]
        return random.choice(other_states)


def get_player_path(player: Player):
    if player.first_choice == 'withdraw':
        return 'early'
    elif player.second_choice == 'withdraw':
        return 'late'
    else:
        return 'stay'


def get_payoff(path, other_path, state):
    if state == 'Low':
        if path == 'early':
            return C.ENDOWMENT
        elif path == 'late':
            return C.ENDOWMENT - C.DELAY_COST
        else:  # stay
            return C.FAIL_PAYOFF
    elif state == 'Medium':
        if path == 'early':
            return C.ENDOWMENT
        elif path == 'late':
            if other_path == 'stay':
                return C.ENDOWMENT
            else:  # other is early or late
                return C.ENDOWMENT - C.DELAY_COST
        else:  # stay
            if other_path == 'stay':
                return C.SUCCESS_PAYOFF
            else:
                return C.FAIL_PAYOFF
    else:  # High
        if path == 'early':
            return C.ENDOWMENT
        elif path == 'late':
            return C.ENDOWMENT
        else:  # stay
            return C.SUCCESS_PAYOFF


def calculate_payoffs(group: Group):
    state = group.yourbank_state
    for p in group.get_players():
        other = p.get_others_in_group()[0]
        p.payoff = get_payoff(
            get_player_path(p),
            get_player_path(other),
            state
        )


# --- Session creation ---

def creating_session(subsession: Subsession):
    subsession.group_randomly()

    for group in subsession.get_groups():
        if OTHERBANK_DATA:
            otherbank_state, otherbank_withdrawals = random.choice(OTHERBANK_DATA)
        else:
            otherbank_state = draw_state(random.randint(1, C.RAND_MAX))
            otherbank_withdrawals = DEMO_WITHDRAWALS[otherbank_state]
        group.otherbank_state = otherbank_state
        group.otherbank_withdrawals = otherbank_withdrawals
        group.yourbank_state = draw_correlated_state(otherbank_state)

    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.b2_part1_round = random.randint(1, C.PART1_ROUNDS)

    if subsession.round_number == C.PART1_ROUNDS + 1:
        for player in subsession.get_players():
            r1, r2, r3 = random.sample(range(C.PART1_ROUNDS + 1, C.NUM_ROUNDS + 1), 3)
            player.participant.b2_part2_round    = r1  # game payoff round
            player.participant.b2_belief_period1_round = r2  # belief_period1choice payment round (other's Period 1 choice)
            player.participant.b2_belief_state_round  = r3  # state belief payment round



class Part1Intro(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        
        return player.round_number == 1
        
class FirstPeriod(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        fields = ['first_choice']
        if player.round_number > C.PART1_ROUNDS:
            fields += ['belief_period1choice', 'belief_low', 'belief_med', 'belief_high']
        return fields

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
            sw_payoff=C.ENDOWMENT-C.DELAY_COST,
            unmatched_corr=(100-C.STATE_CORR)//2,
            show_beliefs=player.round_number > C.PART1_ROUNDS,
            otherbank_withdrawals=player.group.otherbank_withdrawals,
            part2_rounds=C.NUM_ROUNDS-C.PART1_ROUNDS,
        )

    @staticmethod
    def error_message(player: Player, values):
        if player.round_number <= C.PART1_ROUNDS:
            return None
        low  = values.get('belief_low')  or 0
        med  = values.get('belief_med')  or 0
        high = values.get('belief_high') or 0
        if low + med + high != 100:
            return f'Your state beliefs must sum to 100% (currently {low + med + high}%).'

class AfterFirstPeriod(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            if not C.RECOMMENDATION_ENABLED:
                player.recommendation = ''
                continue

            other = player.get_others_in_group()[0]
            if player.first_choice == 'withdraw':
                player.recommendation = ''
            else:
                state = group.yourbank_state
                other_withdrew_period1 = (other.first_choice == 'withdraw')
                if state == 'Low':
                    player.recommendation = 'Withdraw'
                elif state == 'High':
                    player.recommendation = 'Stay'
                else:  # Medium
                    player.recommendation = 'Withdraw' if other_withdrew_period1 else 'Stay'

class SecondPeriod(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        fields = ['second_choice']
        if C.SECOND_PERIOD_BELIEF_ENABLED and player.round_number > C.PART1_ROUNDS:
            fields += ['belief_period2choice']
        return fields

    @staticmethod
    def is_displayed(player: Player):
        return player.first_choice == 'stay'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
            sw_payoff=C.ENDOWMENT-C.DELAY_COST,
            unmatched_corr=(100-C.STATE_CORR)//2,
            ask_belief=C.SECOND_PERIOD_BELIEF_ENABLED and player.round_number > C.PART1_ROUNDS,
            otherbank_withdrawals=player.group.otherbank_withdrawals,
            recommendation=player.recommendation,
            show_recommendation=C.RECOMMENDATION_ENABLED,
            part2_rounds=C.NUM_ROUNDS-C.PART1_ROUNDS,
        )
    
class AfterSecondPeriod(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        calculate_payoffs(group)

        for player in group.get_players():
            other = player.get_others_in_group()[0]
            player.path = get_player_path(player)
            player.other_path = get_player_path(other)

            # Part 1 game payoff storage
            if player.round_number == player.participant.b2_part1_round:
                player.participant.b2_part1_payoff = float(player.payoff)
                player.participant.b2_part1_state = player.group.yourbank_state
                player.participant.b2_part1_path = get_player_path(player)
                player.participant.b2_part1_other_path = get_player_path(other)

            if player.round_number > C.PART1_ROUNDS:

                # Part 2 game payoff storage
                if player.round_number == player.participant.b2_part2_round:
                    player.participant.b2_part2_payoff = float(player.payoff)
                    player.participant.b2_part2_state = player.group.yourbank_state
                    player.participant.b2_part2_path = get_player_path(player)
                    player.participant.b2_part2_other_path = get_player_path(other)

                # Other's choice belief payment (Period 1, BQSR)
                if player.round_number == player.participant.b2_belief_period1_round:
                    other_withdrew_period1 = (other.first_choice == 'withdraw')
                    player.participant.b2_belief_period1choice = player.belief_period1choice
                    player.participant.b2_belief_period1_actual_choice = 'withdraw' if other_withdrew_period1 else 'stay'

                    r1_period1 = random.randint(0, 100)
                    r2_period1 = random.randint(0, 100)
                    player.belief_period1_draw1 = r1_period1
                    player.belief_period1_draw2 = r2_period1
                    player.participant.b2_belief_period1_draw1 = r1_period1
                    player.participant.b2_belief_period1_draw2 = r2_period1

                    if other_withdrew_period1:
                        player.belief_period1_rewarded = (player.belief_period1choice > r1_period1) or (player.belief_period1choice > r2_period1)
                    else:
                        player.belief_period1_rewarded = ((100 - player.belief_period1choice) > r1_period1) or ((100 - player.belief_period1choice) > r2_period1)

                    player.participant.b2_belief_period1_payoff = (
                        C.BELIEF_REWARD if player.belief_period1_rewarded else 0
                    )

                # State belief payment (Period 1, BQSR)
                if player.round_number == player.participant.b2_belief_state_round:
                    actual_state = player.group.yourbank_state
                    player.participant.b2_belief_actual_state = actual_state

                    picked_state = random.choice(['Low', 'Medium', 'High'])
                    player.participant.b2_belief_picked_state = picked_state

                    if picked_state == 'Low':
                        reported_p = player.belief_low
                    elif picked_state == 'Medium':
                        reported_p = player.belief_med
                    else:
                        reported_p = player.belief_high
                    player.participant.b2_belief_state = reported_p

                    r1_state = random.randint(0, 100)
                    r2_state = random.randint(0, 100)
                    player.belief_state_draw1 = r1_state
                    player.belief_state_draw2 = r2_state
                    player.participant.b2_belief_state_draw1 = r1_state
                    player.participant.b2_belief_state_draw2 = r2_state

                    if actual_state == picked_state:
                        player.belief_state_rewarded = (reported_p > r1_state) or (reported_p > r2_state)
                    else:
                        player.belief_state_rewarded = ((100 - reported_p) > r1_state) or ((100 - reported_p) > r2_state)
                    player.participant.b2_belief_state_payoff = (
                        C.BELIEF_REWARD if player.belief_state_rewarded else 0
                    )

class Results(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        
        other = player.get_others_in_group()[0]
        return dict(
            round_number=player.round_number,
            other=other,
            sw_payoff=10-C.DELAY_COST,
            yourbank_state=player.group.yourbank_state,
            otherbank_state=player.group.otherbank_state,
            otherbank_withdrawals=player.group.otherbank_withdrawals,
            payoff_value=int(player.payoff)
        )

class Part1Outro(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == C.PART1_ROUNDS


class AfterPart1(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants to finish Part 1.'

    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == C.PART1_ROUNDS


class Part2Intro1(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.PART1_ROUNDS

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            part2_rounds=C.NUM_ROUNDS-C.PART1_ROUNDS
        )

class Part2Intro2(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.PART1_ROUNDS

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            part2_rounds=C.NUM_ROUNDS-C.PART1_ROUNDS
        )

class Part2Intro3(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.PART1_ROUNDS

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            part2_rounds=C.NUM_ROUNDS-C.PART1_ROUNDS
        )

class WaitforAll(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants to finish Part 2 instructions.'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.PART1_ROUNDS


class Part2Outro(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class AfterPart2(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants to finish Part 2.'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [Part1Intro, FirstPeriod, AfterFirstPeriod, SecondPeriod, AfterSecondPeriod,
                 Results, Part1Outro, AfterPart1,
                 Part2Intro1, Part2Intro2, Part2Intro3, WaitforAll, Part2Outro, AfterPart2]