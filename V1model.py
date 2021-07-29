import numpy as np
from V1cells import *


class V1model:
    """
    Classical V1 model
    """

    def __init__(
        self,
        inputs_res,
        inputs_fov,
        cell_density,
        n_ori,
        n_phase,
        sf,
        sigma_x_values=[1],
        sigma_y_values=[1],
        with_complex_cells=True,
    ):
        """init function of a classical V1 model

        Args:
            inputs_res (int, int): dimension of the inputs and of the cells filters in x and y dimension
            inputs_fov (float, float): field of view in degree of visual field covered by the input
            cell_density (float): number of cells per degree of visual field
            n_ori (int): number of equidistant orientations of cell's Gabor filters
            n_phase (int): number of equidistant phases of cell's Gabor filters
            sf (list of floats): spatial frequencies values of cell's Gabor filters
            sigma_x_values (list of floats, optional): standard deviation of the Gaussian envelope of the 
                                                    cell's Gabor filters in the orthogonal direction. Defaults to [1].
            sigma_y_values (list of floats, optional): standard deviation of the Gaussian envelope of the 
                                                    cell's Gabor filters in the parallel direction. Defaults to [1].
            with_complex_cells (bool, optional): True to have complex cells (on top of simples). Defaults to True.
        """
        self.inputs_res = inputs_res
        self.inputs_fov = inputs_fov
        self.xlim = (-inputs_fov[0] / 2, inputs_fov[0] / 2)
        self.ylim = (-inputs_fov[1] / 2, inputs_fov[1] / 2)
        self.cell_density = cell_density
        self.n_ori = n_ori
        self.sf = sf
        self.n_phase = n_phase
        self.sigma_x_values = sigma_x_values
        self.sigma_y_values = sigma_y_values
        self.positions = self._get_positions()
        self.orientations = self._get_orientations()
        self.phases = self._get_phases()
        self.with_complex_cells = with_complex_cells
        self.simple_cells = self.create_simple_cells()
        if self.with_complex_cells == True:
            self.complex_cells = self.create_complex_cells()
        else:
            self.complex_cells = []
        self.cells = self.simple_cells + self.complex_cells

    # TODO can improve this
    def _get_positions(self):
        pos_x = (
            np.linspace(-0.5, 0.5, int(self.cell_density * self.inputs_fov[0]))
            * self.inputs_fov[0]
        )
        pos_y = (
            np.linspace(-0.5, 0.5, int(self.cell_density * self.inputs_fov[0]))
            * self.inputs_fov[1]
        )
        positions = [(x, y) for x in pos_x for y in pos_y]
        return positions

    def _get_orientations(self):
        orientations = np.linspace(0, np.pi, self.n_ori + 1)[:-1]
        return orientations

    def _get_phases(self):
        phases = np.linspace(0, 2 * np.pi, self.n_phase + 1)[:-1]
        return phases

    def create_simple_cells(self):
        """creates the models simple cells according to the initialization args

        Returns:
            [list]: list containing simple cells objects 
        """
        return [
            simple_cell(
                self.inputs_res,
                self.xlim,
                self.ylim,
                pos,
                theta,
                sf,
                phase,
                sigma_x,
                sigma_y,
            )
            for pos in self.positions
            for theta in self.orientations
            for sf in self.sf
            for phase in self.phases
            for sigma_x in self.sigma_x_values
            for sigma_y in self.sigma_y_values
        ]

    def create_complex_cells(self):
        """creates the models complex cells according to the initialization args

        Returns:
            [list]: list containing complex cells objects 
        """
        return [
            complex_cell(
                self.inputs_res,
                self.xlim,
                self.ylim,
                pos,
                theta,
                sf,
                phase,
                sigma_x,
                sigma_y,
            )
            for pos in self.positions
            for theta in self.orientations
            for sf in self.sf
            for phase in self.phases
            for sigma_x in self.sigma_x_values
            for sigma_y in self.sigma_y_values
        ]

    def get_responses(self, stim):
        """returns cells responses to a given stimulus

        Args:
            stim ([2d numpy array]): stimulus

        Returns:
            [list of floats]: list containing cell's responses
        """
        return [cell.get_response(stim) for cell in self.cells]

    def get_simple_cell_filters(self):
        """function to get all the filters of simple cells as a 3d numpy array 

        Returns:
            [3d numpy array]: cell's filters
        """
        simple_cells_filters = np.array([cell.filter for cell in self.simple_cells])
        return simple_cells_filters

    def get_complex_cell_filters(self):
        """function to get the filters and the 180 deg phase shifted filters of complex cells

        Returns:
            [list]: list containing 2 3d numpy arrays representing the cells
                    filters and phase shifted filters
        """
        complex_cells_f1s = np.array([cell.f1 for cell in self.complex_cells])
        complex_cells_f2s = np.array([cell.f2 for cell in self.complex_cells])
        return complex_cells_f1s, complex_cells_f2s
