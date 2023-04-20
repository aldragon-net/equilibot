from pydantic import BaseModel


class SWProblem(BaseModel):
    mixture: str
    p_1: float
    T_1: float
    u_isw: float


class SWSolution(BaseModel):
    u_isw: float
    mach_isw: float
    T_2: float
    p_2: float
    n_2: float
    a_2: float
    density_ratio_2: float
    u_rsw: float
    mach_rsw: float
    T_5: float
    p_5: float
    n_5: float
    a_5: float
    density_ratio_5: float


class RuptureProblem(BaseModel):
    mixture: str
    driver: str
    p_1: float
    T_1: float
    p_4: float
    T_4: float


class RuptureSolution(SWSolution):
    pass
