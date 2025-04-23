# type: ignore

from shutil import copytree
from PySide6 import QtCore, QtWidgets, QtSvgWidgets

from common.common_paths import (
    SIMULATION_CONFIG_BASE_FOLDER,
    OUTPUT_FOLDER,
    TEMPLATE_FOLDER,
    LOGO_PATH,
    get_simulation_config_folders,
)
from gui.asset_library_editor_main_widget import (
    AssetLibraryEditorMainWidget,
)
from gui.cloeseable_window_widget import CloseableWindowWidget
from bears_flight_simulation import (
    load_configs_and_run_simulation,
)


class FlightSimulationGUI(CloseableWindowWidget):
    current_selection: str | None
    asset_library_editor_main_widget: AssetLibraryEditorMainWidget | None

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self.current_selection = None
        self.asset_library_editor_main_widget = None

        self.layout = QtWidgets.QVBoxLayout(self)

        _spacer_top = QtWidgets.QSpacerItem(
            20,
            40,
            hData=QtWidgets.QSizePolicy.Policy.Preferred,
            vData=QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.layout.addSpacerItem(_spacer_top)

        self.horizontal_centering_widget = QtWidgets.QWidget()
        _horizontal_centering_layout = QtWidgets.QHBoxLayout()
        _horizontal_centering_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.layout.addWidget(self.horizontal_centering_widget)
        self.horizontal_centering_widget.setLayout(_horizontal_centering_layout)

        self.main_layout_widget = QtWidgets.QWidget()
        _main_layout = QtWidgets.QVBoxLayout()
        _main_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.main_layout_widget.setMaximumWidth(1024)
        _horizontal_centering_layout.addWidget(self.main_layout_widget)
        self.main_layout_widget.setLayout(_main_layout)

        self.logo_layout_widget = QtWidgets.QWidget()
        _logo_layout = QtWidgets.QHBoxLayout()
        _logo_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 32))
        _main_layout.addWidget(self.logo_layout_widget)
        self.logo_layout_widget.setLayout(_logo_layout)

        self.logo_widget = QtSvgWidgets.QSvgWidget(LOGO_PATH)
        self.logo_widget.setFixedSize(576, 158)
        _logo_layout.addWidget(self.logo_widget)

        self.library_editors_button = QtWidgets.QPushButton("Asset Library Editors")
        self.library_editors_button.clicked.connect(
            self._library_editors_button_pressed
        )
        _main_layout.addWidget(self.library_editors_button)

        self.selection_layout_widget = QtWidgets.QWidget()
        _selection_layout = QtWidgets.QHBoxLayout()
        _selection_layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        _main_layout.addWidget(self.selection_layout_widget)
        self.selection_layout_widget.setLayout(_selection_layout)

        self.simulation_selector_dropdown = QtWidgets.QComboBox()
        self.simulation_selector_dropdown.currentTextChanged.connect(
            self._simulation_selector_dropdown_changed
        )
        _selection_layout.addWidget(self.simulation_selector_dropdown)

        self.selection_edit_button = QtWidgets.QPushButton("Edit")
        self.selection_edit_button.clicked.connect(self._selection_edit_button_pressed)
        _selection_layout.addWidget(self.selection_edit_button)

        self.selection_new_button = QtWidgets.QPushButton("New")
        self.selection_new_button.clicked.connect(self._selection_new_button_pressed)
        _selection_layout.addWidget(self.selection_new_button)

        self.run_simulation_button = QtWidgets.QPushButton("Run Simulation")
        self.run_simulation_button.clicked.connect(self._run_simulation_button_pressed)
        _main_layout.addWidget(self.run_simulation_button)

        self.show_results_button = QtWidgets.QPushButton("Show Results")
        self.show_results_button.clicked.connect(self._show_results_button_pressed)
        _main_layout.addWidget(self.show_results_button)

        _spacer_bottom = QtWidgets.QSpacerItem(
            20,
            40,
            hData=QtWidgets.QSizePolicy.Policy.Preferred,
            vData=QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.layout.addSpacerItem(_spacer_bottom)

        # Actually generate content for the GUI elements
        self._refresh_selectable_simulations()

    def _library_editors_button_pressed(self):
        # Open asset library editor main window if not already open
        if (
            self.asset_library_editor_main_widget is None
            or self.asset_library_editor_main_widget not in self._children_to_close
        ):
            self.asset_library_editor_main_widget = AssetLibraryEditorMainWidget()
            self.add_child_to_close(self.asset_library_editor_main_widget)
            self.asset_library_editor_main_widget.resize(640, 360)
            self.asset_library_editor_main_widget.show()

    def _simulation_selector_dropdown_changed(self, new_text):
        self.current_selection = new_text

    def _selection_edit_button_pressed(self):
        # TODO Launch config editor for the currently selected simulation
        pass

    def _selection_new_button_pressed(self):
        # Ask for name of new simulation from user
        (new_simulation_name, dialog_accepted) = QtWidgets.QInputDialog.getText(
            self,
            "New Simulation",
            "Enter name for new simulation (please DO NOT use special characters like '/'):",
        )

        # Abort if name is empty or dialog not accepted
        if not dialog_accepted or new_simulation_name == "":
            return

        # Create folder and copy template for new simulation
        new_simulation_path = SIMULATION_CONFIG_BASE_FOLDER + "/" + new_simulation_name
        copytree(TEMPLATE_FOLDER, new_simulation_path, dirs_exist_ok=False)

        self._refresh_selectable_simulations()

    def _run_simulation_button_pressed(self):
        load_configs_and_run_simulation(
            config_folder=SIMULATION_CONFIG_BASE_FOLDER + "/" + self.current_selection,
            output_folder=OUTPUT_FOLDER,
        )

    def _show_results_button_pressed(self):
        pass

    def _refresh_selectable_simulations(self):
        old_selection = self.simulation_selector_dropdown.currentText()

        simulation_config_folders = get_simulation_config_folders()
        self.simulation_selector_dropdown.clear()
        self.simulation_selector_dropdown.addItems(simulation_config_folders)

        index_equal_to_old_selection = self.simulation_selector_dropdown.findText(
            old_selection
        )
        if index_equal_to_old_selection >= 0:
            self.simulation_selector_dropdown.setCurrentIndex(
                index_equal_to_old_selection
            )

        no_simulations_exist = (
            simulation_config_folders is None or len(simulation_config_folders) == 0
        )
        self.run_simulation_button.setDisabled(no_simulations_exist)
        self.selection_edit_button.setDisabled(no_simulations_exist)
