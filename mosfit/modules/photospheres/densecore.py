from math import pi

import numexpr as ne
import numpy as np
from astropy import constants as c

from mosfit.constants import DAY_CGS, FOUR_PI, KM_CGS, M_SUN_CGS
from mosfit.modules.photospheres.photosphere import photosphere

CLASS_NAME = 'densecore'


class densecore(photosphere):
    """Expanding/receding photosphere with a dense core + low-mass power-law
    envelope
    """

    STEF_CONST = (4.0 * pi * c.sigma_sb).cgs.value
    PL_ENV = 10.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process(self, **kwargs):
        self._t_explosion = kwargs['texplosion']
        self._times = kwargs['times']
        self._luminosities = kwargs['luminosities']
        self._v_ejecta = kwargs['vejecta']
        self._m_ejecta = kwargs['mejecta']
        self._kappa = kwargs['kappa']
        slope = self.PL_ENV
        rphot = []
        Tphot = []
        temperature_last = 2.e4
        for li, lum in enumerate(self._luminosities):

            # Radius is determined via expansion
            radius = self._v_ejecta * KM_CGS * (
                self._times[li] - self._t_explosion) * DAY_CGS

            # Compute density in core
            rho_core = (3.0 * self._m_ejecta * M_SUN_CGS /
                        (4.0 * pi * radius**3))

            tau_core = self._kappa * rho_core * radius

            # Attach power-law envelope of negligible mass
            tau_e = self._kappa * rho_core * radius / (slope - 1.0)

            # Find location of photosphere in envelope/core
            if tau_e > 0.667:
                radius_phot = (2.0 * (slope - 1.0) /
                               (3.0 * self._kappa * rho_core * radius
                                **slope))**(1.0 / (1.0 - slope))
            else:
                radius_phot = slope * radius / (slope - 1.0) - 2.0 / (
                    3.0 * self._kappa * rho_core)

            # Compute temperature
            # Prevent weird behaviour as R_phot -> 0
            if tau_core > 1.0:
                temperature_phot = (lum / (radius_phot**2 *
                                self.STEF_CONST))**0.25
            else:
                temperature_phot = temperature_last
                radius_phot = (lum / (temperature_phot**4 *
                                self.STEF_CONST))**0.5

            temperature_last = temperature_phot

            rphot.append(radius_phot)

            Tphot.append(temperature_phot)


        return {'radiusphot': rphot, 'temperaturephot': Tphot}