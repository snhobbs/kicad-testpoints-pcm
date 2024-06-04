import os
import csv
import wx
import wx.aui
import wx.lib.buttons as buttons
from pathlib import Path
import pcbnew


class Meta:
    toolname="kicadtestpoints"
    title="Test Point Report"
    body="Choose test points by setting the desired pads 'Fabrication Property' to 'Test Point Pad'. The output is formated as a JigsApp test point report."
    about_text="This plugin generates TheJigsApp style test points reports. Test more, worry less."
    short_description="TheJigsApp KiCAD Test Point Report"
    frame_title="TheJigsApp KiCAD Test Point Report"
    website="https://www.thejigsapp.com"
    version='0.1.7'


def get_pad_side(p: pcbnew.PAD):
    """
    As footprints can be on the top or bottom and the pad position is relative
    to the footprint we need to use both the footprint and the pad position to get
    the correct side. As the top layer/side is 0 then we can do the following.
    """
    fp: pcbnew.FOOTPRINT = p.GetParentFootprint()
    return "BOTTOM" if (fp.GetSide() - p.GetLayer()) else "TOP"


# Table of fields and how to get them
_fields = {
    'source ref des': lambda p: p.GetParentFootprint().GetReferenceAsString(),
    'source pad': lambda p: p.GetNumber(),
    'net': lambda p: p.GetShortNetname(),
    'net class': lambda p: p.GetNetClassName(),
    'side': get_pad_side,
    'x': lambda p: pcbnew.ToMM(p.GetCenter())[0],
    'y': lambda p: pcbnew.ToMM(p.GetCenter())[1],
    'pad type': lambda p: "SMT" if (p.GetDrillSizeX() == 0 and p.GetDrillSizeY() == 0) else "THRU",
    'footprint side': lambda p: "BOTTOM" if p.GetParentFootprint().GetSide() else "TOP"
}


def write_csv(data: list[dict], filename: Path):
    fieldnames = data[0].keys()
    with filename.open('w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if fieldnames is not None:
            writer.writeheader()
        writer.writerows(data)


def build_test_point_report(board: pcbnew.BOARD) -> list[dict]:
    test_point_property = 4
    lines = []
    for p in board.GetPads():
        if p.GetProperty() != test_point_property:
            continue
        lines.append({
            key: value(p) for key, value in _fields.items()
        })
    return lines


class SuccessPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Static text for success message
        success_text = "Submission successful!"
        success_label = wx.StaticText(self, label=success_text)

        # Sizer for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(success_label, 0, wx.ALL, 5)
        self.SetSizer(sizer)


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Get current working directory
        dir_ = Path(os.getcwd())
        wd = Path(pcbnew.GetBoard().GetFileName()).absolute()
        if wd.exists():
            dir_ = wd.parent
        default_file_path = (dir_ / f"{Meta.toolname}-report.csv")

        # File output selector
        file_output_label = wx.StaticText(self, label="File Output:")
        self.file_output_selector = wx.FilePickerCtrl(self, style=wx.FLP_SAVE | wx.FLP_USE_TEXTCTRL, wildcard="CSV files (*.csv)|*.csv", path=default_file_path.as_posix())

        # Lorem Ipsum text
        lorem_text = wx.StaticText(self, label=Meta.body)

        # Buttons
        self.submit_button = buttons.GenButton(self, label="Submit")
        self.cancel_button = buttons.GenButton(self, label="Cancel")
        self.submit_button.SetBackgroundColour(wx.Colour(150, 225, 150))
        self.cancel_button.SetBackgroundColour(wx.Colour(225, 150, 150))
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        # Horizontal box sizer for buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.submit_button, 0, wx.ALL, 5)
        button_sizer.Add(self.cancel_button, 0, wx.ALL, 5)

        # Sizer for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(file_output_label, 0, wx.ALL, 5)
        sizer.Add(self.file_output_selector, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(lorem_text, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetMinSize((400, 200))  # Set a minimum width and height for the frame
        self.Layout()

    def on_submit(self, event):
        file_path = Path(self.file_output_selector.GetPath())
        if file_path:
            print("Submitting...")
            print("File Path:", file_path)

            board = pcbnew.GetBoard()

            data = build_test_point_report(board)
            write_csv(data, filename=file_path)
            self.GetTopLevelParent().EndModal(wx.ID_OK)
            # self.GetParent().ShowSuccessPanel()
        else:
            wx.MessageBox("Please select a file output path.", "Error", wx.OK | wx.ICON_ERROR)

    def on_cancel(self, event):
        print("Canceling...")
        self.GetTopLevelParent().EndModal(wx.ID_CANCEL)


class AboutPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        bold = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # Static text for about information
        message_text = wx.StaticText(self, label=Meta.about_text)
        version_text = wx.StaticText(self, label=f"Version: {Meta.version}")

        from wx.lib.agw.hyperlink import HyperLinkCtrl
        link = HyperLinkCtrl(self, wx.ID_ANY,
                             f"Visit {Meta.website} for more information.",
                             URL=Meta.website)

        link.SetColours(wx.BLUE, wx.BLUE, wx.BLUE)
        version_text.SetFont(bold)
        message_text.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(version_text, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(message_text, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(link, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)


class MyDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(400, 300))

        # Create a notebook with two tabs
        notebook = wx.Notebook(self)
        tab_panel = MyPanel(notebook)
        about_panel = AboutPanel(notebook)
        self.success_panel = SuccessPanel(notebook)

        notebook.AddPage(tab_panel, "Main")
        notebook.AddPage(about_panel, "About")

        # Sizer for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    def on_close(self, event):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def ShowSuccessPanel(self):
        self.GetSizer().GetChildren()[0].GetWindow().Destroy()
        self.GetSizer().Insert(0, self.success_panel)
        self.Layout()


class Plugin(pcbnew.ActionPlugin, object):

    def __init__(self):
        super().__init__()

        self.logger = None
        self.config_file = None

        self.name = Meta.title
        self.category = "Read PCB"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        icon_dir = os.path.dirname(__file__)
        self.icon_file_name = os.path.join(icon_dir, 'icon.png')
        self.description = Meta.body

    def Run(self):
        try:
            dlg = MyDialog(None, title=Meta.title)
            dlg.ShowModal()

        finally:
            dlg.Destroy()
