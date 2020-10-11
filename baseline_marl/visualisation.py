import torch as th
from stable_baselines3.common.logger import Video


def render_trajectory(env, model):
    obs = env.reset()
    rewards = []
    done = False
    screens = []
    while not done:
        actions, _ = model.predict(obs, deterministic=True)
        obs, reward, done, infos = env.step(actions)
        screen = env.render(mode='rgb_array')
        screens.append(screen.transpose(2, 0, 1))
        rewards.append(reward)

    return Video(th.ByteTensor([screens]), fps=40), rewards
