import numpy as np
from itertools import izip

board_raw = np.zeros(81, dtype = "int")
board_raw.shape = (3,3,3,3)

primary_list = range(1,10)
step = 0


pu_row_board = np.zeros(81, dtype = "int")
pu_row_board.shape = (3,3,3,3)

pu_col_board = np.zeros(81, dtype = "int")
pu_col_board.shape = (3,3,3,3)



def print_board(board_raw):
    print "*---------*---------*---------*"
    for y in range(3):
        for x in range (3):
            print "|", board_raw[y,0,x,:], "|", board_raw[y,1,x,:], "|", board_raw[y,2,x,:],"|"
        print "*---------*---------*---------*"


def ask():
    for number in range(1,82):
        print ">>"
        if number % 9 != 0:
            x = int((number) % 9)
        else:
            x = 9
        y = int(np.ceil(float(number) / 9))
        slot = raw_input("Row %d | Column %d: " % (y,x))

        if slot == "":
            pass
        elif -1<int(slot)<10:
            a1 = int(np.ceil(float(y)/3)) - 1
            a2 = int(np.ceil(float(x)/3)) - 1
            a3 = (y-1) - 3*a1
            a4 = (x-1) - 3*a2

            board_raw[a1,a2,a3,a4] = slot
        else:
            print "\t \t \t ***** Input Error *****"
            quit()

    print_board(board_raw)
    print "\n"

    proceed = ""
    scrap = ""
    row_to_fix = -1
    col_to_fix = -1
    num_to_replace = -1
    full_proceed = ""
    while proceed != "y" and proceed != "n":
        print "Solve sudoku?"
        proceed = raw_input("'y' or 'n': ")
        if proceed == "y":
            pass
        elif proceed == "n":
            while scrap != "s" and scrap != "f":
                print "Scrap, or fix a square?"
                scrap = raw_input("'s' or 'f': ")
                if scrap == "s":
                    quit()

                elif scrap == "f":
                    while (row_to_fix < 0 or row_to_fix > 9) and (col_to_fix < 0 or col_to_fix > 9) and \
                    (num_to_replace < 0 or num_to_replace > 9) or (full_proceed != "y"):
                        print "Which square to fix?"
                        row_to_fix = int(raw_input("Row: "))
                        col_to_fix = int(raw_input("Col: "))
                        num_to_replace = raw_input("Correct number: ")

                        if num_to_replace == "":
                            num_to_replace = 0

                        if -1<int(row_to_fix)<10 and -1<int(col_to_fix)<10 and -1<int(num_to_replace)<10:
                            a1 = int(np.ceil(float(row_to_fix)/3)) - 1
                            a2 = int(np.ceil(float(col_to_fix)/3)) - 1
                            a3 = (row_to_fix-1) - 3*a1
                            a4 = (col_to_fix-1) - 3*a2

                            board_raw[a1,a2,a3,a4] = num_to_replace
                            print "Replaced!"
                            print "\n"
                            print_board(board_raw)
                            "\n"
                            print "Solve sudoku?"
                            print "\n"
                            full_proceed = raw_input("'y' or 'n': ")
                            if full_proceed == "y":
                                pass
                            elif full_proceed == "n":
                                print "Scrap, or fix a square?"
                                scrap = raw_input("'s' or 'f': ")
                                if scrap == "s":
                                    quit()
                            else:
                                print "\n"
                                print "Bad input"
                                print "\n"
                        else:
                            print "\n"
                            print "Bad input"
                            print "\n"
                else:
                    print "\n"
                    print "Bad input"
                    print "\n"
        else:
            print "\n"
            print "Bad input"
            print "\n"


def convert_coordinates(index,p): #for list of length p
    if p == 9:
        b1 = int(np.floor(float(index)/3))
        b2 = int(index - 3*b1)
        return (b1,b2)

    if p == 81:
        b1 = int(np.floor(float(index)/27))
        b2 = int(np.floor(float(index)/9) - 3*b1)
        return (b1,b2)


def zero_fill_method():
    global step
    row = []
    column = []
    square = []
    for y in range(3):
        for x in range(3):
            row = np.array([board_raw[y,0,x,:], board_raw[y,1,x,:], board_raw[y,2,x,:]])
            new_row = row.flatten().tolist()
            if new_row.count(0) == 1:
                zero_index = new_row.index(0)
                zero_replace = list(set(primary_list).difference(new_row))
                (c,d) = convert_coordinates(zero_index,9)
                board_raw[y,c,x,d] = zero_replace[0]
                print_board(board_raw)
                step += 1
                print "******************************* Normal Row Step:", step, "\n"

    for y in range(3):
        for x in range(3):
            column = np.array([board_raw[0,y,:,x], board_raw[1,y,:,x], board_raw[2,y,:,x]])
            new_column = column.flatten().tolist()
            if new_column.count(0) == 1:
                zero_index = new_column.index(0)
                zero_replace = list(set(primary_list).difference(new_column))
                (c,d) = convert_coordinates(zero_index,9)
                board_raw[c,y,d,x] = zero_replace[0]
                print_board(board_raw)
                step += 1
                print "******************************* Normal Column Step:", step, "\n"

    for y in range(3):
        for x in range(3):
            square = np.array([board_raw[y,x]])
            new_square = square.flatten().tolist()
            if new_square.count(0) == 1:
                zero_index = new_square.index(0)
                zero_replace = list(set(primary_list).difference(new_square))
                (c,d) = convert_coordinates(zero_index,9)
                board_raw[y,x,c,d] = zero_replace[0]
                print_board(board_raw)
                step += 1
                print "******************************* Normal Square Step:", step, "\n"


def attack_method(gear):
    global step
    false_step = 0

    if gear == 2:
        adv_comp_board = np.zeros(729)
        adv_comp_board.shape = (3,3,3,3,9)

    for n in range(1,10):
        n_coord_list_raw = np.where(board_raw == n)
        n_coord_list = tuple(izip(*n_coord_list_raw)) #list of coords of n
        n_instance_number = len(n_coord_list)
        if n_instance_number == 9 and n != 9:
            false_step += 1
            continue

        big_square_step = 0
        for y in range(3):
            for x in range(3):
                board_raw_copy = np.copy(board_raw[y,x])
                if n not in board_raw_copy or n == 9: #begins work on squares without n
                    board_raw_copy_flattened = board_raw_copy.flatten().tolist()

                    if n in board_raw_copy:
                        board_raw_copy.fill(99)

                    for small_box in board_raw_copy_flattened:
                        if small_box != 0:
                            small_box_index = board_raw_copy_flattened.index(small_box)
                            (c,d) = convert_coordinates(small_box_index,9)
                            board_raw_copy[c,d] = 99

                    for n_instance in range(n_instance_number):
                        if n_coord_list[n_instance][0] == y:
                            row_to_attack = n_coord_list[n_instance][2]
                            board_raw_copy[row_to_attack,:] = 99

                        if n_coord_list[n_instance][1] == x:
                            column_to_attack = n_coord_list[n_instance][3]
                            board_raw_copy[:,column_to_attack] = 99


                    pu_row_board_n_coord_list_raw = np.where(pu_row_board == n) #parallel unknown method ROW-INPUT
                    pu_row_board_n_coord_list = tuple(izip(*pu_row_board_n_coord_list_raw))
                    pu_row_n_instance_number = len(pu_row_board_n_coord_list)

                    for n_instance in range(pu_row_n_instance_number):
                        if pu_row_board_n_coord_list[n_instance][0] == y and \
                        pu_row_board_n_coord_list[n_instance][1] != x:
                            ROW_TO_ATTACK = pu_row_board_n_coord_list[n_instance][2]
                            board_raw_copy[ROW_TO_ATTACK,:] = 99

                    pu_col_board_n_coord_list_raw = np.where(pu_col_board == n) #parallel unknown method COL-INPUT
                    pu_col_board_n_coord_list = tuple(izip(*pu_col_board_n_coord_list_raw))
                    pu_col_n_instance_number = len(pu_col_board_n_coord_list)

                    for n_instance in range(pu_col_n_instance_number):
                        if pu_col_board_n_coord_list[n_instance][1] == x and \
                        pu_col_board_n_coord_list[n_instance][0] != y:
                            COL_TO_ATTACK = pu_col_board_n_coord_list[n_instance][3]
                            board_raw_copy[:,COL_TO_ATTACK] = 99


                    board_raw_copy_flattened = board_raw_copy.flatten().tolist() #updating board_raw_copy_flattened
                    if board_raw_copy_flattened.count(0) == 1: #entering n value into square
                        zero_index = board_raw_copy_flattened.index(0)
                        (c,d) = convert_coordinates(zero_index,9)
                        board_raw[y,x,c,d] = n
                        print_board(board_raw)
                        step += 1
                        big_square_step += 1
                        if gear == 2:
                            adv_comp_board[y,x,c,d] = 0
                        print "******************************* Normal Step:", step, "\n"



                    if board_raw_copy_flattened.count(0) == 2: #parallel unknown method 2-box
                        zeros_list_raw_2 = np.where(board_raw_copy == 0)
                        zeros_list_2 = tuple(izip(*zeros_list_raw_2))

                        if zeros_list_2[0][0] == zeros_list_2[1][0]:
                            row_to_attack_pu_1 = zeros_list_2[0][0]
                            for nnn in range(3):
                                if pu_row_board[y,x,row_to_attack_pu_1,nnn] == n:
                                    break
                                elif pu_row_board[y,x,row_to_attack_pu_1,nnn] == 0:
                                    pu_row_board[y,x,row_to_attack_pu_1,nnn] = n
                                    break
                        if zeros_list_2[0][1] == zeros_list_2[1][1]:
                            col_to_attack_pu_1 = zeros_list_2[0][1]
                            for nnn in range(3):
                                if pu_col_board[y,x,nnn,col_to_attack_pu_1] == n:
                                    break
                                elif pu_col_board[y,x,nnn,col_to_attack_pu_1] == 0:
                                    pu_col_board[y,x,nnn,col_to_attack_pu_1] = n
                                    break


                    if board_raw_copy_flattened.count(0) == 3: #parallel unknown method 3-box
                        zeros_list_raw_3 = np.where(board_raw_copy == 0)
                        zeros_list_3 = tuple(izip(*zeros_list_raw_3))

                        if zeros_list_3[0][0] == zeros_list_3[1][0] == zeros_list_3[2][0]:
                            row_to_attack_pu_2 = zeros_list_3[0][0]
                            for nnn in range(3):
                                if pu_row_board[y,x,row_to_attack_pu_2,nnn] == n:
                                    break
                                elif pu_row_board[y,x,row_to_attack_pu_2,nnn] == 0:
                                    pu_row_board[y,x,row_to_attack_pu_2,nnn] = n
                                    break
                        if zeros_list_3[0][1] == zeros_list_3[1][1] == zeros_list_3[2][1]:
                            col_to_attack_pu_2 = zeros_list_3[0][1]
                            for nnn in range(3):
                                if pu_col_board[y,x,nnn,col_to_attack_pu_2] == n:
                                    break
                                elif pu_col_board[y,x,nnn,col_to_attack_pu_2] == 0:
                                    pu_col_board[y,x,nnn,col_to_attack_pu_2] = n
                                    break


                    if gear == 2: #adv_comp_board array setup and input
                        if board_raw_copy_flattened.count(0) > 1:
                            small_box_zero_indices_list = [i for i,ZERO_SLOT in enumerate(board_raw_copy_flattened) if ZERO_SLOT == 0]
                            index_instances = len(small_box_zero_indices_list)
                            for small_box in range(index_instances):
                                small_box_index = small_box_zero_indices_list[small_box]
                                (c,d) = convert_coordinates(small_box_index,9)
                                for nnn in range(9):
                                    if adv_comp_board[y,x,c,d,nnn] == n:
                                        break
                                    elif adv_comp_board[y,x,c,d,nnn] == 0:
                                        adv_comp_board[y,x,c,d,nnn] = n
                                        break

                        if n == 9: #simplification of adv_comp_board, begin adv_comp solving methods

                            adv_comp_board_copy = np.copy(adv_comp_board[y,x])
                            adv_comp_board_copy_flattened = adv_comp_board_copy.flatten().tolist()

                            for first_num_to_compare in range(1,10): #method to simplify potentials in double case
                                for second_num_to_compare in range(1,10):
                                    if first_num_to_compare == second_num_to_compare:
                                        continue

                                    first_num_to_compare_coord_ls_raw = np.where(adv_comp_board_copy == first_num_to_compare)
                                    first_num_to_compare_coord_ls = tuple(izip(*first_num_to_compare_coord_ls_raw))

                                    first_num_to_compare_instance_num = len(first_num_to_compare_coord_ls)

                                    second_num_to_compare_coord_ls_raw = np.where(adv_comp_board_copy == second_num_to_compare)
                                    second_num_to_compare_coord_ls = tuple(izip(*second_num_to_compare_coord_ls_raw))

                                    second_num_to_compare_instance_num = len(second_num_to_compare_coord_ls)

                                    if first_num_to_compare_instance_num == second_num_to_compare_instance_num == 2:
                                        new_compare_ls = []
                                        for c_1 in range(first_num_to_compare_instance_num): #coords of double case
                                            for c_2 in range(second_num_to_compare_instance_num):
                                                if first_num_to_compare_coord_ls[c_1][0] == second_num_to_compare_coord_ls[c_2][0] and \
                                                first_num_to_compare_coord_ls[c_1][1] == second_num_to_compare_coord_ls[c_2][1]:
                                                    new_compare_ls.append(first_num_to_compare_coord_ls[c_1])

                                        if len(new_compare_ls) == 2:
                                            for ins_num in range(first_num_to_compare_instance_num): #reduce potentials
                                                for little_slot in range(9):

                                                    if adv_comp_board[y,x,new_compare_ls[ins_num][0],new_compare_ls[ins_num][1],little_slot] == first_num_to_compare or \
                                                    adv_comp_board[y,x,new_compare_ls[ins_num][0],new_compare_ls[ins_num][1],little_slot] == second_num_to_compare:
                                                        continue
                                                    elif adv_comp_board[y,x,new_compare_ls[ins_num][0],new_compare_ls[ins_num][1],little_slot] != 0:
                                                        adv_comp_board[y,x,new_compare_ls[ins_num][0],new_compare_ls[ins_num][1],little_slot] = 0
                                                    else:
                                                        break


                                            if new_compare_ls[0][0] == new_compare_ls[1][0]: #adding to pu board
                                                row_to_attack_pu_1 = new_compare_ls[0][0]
                                                for nnn in range(3):
                                                    if pu_row_board[y,x,row_to_attack_pu_1,nnn] == first_num_to_compare or \
                                                    pu_row_board[y,x,row_to_attack_pu_1,nnn] == second_num_to_compare:
                                                        break
                                                    elif pu_row_board[y,x,row_to_attack_pu_1,nnn] == 0:
                                                        pu_row_board[y,x,row_to_attack_pu_1,nnn] = first_num_to_compare
                                                        pu_row_board[y,x,row_to_attack_pu_1,nnn+1] = second_num_to_compare
                                                        break
                                            if new_compare_ls[0][1] == new_compare_ls[1][1]: #adding to pu board
                                                col_to_attack_pu_1 = new_compare_ls[0][1]
                                                for nnn in range(3):
                                                    if pu_col_board[y,x,nnn,col_to_attack_pu_1] == first_num_to_compare or \
                                                    pu_col_board[y,x,nnn,col_to_attack_pu_1] == second_num_to_compare:
                                                        break
                                                    elif pu_col_board[y,x,nnn,col_to_attack_pu_1] == 0:
                                                        pu_col_board[y,x,nnn,col_to_attack_pu_1] = first_num_to_compare
                                                        pu_col_board[y,x,nnn+1,col_to_attack_pu_1] = second_num_to_compare
                                                        break

                            for c in range(3): #if single instance of any potential n in LITTLE SQUARE
                                for d in range(3):
                                    adv_comp_board_single_slot_list = adv_comp_board[y,x,c,d].tolist()
                                    if adv_comp_board_single_slot_list.count(0) == 8:
                                        board_raw[y,x,c,d] = adv_comp_board_single_slot_list[0]
                                        print_board(board_raw)
                                        step += 1
                                        big_square_step += 1
                                        adv_comp_board[y,x,c,d] = 0
                                        print "******************************* Little Square Step:", step, "\n"
                            if big_square_step != 0:
                                continue

                            adv_comp_board_copy = np.copy(adv_comp_board[y,x])
                            adv_comp_board_copy_flattened = adv_comp_board_copy.flatten().tolist()
                            for n_in_adv_comp in range(1,10): #if single instance of any potential n in BIG SQUARE
                                if adv_comp_board_copy_flattened.count(n_in_adv_comp) == 1:
                                    single_n_coord = adv_comp_board_copy_flattened.index(n_in_adv_comp)
                                    (c,d) = convert_coordinates(single_n_coord,81)
                                    board_raw[y,x,c,d] = n_in_adv_comp
                                    print_board(board_raw)
                                    step += 1
                                    big_square_step += 1
                                    adv_comp_board[y,x,c,d] = 0
                                    print "******************************* Big Square Step:", step, "\n"
                            if big_square_step != 0:
                                continue

                            if y == 2 and x == 2:
                                for n_in_adv_comp in range(1,10):
                                    adv_step = 0

                                    #if single instance of potential n in ROW
                                    for k in range(3):
                                        for l in range(3):
                                            adv_comp_board_row = np.array([adv_comp_board[k,0,l,:],\
                                            adv_comp_board[k,1,l,:],adv_comp_board[k,2,l,:]])
                                            adv_comp_board_row_flattened = adv_comp_board_row.flatten().tolist()
                                            if adv_comp_board_row_flattened.count(n_in_adv_comp) == 1:
                                                single_n_coord = adv_comp_board_row_flattened.index(n_in_adv_comp)
                                                (c,d) = convert_coordinates(single_n_coord,81)
                                                board_raw[k,c,l,d] = n_in_adv_comp
                                                print_board(board_raw)
                                                step += 1
                                                adv_comp_board[k,c,l,d] = 0
                                                adv_step += 1
                                                print "******************************* ADV ROW Step:", step, "\n"
                                    if adv_step != 0:
                                        break

                                    #if single instance of potential n in COLUMN
                                    for k in range(3):
                                        for l in range(3):
                                            adv_comp_board_col = np.array([adv_comp_board[0,k,:,l],\
                                            adv_comp_board[1,k,:,l],adv_comp_board[2,k,:,l]])
                                            adv_comp_board_col_flattened = adv_comp_board_col.flatten().tolist()
                                            if adv_comp_board_col_flattened.count(n_in_adv_comp) == 1:
                                                single_n_coord = adv_comp_board_col_flattened.index(n_in_adv_comp)
                                                (c,d) = convert_coordinates(single_n_coord,81)
                                                board_raw[c,k,d,l] = n_in_adv_comp
                                                print_board(board_raw)
                                                step += 1
                                                adv_comp_board[c,k,d,l] = 0
                                                print "******************************* ADV COL Step:", step, "\n"


        if big_square_step == 0:
            false_step += 1
    return false_step

#####################################

ask()

final = board_raw.flatten().tolist()
while final.count(0) > 0:
    if attack_method(1) == 9:
        if attack_method(1) == 9:
            zero_fill_method()
            if attack_method(2) == 9:
                zero_fill_method()

    final = board_raw.flatten().tolist()
else:
    print "********** Sudoku SOLVED! **********"
    print "\n"
