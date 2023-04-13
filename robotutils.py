from pybricks.parameters import Color

ONE = [1,0,0,0]
TWO = [1,0,1,0]
THREE = [1,1,0,0]
FOUR = [1,0,0,1]

DEFAULT_BARCODE = 2

class BarcodeUtils:

    def match_barcode(self, input):
        if input == ONE:
            return 1
        elif input == TWO:
            return 2
        elif input == THREE:
            return 3
        elif input == FOUR:
            return 4
        else:
            return DEFAULT_BARCODE

    def convert_scanned_colors_to_barcode(self, colors_scanned: list) -> int:
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

        # now we have an output with a lot of colors, so we need to merge the colors by similarity

        secondary_output = []

        for i in range(len(output)):
            if output[i] == Color.BLACK:
                secondary_output.append(Color.BLACK)
            elif output[i] == Color.WHITE or output[i] == Color.BLUE:
                secondary_output.append(Color.WHITE)
            else: pass

        output = []
        # convert black to 1 and white to 0
        for i in range(len(secondary_output)):
            if secondary_output[i] == Color.BLACK:
                output.append(1)
            elif secondary_output[i] == Color.WHITE:
                output.append(0)
            else: pass

        # reverse the list
        output = output[::-1]

        print(output)

        return self.match_barcode(output)
    

# All coordiantes in inches
class Coordinates:

    # diagram
    # []
    #   [.....]   [.....]
    #   [.....]   [.....] 
    #   [.....]   [.....]
    #   [.....]   [.....] 
    # []

    def adjust_coordinates_by_starting_position(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        # make them in terms of 0,0 being the home a
        x -= self.home_a_coordinates()[0]
        y -= self.home_a_coordinates()[1]
        
        return (x, y)

    def home_a_coordinates(self):
        return (6, -6)

    def home_b_coordinates(self):
        return (102, -6)
    
    def home_c_coordinates(self):
        return (6, 114)
    
    def home_d_coordinates(self):
        return (102, 114)

    def a1_top_left_coordinates(self):
        return (12, 24)
    
    def a2_top_left_coordinates(self):
        return (12, 48)
    
    def c1_top_left_coordinates(self):
        return (12, 72)
    
    def c2_top_left_coordinates(self):
        return (12, 96)
    
    def b1_top_left_coordinates(self):
        return (60, 24)
    
    def b2_top_left_coordinates(self):
        return (60, 48)
    
    def d1_top_left_coordinates(self):
        return (60, 72)
    
    def d2_top_left_coordinates(self):
        return (60, 96)
    
    def convert_inch_to_mm(self, inch):
        return inch * 25.4
    
    def coordinate_to_mm(self, coordinate):
        return (self.convert_inch_to_mm(coordinate[0]), self.convert_inch_to_mm(coordinate[1]))
    
    def get_stage1_coordinate_from_top_left_of_shelving(self, box_number, shelving_top_left):
        # each shelving unit is 36 inches long and 12 inches wide
        # (long is x, wide is y)

        # box number is 1-12, 6 on each side of the shelving

        # if box # <= 6, its on the lower side of the shelving
        # if box # > 6, its on the upper side of the shelving

        # each box CENTER is 6 inches from each other,
        # and the furthest left is 3 inches
        # from the left side of the shelving,
        # and the furthest right is 3 inches
        # from the right side of the shelving

        # find the x coordinate of the box (the front of the box)
        
        if box_number <= 6:
            x = shelving_top_left[0] + 3 + (6 * (box_number - 1))
            y = shelving_top_left[1] - 12 - 6
        else:
            x = shelving_top_left[0] + 3 + (6 * (box_number - 7))
            y = shelving_top_left[1] + 6

        return (x, y)
    
    def get_y_coordinate_to_drive(self, box_number, box_coordinate):
        box_y_coordinate = box_coordinate[1]
        if box_number <= 6:
            return box_y_coordinate - 6
        else:
            return box_y_coordinate + 6
        
    def generate_stage1_coordinates(self, input_array):
        # e.g. input array
        # ["A1_6", "3", "B"]
        # [ShelvingUnit_BoxNumber, Barcode, FullfillmentCenter]
        # ShelvingUnits: A1, A2, B1, B2, C1, C2, D1, D2
        # FullfillmentCenters: A, B, C, D
        # BoxNumbers: 1-12

        shelving_unit = input_array[0].split("_")[0]
        box_number = int(input_array[0].split("_")[1])
        
        if shelving_unit == "A1":
            return self.get_stage1_coordinate_from_top_left_of_shelving(box_number, self.a1_top_left_coordinates())
        elif shelving_unit == "A2":
            return self.get_stage1_coordinate_from_top_left_of_shelving(box_number, self.a2_top_left_coordinates())
        elif shelving_unit == "B1":
            return self.get_stage1_coordinate_from_top_left_of_shelving(box_number, self.b1_top_left_coordinates())
        elif shelving_unit == "B2":
            return self.get_stage1_coordinate_from_top_left_of_shelving(box_number, self.b2_top_left_coordinates())
        elif shelving_unit == "C1":
            return self.get_stage1_coordinate_from_top_left_of_shelving(box_number, self.c1_top_left_coordinates())
        elif shelving_unit == "C2":
            return self.get_stage1_coordinate_from_top_left_of_shelving(box_number, self.c2_top_left_coordinates())
        elif shelving_unit == "D1":
            return self.get_stage1_coordinate_from_top_left_of_shelving(box_number, self.d1_top_left_coordinates())
        elif shelving_unit == "D2":
            return self.get_stage1_coordinate_from_top_left_of_shelving(box_number, self.d2_top_left_coordinates())
        else: # return A1 for safety
            return self.get_stage1_coordinate_from_top_left_of_shelving(box_number, self.a1_top_left_coordinates())

barcode_utils = BarcodeUtils()
coordinates = Coordinates()
