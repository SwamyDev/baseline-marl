from datetime import datetime

import gym

from stable_baselines3 import A2C
from stable_baselines3.common.cmd_util import make_atari_env
from stable_baselines3.common.vec_env import sync_envs_normalization, VecFrameStack, VecTransposeImage
from torch.utils.tensorboard import SummaryWriter

from baseline_marl.visualisation import render_trajectory
from stable_baselines3.common.callbacks import BaseCallback


class ReportTrajectoryCallback(BaseCallback):
    def __init__(self, eval_env, check_freq):
        super().__init__()
        self._eval_env = eval_env
        self._check_freq = check_freq

    def _on_step(self):
        if self.n_calls % self._check_freq == 0:
            sync_envs_normalization(self.training_env, self._eval_env)
            video, rewards = render_trajectory(self._eval_env, self.model)
            self.logger.record("trajectory/video", video)
            self.logger.record("trajectory/return", sum(rewards))
        return True


t_env = make_atari_env('BreakoutNoFrameskip-v4', n_envs=8)
t_env = VecFrameStack(t_env, n_stack=4)
e_env = make_atari_env('BreakoutNoFrameskip-v4')
e_env = VecFrameStack(e_env, n_stack=4)
e_env = VecTransposeImage(e_env)

current_time = datetime.now().strftime('%b%d_%H-%M-%S')
model = A2C('CnnPolicy', t_env, verbose=0, tensorboard_log=f"runs/{current_time}")
eval_callback = ReportTrajectoryCallback(e_env, 10000)
model.learn(total_timesteps=int(1e7), eval_env=e_env, eval_freq=100, callback=eval_callback)
