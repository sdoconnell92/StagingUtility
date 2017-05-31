import logging
import gettext
_ = gettext.gettext


class DeckUnit:
    def __init__(self):
        self.isWidthChild = False
        self.isDepthChild = False
        self.hasWidthChild = False
        self.hasDepthChild = False
        self.hasFrame = False
        self.FrameSide = ""
        self.TopHats = [0, 0]
        self.width = 4
        self.depth = 4
        self.height = 4
        self.ChildNorth = False
        self.ChildSouth = False
        self.ChildEast = False
        self.ChildWest = False
        self.ParentNorth = False
        self.ParentSouth = False
        self.ParentEast = False
        self.ParentWest = False

    def count_tophats(self):
        dict_tophats = {"single": 0, "double": 0, "quad": 0}
        for top_hat in self.TopHats:
            if top_hat == 0:
                pass
            elif top_hat == 1:
                dict_tophats["single"] += 1
            elif top_hat == 2:
                dict_tophats["double"] += 1
            elif top_hat == 4:
                dict_tophats["quad"] += 1
        return dict_tophats

    def count_frames(self):
        dict_frame_things = {"diag-brace": 0, "horiz-brace": 0, "frame": 0}
        if self.hasFrame:
            dict_frame_things["frame"] += 1
            dict_frame_things["diag-brace"] += 1
            dict_frame_things["horiz-brace"] += 1
        return dict_frame_things


class DeckRow:

    def __init__(self):
        self.Decks = []
        self.Offset = 0
        self.hasFrames = False

    def width(self):
        x1 = 0
        for deck in self.decks:
            x1 = x1 + deck.width
        return x1

    def add_decks(self, amount=1):
        for x in range(0,amount):
            deck1 = DeckUnit()
            self.Decks.append(deck1)

    def is_all_4x4(self):
        # returns true if all the decks in this row are 4x4s
        return_value = False
        for deck in self.Decks:
            if not deck.isWidthChild and not deck.isDepthChild:
                return_value = True
            else:
                return_value = False
        return return_value

    def count_tophats(self):
        dict_tophats = {"single": 0, "double": 0, "quad": 0}
        for deck in self.Decks:
            deck_tophats = {}
            deck_tophats = deck.count_tophats()

            dict_tophats["single"] += deck_tophats["single"]
            dict_tophats["double"] += deck_tophats["double"]
            dict_tophats["quad"] += deck_tophats["quad"]
        return dict_tophats

    def count_frames(self):
        dict_frame_things = {"diag-brace": 0, "horiz-brace": 0, "frame": 0}
        for deck in self.Decks:
            deck_frame_things = deck.count_frames()

            dict_frame_things["diag-brace"] += deck_frame_things["diag-brace"]
            dict_frame_things["horiz-brace"] += deck_frame_things["horiz-brace"]
            dict_frame_things["frame"] += deck_frame_things["frame"]
        return dict_frame_things

    def count_decks(self):
        running_count = 0
        for deck in self.Decks:
            if deck.hasDepthChild or deck.hasWidthChild or (not deck.isDepthChild and not deck.isWidthChild):
                running_count += 1
        return running_count

    def get_print_row(self):
        # Gets a row of decks to print for console
        POR = PrintObjectRow()
        for idx1, deck in enumerate(self.Decks):
            PrintObject = PrintBaseDeckObject()

            chr_thing = ""
            if deck.isWidthChild:
                chr_thing = "|"
                PrintObject.row1[0] = chr_thing
                PrintObject.row2[0] = chr_thing
                PrintObject.row3[0] = chr_thing
                PrintObject.row4[0] = chr_thing
                deck.ParentWest = True
            else:
                chr_thing = "{"
                if deck.hasFrame and deck.FrameSide == "Left":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                PrintObject.row2[0] = chr_thing
                PrintObject.row3[0] = chr_thing

                chr_thing = str(deck.TopHats[0])
                if deck.hasFrame and deck.FrameSide == "Left":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                    PrintObject.row1[0] = chr_thing

                chr_thing = str(deck.TopHats[1])
                if deck.hasFrame and deck.FrameSide == "Left":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                    PrintObject.row4[0] = chr_thing

            if deck.isDepthChild:
                chr_thing = "-"
                PrintObject.row1[1] = chr_thing
                PrintObject.row1[2] = chr_thing
                deck.ParentNorth
            else:
                chr_thing = "~"
                if deck.hasFrame and deck.FrameSide == "Top":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                PrintObject.row1[1] = chr_thing
                PrintObject.row1[2] = chr_thing

                chr_thing = str(deck.TopHats[0])
                if deck.hasFrame and deck.FrameSide == "Top":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                    PrintObject.row1[0] = chr_thing

                chr_thing = str(deck.TopHats[1])
                if deck.hasFrame and deck.FrameSide == "Top":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                    PrintObject.row1[3] = chr_thing

            if deck.hasWidthChild:
                chr_thing = "|"
                PrintObject.row1[3] = chr_thing
                PrintObject.row2[3] = chr_thing
                PrintObject.row3[3] = chr_thing
                PrintObject.row4[3] = chr_thing
                deck.ChildEast = True
            else:
                chr_thing = "}"
                if deck.hasFrame and deck.FrameSide == "Right":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                PrintObject.row2[3] = chr_thing
                PrintObject.row3[3] = chr_thing

                chr_thing = str(deck.TopHats[0])
                if deck.hasFrame and deck.FrameSide == "Right":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                    PrintObject.row1[3] = chr_thing

                chr_thing = str(deck.TopHats[1])
                if deck.hasFrame and deck.FrameSide == "Right":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                    PrintObject.row4[3] = chr_thing

            if deck.hasDepthChild:
                chr_thing = "-"
                PrintObject.row4[1] = chr_thing
                PrintObject.row4[2] = chr_thing
                deck.ChildSouth = True
            else:
                chr_thing = "~"
                if deck.hasFrame and deck.FrameSide == "Bottom":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                PrintObject.row4[1] = chr_thing
                PrintObject.row4[2] = chr_thing

                chr_thing = str(deck.TopHats[0])
                if deck.hasFrame and deck.FrameSide == "Bottom":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                    PrintObject.row4[0] = chr_thing

                chr_thing = str(deck.TopHats[1])
                if deck.hasFrame and deck.FrameSide == "Bottom":
                    chr_thing = bcolors.Frame + chr_thing + bcolors.ENDC
                    PrintObject.row4[3] = chr_thing


            POR.BaseObjects.append(PrintObject)
        return POR


class StagePlatform:

    def __init__(self, log):
        self.DeckRows = []
        self.log = log
        self.logger = logging.getLogger(self.__class__.__name__)

    def widest_point(self, in_number_of_decks=False):
        # Determines the widest point of the stage platform and returns it to user
        # This can be determined in number of decks wide
        # Or in feet wide

        the_widest_point = 0
        i1 = 0
        for row in self.DeckRows:
            running_width = 0
            if in_number_of_decks:
                running_width = len(row.Decks)
            else:
                i2 = 0
                for deck in row.Decks:
                    running_width = running_width + deck.width
                    i2 += 1
            if running_width > the_widest_point:
                the_widest_point = running_width
            i1 += 1
        return the_widest_point

    def count_tophats(self):
        dict_tophats = {"single": 0, "double": 0, "quad": 0}
        for row in self.DeckRows:
            row_tophats = {}
            row_tophats = row.count_tophats()

            dict_tophats["single"] += row_tophats["single"]
            dict_tophats["double"] += row_tophats["double"]
            dict_tophats["quad"] += row_tophats["quad"]
        return dict_tophats

    def count_frames(self):
        dict_frame_things = {"diag-brace": 0, "horiz-brace": 0, "frame": 0}
        for row in self.DeckRows:
            row_frame_things = row.count_frames()
            dict_frame_things["diag-brace"] += row_frame_things["diag-brace"]
            dict_frame_things["horiz-brace"] += row_frame_things["horiz-brace"]
            dict_frame_things["frame"] += row_frame_things["frame"]
        return dict_frame_things

    def count_decks(self):
        running_count = 0
        for row in self.DeckRows:
            running_count += row.count_decks()
        return running_count

    def deepest_point(self, in_number_of_decks=False):
        if in_number_of_decks:
            return len(self.DeckRows)
        else:
            running_depth = 0
            for row in self.DeckRows:
                running_depth += row.Decks[0].depth
            return running_depth

    def add_row(self, amount=1):
        for x in range(0, amount):
            row1 = DeckRow()
            self.DeckRows.append(row1)

    def get_print_stage(self):
        pos = PrintObjectStage()
        for idx1, row in enumerate(self.DeckRows):
            por = PrintObjectRow()
            por = row.get_print_row()
            pos.PrintRows.append(por)
        return pos

    def print_me(self):
        stage_printable = self.get_print_stage()
        print_string = stage_printable.print_me()
        self.logger.info(_(print_string))

    def frame_me(self):

        for idx1, row in enumerate(self.DeckRows):
            if idx1 % 2 == 0 or idx1 == len(self.DeckRows) - 1:
                row.hasFrames = True

            prior_row = None
            if idx1 - 1 > -1:
                prior_row = self.DeckRows[idx1 - 1]

            for idx2, deck in enumerate(row.Decks):

                prior_deck = None
                if deck.isWidthChild or deck.hasWidthChild:
                    if idx2 - 1 > -1:
                        prior_deck = row.Decks[idx2 - 1]

                elif deck.isDepthChild or deck.hasDepthChild:
                    if prior_row is not None:
                        if idx2 + row.Offset - prior_row.Offset < len(prior_row.Decks):
                            # there is a matching deck in the row above us
                            prior_deck = prior_row.Decks[idx2 + row.Offset - prior_row.Offset]

                if deck.isWidthChild:
                    if prior_deck.hasFrame:
                        if row.hasFrames:
                            # parent has a frame, so we need a frame
                            deck.hasFrame = True
                            deck.FrameSide = "Right"
                elif deck.hasWidthChild:
                    if prior_deck is not None:
                        # there is a deck to our left
                        if prior_deck.hasFrame and idx2 + 2 != len(row.Decks):
                            # the deck to our left has a frame
                            # we do not need one
                            pass
                        else:
                            # the deck to our left does not have a frame
                            # we need one
                            if row.hasFrames:
                                deck.hasFrame = True
                                deck.FrameSide = "Left"
                    else:
                        # there is now deck to the left
                        if row.hasFrames:
                            deck.hasFrame = True
                            deck.FrameSide = "Left"
                elif deck.isDepthChild:
                    if prior_deck.hasFrame:
                        # parent has frame so wee need frame
                        deck.hasFrame = True
                        deck.FrameSide = "Bottom"
                elif deck.hasDepthChild:
                    if prior_deck is not None:
                        # there is a deck above us
                        if prior_deck.hasFrame:
                            # the deck above us has a frame
                            if idx1 + 2 == len(self.DeckRows):
                                # we are on the last deck
                                # need frame
                                deck.hasFrame = True
                                deck.FrameSide = "Top"
                        else:
                            # the deck above has no frame
                            # we need our own
                            deck.hasFrame = True
                            deck.FrameSide = "Top"
                    else:
                        # there is no deck above us
                        # we need frame
                        deck.hasFrame = True
                        deck.FrameSide = "Top"

    def tophat_me(self):

        for idx1, row in enumerate(self.DeckRows):

            row_above = None
            row_below = None
            if idx1 - 1 > -1:
                row_above = self.DeckRows[idx1 - 1]
            if idx1 + 1 < len(self.DeckRows):
                row_below = self.DeckRows[idx1 + 1]

            for idx2, deck in enumerate(row.Decks):
                deck_left = None
                deck_right = None
                deck_above = None
                deck_below = None
                if idx2 - 1 > -1:
                    deck_left = row.Decks[idx2 - 1]
                if idx2 + 1 < len(row.Decks):
                    deck_right = row.Decks[idx2 + 1]
                if row_above is not None:
                    if idx2 + row.Offset - row_above.Offset < len(row_above.Decks):
                        deck_above = row_above.Decks[idx2 + row.Offset - row_above.Offset]
                if row_below is not None:
                    if idx2 + row.Offset - row_below.Offset < len(row_below.Decks):
                        deck_below = row_below.Decks[idx2 + row.Offset - row_below.Offset]

                # now we have all the decks around us
                if deck.hasFrame:
                    if deck.isWidthChild or deck.hasWidthChild:
                        if deck.FrameSide == "Left":
                            number_of_supportees = 0
                            if deck_above is not None:
                                if not deck_above.hasFrame:
                                    number_of_supportees += 1
                            if deck_left is not None:
                                if not deck_left.hasFrame:
                                    number_of_supportees += 1
                            if number_of_supportees == 2:
                                number_of_supportees = 4
                            else:
                                number_of_supportees += 1

                            deck.TopHats[0] = number_of_supportees

                            number_of_supportees = 0
                            if deck_below is not None:
                                if not deck_below.hasFrame:
                                    number_of_supportees += 1
                            if deck_left is not None:
                                if not deck_left.hasFrame:
                                    number_of_supportees += 1
                            if number_of_supportees == 2:
                                number_of_supportees = 4
                            else:
                                number_of_supportees += 1

                            deck.TopHats[1] = number_of_supportees

                        if deck.FrameSide == "Right":
                            number_of_supportees = 0
                            if deck_above is not None:
                                if not deck_above.hasFrame:
                                    number_of_supportees += 1
                            if deck_right is not None:
                                if not deck_right.hasFrame and not deck_right.isDepthChild and not deck_right.hasDepthChild:
                                    number_of_supportees += 1
                            if number_of_supportees == 2:
                                number_of_supportees = 4
                            else:
                                number_of_supportees += 1

                            deck.TopHats[0] = number_of_supportees

                            number_of_supportees = 0
                            if deck_below is not None:
                                if not deck_below.hasFrame:
                                    number_of_supportees += 1
                            if deck_right is not None:
                                if not deck_right.hasFrame and not deck_right.isDepthChild and not deck_right.hasDepthChild:
                                    number_of_supportees += 1
                            if number_of_supportees == 2:
                                number_of_supportees = 4
                            else:
                                number_of_supportees += 1

                            deck.TopHats[1] = number_of_supportees

                    if deck.isDepthChild or deck.hasDepthChild:
                        number_of_supportees = 0
                        if deck.FrameSide == "Top":
                            if deck_above is not None:
                                if not deck_above.hasFrame:
                                    number_of_supportees += 1
                            number_of_supportees += 1
                            deck.TopHats = [number_of_supportees, number_of_supportees]
                        if deck.FrameSide == "Bottom":
                            if deck_below is not None:
                                if not deck_below.hasFrame:
                                    number_of_supportees += 1
                            number_of_supportees += 1
                            deck.TopHats = [number_of_supportees, number_of_supportees]


class PrintBaseDeckObject:
    # Object for storing one deck print for console
    def __init__(self):
        self.row1 = ["{", "~", "~", "}"]
        self.row2 = ["{", "-", "-", "}"]
        self.row3 = ["{", "-", "-", "}"]
        self.row4 = ["{", "~", "~", "}"]


class PrintObjectRow:

    def __init__(self):
        self.BaseObjects = []


class PrintObjectStage:

    def __init__(self):
        self.PrintRows = []

    def print_me(self):
        return_string = ""
        for print_row in self.PrintRows:
            print_row1_text = ""
            print_row2_text = ""
            print_row3_text = ""
            print_row4_text = ""
            for print_deck in print_row.BaseObjects:
                print_row1_text += "  ".join(print_deck.row1)
                print_row2_text += "  ".join(print_deck.row2)
                print_row3_text += "  ".join(print_deck.row3)
                print_row4_text += "  ".join(print_deck.row4)
            print print_row1_text
            print print_row2_text
            print print_row3_text
            print print_row4_text
        return return_string


class bcolors:
    Frame = '\033[95m'
    #Frame = Fore.RED
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    #ENDC = 'Style.RESET_ALL'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# SOME METHODS


def create4x4grid(log, width=8,depth=8):

    my_stage = StagePlatform(log)

    decks_wide = width / 4
    decks_deep = depth / 4

    if decks_wide >= 1 and decks_deep >= 1:
        my_stage.add_row(decks_deep)
        for row in my_stage.DeckRows:
            row.add_decks(decks_wide)

    return my_stage


def combine_into_4x8_grid(my_stage=None):
    # This method takes a 4x4 grid and combines decks into 4x8 versions

    for idx, row in enumerate(my_stage.DeckRows):
        # loop through each row and group widthly

        for idx2, deck in enumerate(row.Decks):

            # Set up or prior and next deck values
            prior_deck = None
            next_deck = None
            if idx2 - 1 > -1:
                prior_deck = row.Decks[idx2 - 1]
            if idx2 + 1 < len(row.Decks):
                next_deck = row.Decks[idx2 + 1]

            # Check if the current deck is a child widthly
            if deck.isWidthChild:
                continue
            else:
                # not a child yet
                if prior_deck is not None:
                    if not prior_deck.isWidthChild:
                        # Neither current deck or prior deck are width children yet
                        # Therefore we will combine them
                        prior_deck.hasWidthChild = True
                        deck.isWidthChild = True
                    else:
                        # The prior deck is a width child but the current deck is not
                        continue
    for idx, row in enumerate(my_stage.DeckRows):

        prior_row = None
        if idx - 1 > -1:
            prior_row = my_stage.DeckRows[idx - 1]
        for idx2, deck in enumerate(row.Decks):

            if not deck.isWidthChild and not deck.isDepthChild:
                # this deck is not already a child

                # Set up prior deck value
                prior_deck = None
                if prior_row is not None:
                    # there is a row above the current row
                    if idx2 + row.Offset < len(prior_row.Decks):
                        # there is a deck in the same width position as our current deck in the prior row

                        prior_deck = prior_row.Decks[idx2 + row.Offset - prior_row.Offset]

                        if not prior_deck.hasWidthChild and not prior_deck.hasDepthChild and not prior_deck.isDepthChild:
                            # So now we make this deck a child of the matching deck in prior row
                            prior_deck.hasDepthChild = True
                            deck.isDepthChild = True


def create_stage(log,width=8,depth=8):
    astage = create4x4grid(log, width, depth)
    combine_into_4x8_grid(astage)
    astage.frame_me()
    astage.tophat_me()
    return astage