from . import *


class PlayerBot(Bot):
    def play_round(self):
        if self.player.round_number == 1:
            yield Part1Intro

        first_stage_fields = dict(first_choice='stay')
        if self.player.round_number > C.PART1_ROUNDS:
            first_stage_fields.update(
                belief_period1choice=50, belief_low=15, belief_med=70, belief_high=15
            )
        yield FirstPeriod, first_stage_fields

        second_stage_fields = dict(second_choice='withdraw' if self.player.round_number % 2 == 0 else 'stay')
        if C.SECOND_PERIOD_BELIEF_ENABLED and self.player.round_number > C.PART1_ROUNDS:
            second_stage_fields.update(belief_period2choice=50)
        yield SecondPeriod, second_stage_fields

        yield Results

        if self.player.round_number == C.PART1_ROUNDS:
            yield Part1Outro
            yield Part2Intro1
            yield Part2Intro2
            yield Part2Intro3

        if self.player.round_number == C.NUM_ROUNDS:
            yield Part2Outro
