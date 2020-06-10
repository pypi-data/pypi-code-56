import torch.nn as nn
import torch.nn.functional as F
from torch.distributions.categorical import Categorical


class FC512Model(nn.Module):
    """
    Fully connected Actor-Critic model.
    """
    def __init__(self, obs_space, action_space):
        """
        Initialize the model.
        :param obs_space: (gym.spaces.Space) the observation space of the task
        :param action_space: (gym.spaces.Space) the action space of the task
        """
        super().__init__()

        self.recurrent = False  # required for using torch_ac package
        self.layer_width = 512

        # currently unneeded, as most values can be hardcoded, but used to try and maintain consistency of RL
        # implementation
        self.obs_space = obs_space  # must be a flat vector, something like Box(0, 255, shape=(128,))
        self.action_space = action_space

        self.preprocess_obss = None  # Default torch_ac pre-processing works for this model

        # Define state embedding
        self.state_emb = nn.Sequential(
            nn.Linear(obs_space.shape[0], self.layer_width),
            nn.ReLU(),
            nn.Linear(self.layer_width, self.layer_width),
            nn.ReLU()
        )

        # Define actor's model
        self.actor = nn.Sequential(
            nn.Linear(self.layer_width, self.layer_width),
            nn.ReLU(),
            nn.Linear(self.layer_width, action_space.n)
        )

        # Define critic's model
        self.critic = nn.Sequential(
            nn.Linear(self.layer_width, self.layer_width),
            nn.ReLU(),
            nn.Linear(self.layer_width, 1)
        )

    def forward(self, obs):
        obs = self.state_emb(obs.float())
        obs = obs.reshape(obs.shape[0], -1)
        x_act = self.actor(obs)
        dist = Categorical(logits=F.log_softmax(x_act, dim=1))
        x_crit = self.critic(obs)
        value = x_crit.squeeze(1)
        return dist, value

