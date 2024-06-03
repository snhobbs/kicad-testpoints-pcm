import os
import logging
import pcbnew

#from .import dialog


class KicadTestPointsPlugin(pcbnew.ActionPlugin, object):
    def __init__(self):
        super().__init__()

        self.logger = None
        self.config_file = None

        self.name = "KiCAD TestPoints"
        self.category = "Modify PCB"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        icon_dir = os.path.dirname(__file__)
        self.icon_file_name = os.path.join(icon_dir, 'icon.png')
        self.description = "Create test point report"

        self.supportedVersions = ['7.','8.']
        self.kicad_build_version = pcbnew.GetBuildVersion()

    productionDir = "Production"

    def IsSupported(self):
        for v in self.supportedVersions:
            if self.kicad_build_version.startswith(v):
                return True
        return False

    def Run(self):
        # Construct the config_file path from the board name
        board = pcbnew.GetBoard()
        panelOutputPath = os.path.split(board.GetFileName())[0] # Get the file path head
        if not os.path.exists(panelOutputPath):
            os.mkdir(panelOutputPath)

        self.logger = logging.getLogger('kicadtestpoints_logger')
        f_handler = logging.FileHandler(logFile)
        f_handler.setLevel(logging.DEBUG) # Log everything
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        self.logger.addHandler(f_handler)
        self.logger.removeHandler(f_handler)

        #app = dialog.MyApp()
        #app.MainLoop()
