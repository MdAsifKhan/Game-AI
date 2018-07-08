import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# Class for Breakout fuzzy control
class BreakoutFuzzyControl:

    # Initializes all fuzzy variables and defines rules.
    def __init__(self):
        self.define_fuzzy_variables()
        self.define_rules()

        self.control_system = ctrl.ControlSystem(self.rules)
        self.control = ctrl.ControlSystemSimulation(self.control_system)

    # Defines fuzzy variables.
    def define_fuzzy_variables(self):
        self.close = [-1, 10, 14]
        self.far = [12, 25, 30]
        self.very_far = [28, 40, 50]
        self.too_far = [45, 60, 60]

        self.little_step = [0, 4, 6]
        self.mid_step = [5, 10, 12]
        self.big_step = [10, 14, 16]
        self.extreme_step = [14, 20, 20]

        self.distance_range = np.arange(0, 60)
        self.step_range = np.arange(0, 20)

        # Absolute distance between the ball and the player in range 0, 60.
        self.ball_distance = ctrl.Antecedent(self.distance_range, 'ball_distance')
        # Player steps in range 0, 20.
        self.player_steps = ctrl.Consequent(self.step_range, 'player_steps')

        # Generate fuzzy membership functions
        self.ball_distance['close'] = fuzz.trimf(self.ball_distance.universe, self.close)
        self.ball_distance['far'] = fuzz.trimf(self.ball_distance.universe, self.far)
        self.ball_distance['very_far'] = fuzz.trimf(self.ball_distance.universe, self.very_far)
        self.ball_distance['too_far'] = fuzz.trimf(self.ball_distance.universe, self.too_far)

        self.player_steps['little_step'] = fuzz.trimf(self.player_steps.universe, self.little_step)
        self.player_steps['mid_step'] = fuzz.trimf(self.player_steps.universe, self.mid_step)
        self.player_steps['big_step'] = fuzz.trimf(self.player_steps.universe, self.big_step)
        self.player_steps['extreme_step'] = fuzz.trimf(self.player_steps.universe, self.extreme_step)

    # Defines the rules
    def define_rules(self):
        # IF the ball is close to the player THEN take little steps towards the ball.
        rule0 = ctrl.Rule(self.ball_distance['close'], self.player_steps['little_step'])
        # IF the ball is far to the player THEN take mid steps towards the ball.
        rule1 = ctrl.Rule(self.ball_distance['far'], self.player_steps['mid_step'])
        # IF the ball is very far to the player THEN take big steps towards the ball.
        rule2 = ctrl.Rule(self.ball_distance['very_far'], self.player_steps['big_step'])
        # IF the ball is too far to the player THEN take extreme steps towards the ball.
        rule3 = ctrl.Rule(self.ball_distance['too_far'], self.player_steps['extreme_step'])

        self.rules = [rule0, rule1, rule2, rule3]

    # Computes on the basis of absolute distance between the ball and the player.
    def compute(self, input_ball_distance):
        self.control.input['ball_distance'] = input_ball_distance
        self.control.compute()

    # Outputs the amounts of steps as a crisp value.
    def output(self):
        return self.control.output['player_steps']

    # Plots membership functions.
    def plot_membership_functions(self):
        fig, (ax, ax1) = plt.subplots(nrows=2, figsize=(8, 9))

        ax.plot(self.distance_range, fuzz.trimf(self.ball_distance.universe, self.close), linewidth=1.5, label='close')
        ax.plot(self.distance_range, fuzz.trimf(self.ball_distance.universe, self.far), linewidth=1.5, label='far')
        ax.plot(self.distance_range, fuzz.trimf(self.ball_distance.universe, self.very_far), linewidth=1.5, label='very far')
        ax.plot(self.distance_range, fuzz.trimf(self.ball_distance.universe, self.too_far), linewidth=1.5, label='too far')

        ax.set_title('Ball Distance from Player')
        ax.legend()

        ax1.plot(self.step_range, fuzz.trimf(self.player_steps.universe, self.little_step), linewidth=1.5, label='little step')
        ax1.plot(self.step_range, fuzz.trimf(self.player_steps.universe, self.mid_step), linewidth=1.5, label='mid step')
        ax1.plot(self.step_range, fuzz.trimf(self.player_steps.universe, self.big_step), linewidth=1.5, label='big step')
        ax1.plot(self.step_range, fuzz.trimf(self.player_steps.universe, self.extreme_step), linewidth=1.5, label='extreme step')

        ax1.set_title('Player Move Steps')
        ax1.legend()

        plt.tight_layout()
        plt.show()

    # Plots defuzzification result.
    def plot_defuzzification(self, input_ball_distance):

        # Membership functions
        ball_distance_close = fuzz.trimf(self.ball_distance.universe, self.close)
        ball_distance_far = fuzz.trimf(self.ball_distance.universe, self.far)
        ball_distance_very_far = fuzz.trimf(self.ball_distance.universe, self.very_far)
        ball_distance_too_far = fuzz.trimf(self.ball_distance.universe, self.too_far)

        player_steps_little_step = fuzz.trimf(self.player_steps.universe, self.little_step)
        player_steps_mid_step = fuzz.trimf(self.player_steps.universe, self.mid_step)
        player_steps_big_step = fuzz.trimf(self.player_steps.universe, self.big_step)
        player_steps_extreme_step = fuzz.trimf(self.player_steps.universe, self.extreme_step)

        # Activation of Fuzzy membership functions
        ball_distance_is_close = fuzz.interp_membership(self.distance_range, ball_distance_close, input_ball_distance)
        ball_distance_is_far = fuzz.interp_membership(self.distance_range, ball_distance_far, input_ball_distance)
        ball_distance_is_very_far = fuzz.interp_membership(self.distance_range, ball_distance_very_far, input_ball_distance)
        ball_distance_is_too_far = fuzz.interp_membership(self.distance_range, ball_distance_too_far, input_ball_distance)

        # Apply rules.
        active_rule1 = ball_distance_is_close
        active_rule2 = ball_distance_is_far
        active_rule3 = ball_distance_is_very_far
        active_rule4 = ball_distance_is_too_far

        player_steps_activation_little_step = np.fmax(active_rule1, player_steps_little_step)
        player_steps_activation_mid_step = np.fmax(active_rule2, player_steps_mid_step)
        player_steps_activation_big_step = np.fmax(active_rule3, player_steps_big_step)
        player_steps_activation_extreme_step = np.fmax(active_rule4, player_steps_extreme_step)

        # Aggregate all four output membership functions together
        aggregated = np.fmax(player_steps_activation_little_step, 
            np.fmax(player_steps_activation_mid_step, 
                np.fmax(player_steps_activation_big_step, player_steps_activation_extreme_step)))

        # Calculate defuzzified result
        player_steps = fuzz.defuzz(self.step_range, aggregated, 'centroid')
        player_steps_activation = fuzz.interp_membership(self.step_range, aggregated, player_steps)

        # Visualize
        fig, ax0 = plt.subplots(figsize=(8, 3))
        player_steps0 = np.zeros_like(self.step_range)

        ax0.plot(self.step_range, player_steps_little_step, 'b', linewidth=0.5, linestyle='--', )
        ax0.plot(self.step_range, player_steps_mid_step, 'g', linewidth=0.5, linestyle='--')
        ax0.plot(self.step_range, player_steps_big_step, 'r', linewidth=0.5, linestyle='--')
        ax0.fill_between(self.step_range, player_steps0, aggregated, facecolor='Orange', alpha=0.7)
        ax0.plot([player_steps, player_steps], [0, player_steps_activation], 'k', linewidth=1.5, alpha=0.9)
        ax0.set_title('Aggregated membership and result (line)')

        # Turn off top/right axes
        for ax in (ax0,):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        plt.tight_layout()
        plt.show()
























