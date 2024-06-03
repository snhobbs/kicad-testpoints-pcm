#from .kicadtestpoints import plugin
import pcbnew
import re
import datetime


class text_by_date( pcbnew.ActionPlugin ):
    def defaults( self ):
        self.name = "Add date on PCB"
        self.category = "Modify PCB"
        self.description = "Automaticaly add date on an existing PCB"

    def Run( self ):
        pcb = pcbnew.GetBoard()
        for draw in pcb.m_Drawings:
            if draw.GetClass() == 'PTEXT':
                txt = re.sub( "\$date\$ [0-9]{4}-[0-9]{2}-[0-9]{2}",
                             "$date$", draw.GetText() )
            if txt == "$date$":
                draw.SetText( "$date$ %s"%datetime.date.today() )
