import logging
import os
import sys
from pathlib import Path
import wx
import wx.aui
from wx.lib import buttons
import pcbnew
import dataclasses

path_ = Path(__file__).parent.absolute()
sys.path.append(str(path_))

from kicad_testpoints_ import (
    get_pads_by_property,
    build_test_point_report,
    write_csv,
    Settings,
)

from _version import __version__

_log = logging.getLogger("kicad_testpoints-pcm")
_log.setLevel(logging.DEBUG)

_board = None
_frame_size = (800, 600)
_frame_size_min = (300, 200)

def set_board(board):
    """
    Sets the board global.
    """
    global _board
    _board = board

def get_board():
    """
    Use instead of pcbnew.GetBoard to allow
    command line use.
    """
    return _board

@dataclasses.dataclass
class Meta:
    """
    Information about package
    """
    toolname : str = "kicadtestpoints"
    title : str = "Test Point Report"
    body : str = ("Choose test points by setting the desired pads 'Fabrication Property' to \
'Test Point Pad'. The output default is in the JigsApp test point report style. \
Coordinates are Cartesian with x increasing to the right and y increasing upwards. \
For correct agreement with generated gerbers and the component placement, ensure the \
origin used is consistent.")
    about_text : str = "This plugin generates TheJigsApp style test points reports. Test more, worry less."
    short_description : str = "TheJigsApp KiCAD Test Point Report"
    frame_title : str = "TheJigsApp KiCAD Test Point Report"
    website : str = "https://www.thejigsapp.com"
    gitlink : str = "https://github.com/snhobbs/kicad-testpoints-pcm"
    version : str = __version__
    category : str = "Read PCB"
    icon_dir : Path =  Path(__file__).parent
    icon_file_path : Path = icon_dir / "icon-24x24.png"
    # assert icon_file_path.exists()


def setattr_keywords(obj, name, value):
    return setattr(obj, name, value)


class MyPanel(wx.Panel):
    def __init__(self, parent):
        _log.debug("MyPanel.__init__")
        super().__init__(parent)
        self.settings = Settings()

        # Get current working directory
        dir_ = Path(os.getcwd())
        if pcbnew.GetBoard():
            set_board(pcbnew.GetBoard())

        if get_board():
            wd = Path(get_board().GetFileName()).absolute()
            if wd.exists():
                dir_ = wd.parent
        default_file_path = dir_ / f"{Meta.toolname}-report.csv"

        # File output selector
        file_output_label = wx.StaticText(self, label="File Output:")
        self.file_output_selector = wx.FilePickerCtrl(
            self,
            style=wx.FLP_SAVE | wx.FLP_USE_TEXTCTRL,
            wildcard="CSV files (*.csv)|*.csv",
            path=default_file_path.as_posix(),
        )
        self.file_output_selector.SetPath(default_file_path.as_posix())

        lorem_text = wx.StaticText(self, label=Meta.body)

        # Buttons
        self.submit_button = buttons.GenButton(self, label="Submit")
        self.cancel_button = buttons.GenButton(self, label="Cancel")
        self.submit_button.SetBackgroundColour(wx.Colour(100, 225, 100))
        self.cancel_button.SetBackgroundColour(wx.Colour(225, 100, 100))
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        # Horizontal box sizer for buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.submit_button, 0, wx.ALL | wx.EXPAND, 5)
        button_sizer.Add(self.cancel_button, 0, wx.ALL, 5)

        # Origin selection
        self.use_aux_origin_cb = wx.CheckBox(self, label="Use drill/place file origin")
        self.use_aux_origin_cb.SetValue(True)
        self.settings.use_aux_origin = self.use_aux_origin_cb.GetValue()

        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_toggle)

        # Sizer for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.use_aux_origin_cb, 0, wx.ALL, 10)

        sizer.Add(file_output_label, 0, wx.ALL, 5)
        sizer.Add(self.file_output_selector, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(lorem_text, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(sizer)

    def on_checkbox_toggle(self, event):
        checkbox = event.GetEventObject()
        self.settings.use_aux_origin = checkbox.GetValue()

    def on_submit(self, _):
        file_path = Path(self.file_output_selector.GetPath())
        if not file_path:
            wx.MessageBox(
                "Please select a file output path.", "Error", wx.OK | wx.ICON_ERROR
            )
            return

        print("Submitting...")
        print("File Path:", file_path)

        board = get_board()
        pads = get_pads_by_property(board)
        data = build_test_point_report(board, pads=pads, settings=self.settings)
        if not data:
            wx.MessageBox(
                "No test point pads found, have you set any?",
                "Error",
                wx.OK | wx.ICON_ERROR,
            )
            return

        nets = set(board.GetNetsByName())
        tp_nets = set([pt["net"] for pt in data])

        write_csv(data, filename=file_path)

        wx.MessageBox(
            "Coverage: %d / %d nets\n\nSaved to: %s"%(len(tp_nets), len(nets), file_path),
            "Success",
            wx.OK,
        )

        self.GetTopLevelParent().EndModal(wx.ID_OK)
        return

    def on_cancel(self, _):
        print("Canceling...")
        self.GetTopLevelParent().EndModal(wx.ID_CANCEL)


class AboutPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        font = wx.Font(
            12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        bold = wx.Font(
            10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Static text for about information
        version_text = wx.StaticText(self, label=f"Version: {Meta.version}")
        version_text.SetFont(bold)
        sizer.Add(version_text, 1, wx.EXPAND | wx.ALL, 5)

        message_text = wx.StaticText(self, label=Meta.about_text)
        message_text.SetFont(font)
        sizer.Add(message_text, 1, wx.EXPAND | wx.ALL, 5)

        body_text = wx.StaticText(self, label=Meta.body)
        body_text.SetFont(font)
        sizer.Add(body_text, 5, wx.EXPAND | wx.ALL, 5)

        from wx.lib.agw.hyperlink import HyperLinkCtrl
        link_sizer = wx.BoxSizer(wx.HORIZONTAL)

        pre_link_text = wx.StaticText(self, label="Brought to you by TheJigsApp: ")
        pre_link_text.SetFont(font)
        link_sizer.Add(pre_link_text, 0, wx.EXPAND, 0)

        link = HyperLinkCtrl(self, wx.ID_ANY, f"{Meta.website}", URL=Meta.website)
        link.SetFont(font)
        link.SetColours(wx.BLUE, wx.BLUE, wx.BLUE)
        link_sizer.Add(link, 0, wx.EXPAND, 0)

        sizer.Add(link_sizer, 1, wx.EXPAND | wx.ALL, 5)

        gh_link_sizer = wx.BoxSizer(wx.HORIZONTAL)

        gh_pre_link_text = wx.StaticText(self, label="Git Repo: ")
        gh_pre_link_text.SetFont(font)
        gh_link_sizer.Add(gh_pre_link_text, 0, wx.EXPAND, 0)

        gh_link = HyperLinkCtrl(self, wx.ID_ANY, f"{Meta.gitlink}", URL=Meta.gitlink)
        gh_link.SetFont(font)
        gh_link.SetColours(wx.BLUE, wx.BLUE, wx.BLUE)
        gh_link_sizer.Add(gh_link, 0, wx.EXPAND, 0)

        sizer.Add(gh_link_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)


class MyDialog(wx.Dialog):
    """
    Top level GUI view
    """
    def __init__(self, parent, title):
        super().__init__(
            parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )

        # Sizer for layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create a notebook with two tabs
        notebook = wx.Notebook(self)
        tab_panel = MyPanel(notebook)
        about_panel = AboutPanel(notebook)

        notebook.AddPage(tab_panel, "Main")
        notebook.AddPage(about_panel, "About")

        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)
        self.SetMinSize(_frame_size_min)
        self.SetSize(_frame_size)

    def on_close(self, event):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def on_maximize(self, _):
        self.fit_to_screen()

    def on_size(self, _):
        if self.IsMaximized():
            self.fit_to_screen()

    def fit_to_screen(self):
        screen_width, screen_height = wx.DisplaySize()
        self.SetSize(wx.Size(screen_width, screen_height))


def get_gui_frame(name: str = "PcbFrame"):
    pcb_frame = None

    try:
        pcb_frame = [
            x for x in wx.GetTopLevelWindows() if x.GetName() == name
        ][0]
    except IndexError:
        pass
    return pcb_frame


class Plugin(pcbnew.ActionPlugin):
    def __init__(self):
        super().__init__()

        _log.debug("Loading kicad_testpoints")

        self.logger = _log
        self.config_file = None

        self.name = Meta.title
        self.category = Meta.category
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.description = Meta.body
        self.icon_file_name = str(Meta.icon_file_path)

    def defaults(self):
        pass

    def Run(self):
        dlg = MyDialog(get_gui_frame(name="PcbFrame"), title=Meta.title)
        try:
            dlg.ShowModal()

        except Exception as e:
            _log.error(e)
            raise
        finally:
            _log.debug("Destroy Dialog")
            dlg.Destroy()


if __name__ == "__main__":
    logging.basicConfig()
    _log.setLevel(logging.DEBUG)
    if len(sys.argv) > 1:
        set_board(pcbnew.LoadBoard(sys.argv[1]))
    app = wx.App()
    p = Plugin()
    p.Run()
