""" Handle the main application window """
# $Id: MainWindowApp.py,v 1.3 2004/04/12 04:46:16 prof Exp $
import Tkinter as Tk
import gettext
import logging
import tkFont

import ViewLog
import common as com
import entStaging

_ = gettext.gettext

class MainWindowApp:

    def __init__(self, log):
        """ Remember cumulative log, get logger """
        self.log    = log
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        """ Create and run GUI """
        self.root = root = Tk.Tk()
        self.root.grid()

        root.title(_('Stage Utility'))

        # SET UP CONTROLS

        # Create Left Side navigation pane
        root.NavigationPane = Tk.Frame()
        root.StageImagePane = Tk.Frame()

        root.CanStage = Tk.Canvas(root.StageImagePane, width=500, height=500)

        # Create Labels
        root.labDimensions = Tk.Label(root.NavigationPane, text="Dimensions:")
        root.labWidth = Tk.Label(root.NavigationPane, text="Width: ")
        root.labDepth = Tk.Label(root.NavigationPane, text="Depth: ")
        root.tfWidth = Tk.Entry(root.NavigationPane)
        root.tfWidth.insert(0, "8")
        root.tfDepth = Tk.Entry(root.NavigationPane)
        root.tfDepth.insert(0, "8")
        root.butCreateStage = Tk.Button(root.NavigationPane, text="Create!", command=self.onCreateAction)

        root.labDecks = Tk.Label(root.NavigationPane, text="Decks: ")
        root.valDecks = Tk.Label(root.NavigationPane, text="0")
        root.labFrames = Tk.Label(root.NavigationPane, text="Frames: ")
        root.valFrames = Tk.Label(root.NavigationPane, text="0")
        root.labBraces = Tk.Label(root.NavigationPane, text="Braces:")
        root.labDiagonalBraces = Tk.Label(root.NavigationPane, text="Diagonal: ")
        root.valDiagonalBraces = Tk.Label(root.NavigationPane, text="0")
        root.labHorizontalBraces = Tk.Label(root.NavigationPane, text="Horizontal: ")
        root.valHorizontalBraces = Tk.Label(root.NavigationPane, text="0")
        root.labTopHats = Tk.Label(root.NavigationPane, text="TopHats: ")
        root.labThSingle = Tk.Label(root.NavigationPane, text="Single: ")
        root.valThSingle = Tk.Label(root.NavigationPane, text="0")
        root.labThDouble = Tk.Label(root.NavigationPane, text="Double: ")
        root.valThDouble = Tk.Label(root.NavigationPane, text="0")
        root.labThQuad = Tk.Label(root.NavigationPane, text="Quad: ")
        root.valThQuad = Tk.Label(root.NavigationPane, text="0")

        # PUT CONTROL IN GRID
        root.NavigationPane.grid(column=0, row=0, sticky='NSW')
        root.StageImagePane.grid(column=1, row=0, sticky='NSEW')

        root.labDimensions.grid(column=com.col, row=com.row, sticky='W')
        root.labWidth.grid(column=com.col, row=com.increment_row(), sticky='E')
        root.tfWidth.grid(column=1, row=com.row, sticky='WE')
        root.labDepth.grid(column=0, row=com.increment_row(), sticky='E')
        root.tfDepth.grid(column=1, row=com.row, sticky='WE')
        root.butCreateStage.grid(column=1, row=com.increment_row(), sticky='E')

        root.labDecks.grid(column=0, row=com.increment_row(), sticky='E')
        root.valDecks.grid(column=1, row=com.row, sticky='W')
        root.labFrames.grid(column=0, row=com.increment_row(), sticky='E')
        root.valFrames.grid(column=1, row=com.row, sticky='W')
        root.labBraces.grid(column=0, row=com.increment_row(), sticky='W')
        root.labDiagonalBraces.grid(column=0, row=com.increment_row(), sticky='E')
        root.valDiagonalBraces.grid(column=1, row=com.row, sticky='W')
        root.labHorizontalBraces.grid(column=0, row=com.increment_row(), sticky='E')
        root.valHorizontalBraces.grid(column=1, row=com.row, sticky='W')
        root.labTopHats.grid(column=0, row=com.increment_row(), sticky='W')
        root.labThSingle.grid(column=0, row=com.increment_row(), sticky='E')
        root.valThSingle.grid(column=1, row=com.row, sticky='W')
        root.labThDouble.grid(column=0, row=com.increment_row(), sticky='E')
        root.valThDouble.grid(column=1, row=com.row, sticky='W')
        root.labThQuad.grid(column=0, row=com.increment_row(), sticky='E')
        root.valThQuad.grid(column=1, row=com.row, sticky='W')

        root.CanStage.grid(column=0, row=0, columnspan=8, rowspan=8)


        root.mainloop()

    def onExit(self):
        """ Process 'Exit' command """
        self.root.quit()

    def onViewLog(self):
        """ Process 'View Log' command """
        ViewLog.ViewLog(self.root, self.log)

    def onCreateAction(self):
        """ Process 'Create Stage' command """
        self.logger.info(_('Creating stage...'))

        # Get the values from the dimension fields
        iWidth = int(self.root.tfWidth.get())
        iDepth = int(self.root.tfDepth.get())
        aStage = entStaging.create_stage(self.log, width=iWidth, depth=iDepth)
        self.PopulateFields(aStage)
        self.PopulateStageImage(aStage)
        aStage.print_me()

    def PopulateFields(self, aStage):
        """ Populate all of the information in the Navigation Pane """
        self.logger.info(_('Populating Information...'))

        iDecks = aStage.count_decks()

        dictFrameThings = aStage.count_frames()
        iFrames = dictFrameThings["frame"]
        iDiagBraces = dictFrameThings["diag-brace"]
        iHorizBraces = dictFrameThings["horiz-brace"]

        dictTopHats = aStage.count_tophats()
        iSingle = dictTopHats["single"]
        iDouble = dictTopHats["double"]
        iQuad = dictTopHats["quad"]

        self.root.valDecks.config(text=str(iDecks))
        self.root.valFrames.config(text=str(iFrames))
        self.root.valDiagonalBraces.config(text=str(iDiagBraces))
        self.root.valHorizontalBraces.config(text=str(iHorizBraces))

        self.root.valThSingle.config(text=str(iSingle))
        self.root.valThDouble.config(text=str(iDouble))
        self.root.valThQuad.config(text=str(iQuad))

    def PopulateStageImage(self, aStage):
        """ create an image of the stage """
        multiplier = 10
        colStageFrame = "white"
        colStageCenter = "gray"
        root = self.root
        root.CanStage.delete('all')


        x = 1
        y = 1

        for row in aStage.DeckRows:

            # Set the x postion
            x = 1
            x += row.Offset

            for deck in row.Decks:

                width = 4
                depth = 4

                # Figure out if this is a child
                if deck.isWidthChild or deck.isDepthChild:
                    # it is a child
                    # So we can skip this one after advancing x position
                    pass
                else:
                    # Find the width/depth of the deck
                    if deck.hasWidthChild:
                        width = 8
                    elif deck.hasDepthChild:
                        depth = 8

                    # Set rectangle coordinates
                    x1 = x * multiplier
                    y1 = y * multiplier
                    x2 = (x + width) * multiplier
                    y2 = (y + depth) * multiplier

                    root.CanStage.create_rectangle(x1, y1, x2, y2)

                # loop through each corner
                tophat_list = [0, 0, 0, 0]
                if deck.hasFrame:
                    th = deck.TopHats
                    if deck.FrameSide == "Top":
                        tophat_list = [th[0], th[1], 0, 0]
                    elif deck.FrameSide == "Right":
                        tophat_list = [0, th[0], th[1], 0]
                    elif deck.FrameSide == "Bottom":
                        tophat_list = [0, 0, th[0], th[1]]
                    elif deck.FrameSide == "Left":
                        tophat_list = [th[0], 0, 0, th[1]]

                for n1 in range(0, 4):
                    # 0 = NW
                    # 1 = NE
                    # 2 = SE
                    # 3 = SW

                    text = str(tophat_list[n1])
                    font = tkFont.Font(size=10)
                    w, h = font.measure(text), font.metrics('linespace')
                    x3 = 0
                    y3 = 0

                    if n1 == 0:
                        x3 = x1 + (w / 2)
                        y3 = y1 + (h / 2)
                    elif n1 == 1:
                        x3 = x2 - w
                        y3 = y1 + (h / 2)
                    elif n1 == 2:
                        x3 = x2 - w
                        y3 = y2 - (h / 2)
                    elif n1 == 3:
                        x3 = x1 + (w / 2)
                        y3 = y2 - (h / 2)

                    if text != "0":
                        root.CanStage.create_text(x3, y3, text=text, font=font)

                # Advance x position
                x += 4

            # Advance y position
            y += 4
