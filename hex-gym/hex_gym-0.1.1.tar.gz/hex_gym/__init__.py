from gym.envs.registration import register

register(
    id='hexpod-v0',
    entry_point='hex_gym.envs:HexSimulator',
)