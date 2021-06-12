from abc import ABC, abstractmethod
from collections import namedtuple

from staking_bot_template.contracts import Proposal


TimePeriod = namedtuple('TimePeriod', ['start', 'end'])


class Predictor(ABC):
    @abstractmethod
    def get_proposals_for(self, time_period: TimePeriod) -> list[Proposal]:
        pass
