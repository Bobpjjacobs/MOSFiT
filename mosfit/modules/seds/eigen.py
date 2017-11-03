"""Definitions for the `Eigen` class."""

import astropy.units as u
from mosfit.modules.seds.sed import SED


# Important: Only define one ``Module`` class per file.


class Eigen(SED):
    """Adds extinction to SED from both host galaxy and MW."""

    ANG_CGS = u.Angstrom.cgs.scale

    def __init__(self, **kwargs):
        """Initialize module."""
        super(Eigen, self).__init__(**kwargs)
        # Load spectra here.

    def process(self, **kwargs):
        """Process module."""
        kwargs = self.prepare_input(self.key('luminosities'), **kwargs)
        self.preprocess(**kwargs)
        self._seds = kwargs[self.key('seds')]

        # Draw spectrum based on PCA.

        return {
            self.key('seds'): self._seds
        }

    def preprocess(self, **kwargs):
        """Preprocess module."""
        if self._preprocessed:
            return
        # PCA done here.
        self._preprocessed = True
