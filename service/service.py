import cantera as ct

from sdtoolbox.postshock import shk_calc
from sdtoolbox.reflections import reflected_fr
from sdtoolbox.thermo import soundspeed_fr
from sdtoolbox.config import ERRFT, ERRFV

from service.schemas.models import SWProblem, SWSolution


def initialize_species(input_file: str) -> dict:
    all_species = ct.Species.list_from_file(input_file)
    species_dict = {s.name: s for s in all_species}
    return species_dict


def create_solution(mixture, pressure, temperature) -> ct.Solution:
    specs = [component.split(':')[0] for component in mixture.split()]
    gas = ct.Solution(thermo='ideal-gas',
                      species=[species_dict[name] for name in specs])
    gas.TPX = temperature, pressure, mixture
    return gas


def init_states(mixture, pressure, temperature):
    """Creating states before ISW (gas_1), behind ISW (gas_2)
    and behind RSW (gas_5)."""
    gas_1 = create_solution(mixture, pressure, temperature)
    gas_2 = create_solution(mixture, pressure, temperature)
    gas_5 = create_solution(mixture, pressure, temperature)
    return gas_1, gas_2, gas_5


def sw_velocity_faster_than_sound(gas, u):
    a_fr = soundspeed_fr(gas)
    return u > a_fr


input_file = './thermobase/burcat.yaml'
species_dict = initialize_species(input_file)


def isw_rsw_parameters(data: SWProblem) -> SWSolution:
    mixture, u_isw, p_1, T_1 = data.mixture, data.u_isw, data.p_1, data.T_1
    gas_1, gas_2, gas_5 = init_states(mixture, p_1, T_1)
    mach_isw = u_isw/soundspeed_fr(gas_1)
    print('Initial state: ' + mixture + ', P1 = {:.0f} Pa,  T1 = {:.2f} K'.format(p_1, T_1))
    print('Incident shock speed UI = %.2f m/s, Mach %.2f' % (u_isw, mach_isw))
    # compute postshock gas state object gas_2
    gas_2 = shk_calc(u_isw, gas_2, gas_1, ERRFT, ERRFV)
    # compute reflected shock post-shock state gas_5
    p_5, u_rsw, gas_5 = reflected_fr(gas_1, gas_2, gas_5, u_isw)
    # Outputs:
    # p3 - pressure behind reflected wave
    # UR = Reflected shock speed relative to reflecting surface
    # gas3 = gas object with properties of postshock state
    p_2 = gas_2.P/ct.one_atm
    density_ratio_2 = gas_2.density/gas_1.density
    a_2 = soundspeed_fr(gas_2)
    n_2 = gas_2.P / (gas_2.T * ct.boltzmann)
    p_5 = gas_5.P/ct.one_atm
    density_ratio_5 = gas_5.density/gas_1.density
    a_5 = soundspeed_fr(gas_5)
    n_5 = gas_5.P / (gas_5.T * ct.boltzmann)
    u_flow = u_isw * (1 - 1/density_ratio_2)
    mach_rsw = (u_flow + u_rsw) / a_2
    print('Frozen Post-Incident-Shock State')
    print('T2 = %.2f K, P2 = %.2f bar' % (gas_2.T, p_2))
    print('a2 = %.2f m/s, r2/r1 = %.2f' % (a_2, density_ratio_2))
    print('Frozen Post-Reflected-Shock State')
    print('T5 = %.2f K,  P5 = %.2f atm' % (gas_5.T, p_5))
    print('a5 = %.2f m/s, r2/r1 = %.2f' % (a_5, density_ratio_5))
    print("Reflected Wave Speed = %.2f m/s, Mach %.2f" % (u_rsw, mach_rsw))
    result = SWSolution(u_isw=u_isw,
                        mach_isw=mach_isw,
                        T_2=gas_2.T,
                        p_2=p_2,
                        n_2=n_2,
                        a_2=a_2,
                        density_ratio_2=density_ratio_2,
                        u_rsw=u_rsw,
                        mach_rsw=mach_rsw,
                        T_5=gas_5.T,
                        p_5=p_5,
                        n_5=n_5,
                        a_5=a_5,
                        density_ratio_5=density_ratio_5)
    return result
