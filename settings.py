from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.0, participation_fee=0.0)
SESSION_CONFIGS = [
                dict(name='bank2_instruction_70nd', display_name='bank2_instruction_70nd', num_demo_participants=2, app_sequence=['bank2_instruction_70nd']),
                dict(name='bank2_game_70nd', display_name='bank2_game_70nd', num_demo_participants=2, app_sequence=['bank2_game_70nd']),
                dict(name='bank2_postgame_70nd', display_name='bank2_postgame_70nd', num_demo_participants=2, app_sequence=['bank2_postgame_70nd']),
                dict(name='bank2_70nd_fullset', display_name='bank2_70nd_fullset', num_demo_participants=2, app_sequence=['bank2_instruction_70nd','bank2_game_70nd', 'bank2_postgame_70nd']),

                dict(name='bank2_instruction_70d', display_name='bank2_instruction_70d', num_demo_participants=2, app_sequence=['bank2_instruction_70d']),
                dict(name='bank2_game_70d', display_name='bank2_game_70d', num_demo_participants=2, app_sequence=['bank2_game_70d']),
                dict(name='bank2_postgame_70d', display_name='bank2_postgame_70d', num_demo_participants=2, app_sequence=['bank2_postgame_70d']),
                dict(name='bank2_70d_fullset', display_name='bank2_70d_fullset', num_demo_participants=2, app_sequence=['bank2_instruction_70d','bank2_game_70d', 'bank2_postgame_70d'])
                ]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = [
    'b1_part1_round', 'b1_part1_payoff', 'b1_part1_state', 'b1_part1_path', 'b1_part1_other_path',
    'b1_part2_round', 'b1_part2_payoff', 'b1_part2_state', 'b1_part2_path', 'b1_part2_other_path',
    'b1_belief_round', 'b1_belief_round_state', 'b1_belief_period1choice', 'b1_belief_period1_actual_choice', 'b1_belief_period1_draw1', 'b1_belief_period1_draw2', 'b1_belief_period1_payoff',
    'b1_total_payment',

    'b2_part1_round', 'b2_part1_payoff', 'b2_part1_state', 'b2_part1_path', 'b2_part1_other_path',
    'b2_part2_round', 'b2_part2_payoff', 'b2_part2_state', 'b2_part2_path', 'b2_part2_other_path',
    'b2_belief_period1_round', 'b2_belief_period1choice', 'b2_belief_period1_actual_choice', 'b2_belief_period1_draw1', 'b2_belief_period1_draw2', 'b2_belief_period1_payoff',
    'b2_belief_state_round', 'b2_belief_state', 'b2_belief_actual_state', 'b2_belief_picked_state',  'b2_belief_state_draw1', 'b2_belief_state_draw2', 'b2_belief_state_payoff',
    'b2_total_payment',

    'bret_boxes_collected','bret_bomb','bret_payoff_dollars',
]
SESSION_FIELDS = []
THOUSAND_SEPARATOR = ''
ROOMS = [
    dict(name='Session-d', display_name='Session-d', participant_label_file='_rooms/Session-d.txt'),
    dict(name='Session-nd', display_name='Session-nd', participant_label_file='_rooms/Session-nd.txt')
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = '82a812983eb3641cd91d6646538ae450fcd94e9ff69fdb0d58fc5c10cf223963a35c011d131625eaad0eeabe786ffcdb9769'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
