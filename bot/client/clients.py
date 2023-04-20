from bot.schemas.models import UserData, SWProblem, SWSolution
from bot.ui.languages import Localization

from service.service import isw_rsw_parameters


class LocalClient():
    def __init__(self) -> None:
        self.base: dict[int, UserData] = {}

    def is_registered(self, user_id):
        return user_id in self.base

    def get_params(self, user_id) -> UserData:
        if user_id not in self.base:
            self.base[user_id] = UserData(language=Localization.RU,
                                          mixture="H2:10 O2:10 AR:80",
                                          T_1=297,
                                          length=94)
        return self.base[user_id]

    def update_mixture(self, user_id, mixture):
        self.base[user_id].mixture = mixture

    def update_temperature(self, user_id, temperature):
        self.base[user_id].T_1 = temperature

    def update_length(self, user_id, length):
        self.base[user_id].length = length

    def solve(self, data: SWProblem) -> SWSolution:
        return isw_rsw_parameters(data)


client = LocalClient()
