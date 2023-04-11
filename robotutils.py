from pybricks.parameters import Color

class BarcodeUtils:

    ONE = [1,0,0,0]
    TWO = [1,0,1,0]
    THREE = [1,1,0,0]
    FOUR = [1,0,0,1]

    def match_bottom_three(self, colors_scanned: list):
        pass

    def convert_scanned_colors_to_barcode(self, colors_scanned: list):
        # e.g. input:
        # Color.WHITE
        # Color.WHITE
        # Color.WHITE
        # Color.WHITE
        # Color.WHITE
        # Color.WHITE
        # Color.GREEN
        # Color.BLACK
        # Color.WHITE
        # Color.WHITE
        # Color.WHITE
        # Color.GREEN
        # Color.BLACK
        # Color.BLUE
        #
        # should become: [0, 1, 0, 1] (1 = black/dark, 0 = white)

        output = []

        # find the points where the color changes to the next color
        for i in range(len(colors_scanned) - 1):
            if colors_scanned[i] != colors_scanned[i + 1]:
                output.append(colors_scanned[i])

        # now we have an output with a lot of colors, so we need to merge the following
        # blue/green/black/everything else -> black
        # yellow/white -> white

        secondary_output = []

        for i in range(len(output)):
            if output[i] == Color.YELLOW or output[i] == Color.WHITE:
                secondary_output.append(Color.WHITE)
            else:
                secondary_output.append(Color.BLACK)
    
        print(secondary_output)
        # make a new array with 4 different colors

        pass


barcode_utils = BarcodeUtils()