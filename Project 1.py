#!/usr/bin/env python
# coding: utf-8

# In[22]:


import numpy as np
import math
import matplotlib.pyplot as plt


# Heuristic Function that counts the number of wrong values in a given state
def utilityMisplacedTiles(state, r, c):
    
    # Initializes the count
    count = 0
    
    # Loops through the entire list
    for i in range(r*c):
        
        # If it is in the correct position than increase count by 1
        # 0 is in the last spot or
        if(state[i] == 0 and i == r*c-1):
            count += 1
        
        #Each value is in the correct position
        elif(state[i] == i+1):
            count += 1
    
    # The total positions minus the number of correct positions returns the number of wrong positions
    return r*c - count

#Sends the heuristic value of always 0
def justUniformCost(state, r, c):
    return 0

# Heuristic Function that counts the distance between an element and its correct position
def ManhattanDistance(state, r, c):
    
    # Initializes the total to 0
    total = 0
    
    # Loops through the entire state
    for i in range(r*c):
        
        # Checks if it is the blank position
        if(state[i] == 0):
            
            #Finds the distance between its row and the last row
            total += abs(math.floor(i / r) - math.floor((r*c-1)/r))
            
            #Finds the distance between its coloumn and the last coloumn and adds to the total
            total += abs((i+1) % c - (r*c) % c)
        # Does similar to the blank_pos but instead of the last row and coloumn, it is to its correct row and coloumn
        else:
            total += abs(math.floor(i / r) - math.floor((state[i]-1)/r))
            total += abs((i+1) % c - state[i] % c)
    return total

#Swaps the position in a list with the two given postions
def swapPositions(list, pos1, pos2): 
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

#Sorts the nodes and corresponding cost
def sort_Cost(nodes, cost):
    
    #Copying the most recently added elements
    sort_value = cost[-1]
    noded = nodes[-1]
    
    # Initializing the position that it will be inserted
    pos = len(cost) - 1
    
    # Finds the lowest cost that is bigger than this cost and saves its position
    for i in range (len(cost) - 1):
        if(cost[-1] < cost[i]):
            pos = i
            break
    
    # Removes the newly added items that were saved
    cost.pop()
    nodes.pop()
    
    # So it does not interfere with the current cost and node
    if(pos == 0):
        pos = 1

    #inserts new cost and node at same corresponding position
    cost.insert(pos, sort_value)
    nodes.insert(pos, noded)
    return nodes, cost    

# Helper function that loops through the records, if it finds a record of the given node it returns false
# Otherwise it returns true
def record_check(node, record):
    for i in range (len(record)):
        if(node == record[i]):
            return False
    return True

    
# Solving the game Function    
def solve_game(init_state, r, c, utilityFCN):
    # Check if the dimensions given is the same as the init_state
    if(r*c is not len(init_state)):
        print("Initial state does not match dimensions")
        return False
    
    # Checking if there is any element that is larger than the number of elements within the puzzle
    for i in range (r*c):
        if(init_state[i] >= r*c):
            print("Element out of bounds")
            return False
    
    # Initialization of the nodes, cost, record lists and the blank_pos and depth values
    blank_pos = 0
    nodes = [init_state]
    #cost = [utilityFCN(init_state, r, c)]
    cost = [0]
    depth = 0
    record = list(nodes)
    print("Expanding the state: ") 
    for i in range(r):
        print(nodes[0][i*r:i*r + c])
    # Infinite loop that runs until there is no more children to check
    while len(nodes) != 0:
        
        # Check if it is solved and prints the amount moves to solve, 
        # Return whether it was a success or failure, length of the records and the nodes queue
        goal = utilityMisplacedTiles(nodes[0], r, c)
        if(goal == 0):
            print("Goal!!! \n To solve this problem the search algorithm expanded a total of ", len(record) - len(nodes), "nodes.")
            print("The maximum number of nodes in the queue is at any one time was ", len(nodes), ".")
            print("The depth of the goal node was ", depth, ".")
            return True, len(nodes), len(record)
        
        # Finds the blank's position of the current state (node[0])
        for i in range(c*r):
            if(nodes[0][i] == 0):
                blank_pos = i
                
    # Finds which column the blank is in and adds the moves appropriately (either move_right, move_left or both)
        # This selects the moves for the far left column
        if(blank_pos % c == 0):
            # This checks if the new state has already been used using a function record_check
            if(record_check(swapPositions(list(nodes[0]), blank_pos, blank_pos+1), record)):
                # This adds the new move that adds move_right using a function SwapPositions
                nodes.append(swapPositions(list(nodes[0]), blank_pos, blank_pos+1))
                # This adds the new cost of the corresponding node using a combination of the Uniform cost (depth) 
                # and the heuristic function (utilityFCN)
                cost.append(depth + utilityFCN(nodes[-1],r, c))
                # This sorts the new node in the queue based off of the sorted position of its corresponding cost
                # using function sort_Cost
                nodes, cost = sort_Cost(list(nodes), list(cost))
                # This adds the new node to the records of visited nodes
                record.append(list(nodes[-1]))
                
        # This selects the moves for the far right column
        elif(blank_pos % c == c-1):
            if(record_check(swapPositions(list(nodes[0]), blank_pos, blank_pos-1), record)):
                # This adds the move_left using the function SwapPositions
                nodes.append(swapPositions(list(nodes[0]), blank_pos, blank_pos-1))
                cost.append(depth + utilityFCN(nodes[-1],r, c))
                nodes, cost = sort_Cost(list(nodes), list(cost))
                record.append(list(nodes[-1]))
        # This selects the moves for every column in between
        else:
            if(record_check(swapPositions(list(nodes[0]), blank_pos, blank_pos-1), record)):
                # This adds the move_left using the function SwapPositions
                nodes.append(swapPositions(list(nodes[0]), blank_pos, blank_pos-1))
                cost.append(depth + utilityFCN(nodes[-1],r, c))
                nodes, cost = sort_Cost(list(nodes), list(cost))
                record.append(list(nodes[-1]))
            if(record_check(swapPositions(list(nodes[0]), blank_pos, blank_pos+1), record)):
                # This adds the move_right using the function SwapPositions
                nodes.append(swapPositions(list(nodes[0]), blank_pos, blank_pos+1))
                cost.append(depth + utilityFCN(nodes[-1],r, c))
                nodes, cost = sort_Cost(list(nodes), list(cost))
                record.append(list(nodes[-1]))
                
        # Finds which row the blank is in and adds the moves approprately (either move_up, move_down, or both)
        if(math.floor(blank_pos/r) == 0):
            if(record_check(swapPositions(list(nodes[0]), blank_pos, blank_pos+3), record)):
                # This adds the move_down using the function SwapPositions
                nodes.append(swapPositions(list(nodes[0]), blank_pos, blank_pos+3))
                cost.append(depth + utilityFCN(nodes[-1],r, c))
                nodes, cost = sort_Cost(list(nodes), list(cost))
                record.append(list(nodes[-1]))
        elif(math.floor(blank_pos/r) == r-1):
            if(record_check(swapPositions(list(nodes[0]), blank_pos, blank_pos-3), record)):
                # This adds the move_up using the function SwapPositions
                nodes.append(swapPositions(list(nodes[0]), blank_pos, blank_pos-3))
                cost.append(depth + utilityFCN(nodes[-1],r, c))
                nodes, cost = sort_Cost(list(nodes), list(cost))
                record.append(list(nodes[-1]))
        else:
            if(record_check(swapPositions(list(nodes[0]), blank_pos, blank_pos-3), record)):
                # This adds the move_up using the function SwapPositions
                nodes.append(swapPositions(list(nodes[0]), blank_pos, blank_pos-3))
                cost.append(depth + utilityFCN(nodes[-1],r, c))
                nodes, cost = sort_Cost(list(nodes), list(cost))
                record.append(list(nodes[-1]))
            if(record_check(swapPositions(list(nodes[0]), blank_pos, blank_pos+3), record)):
                # This adds the move_down using the function SwapPositions
                nodes.append(swapPositions(list(nodes[0]), blank_pos, blank_pos+3))
                cost.append(depth + utilityFCN(nodes[-1],r, c))
                nodes, cost = sort_Cost(list(nodes), list(cost))
                record.append(list(nodes[-1]))
        
       

        # Pops the top node and its cost from the queue
        nodes.pop(0)
        cost.pop(0)
        # determines the depth of the current state
        depth = cost[0] - utilityFCN(nodes[0], r, c) + 1
        print("\n The best state to expand with a g(n) = ", depth, "and h(n) = ", utilityFCN(nodes[1],r,c), "is...")
        for i in range(r):
            print(nodes[0][i*r:i*r + c])
        
    # If it is unable to find a Solution, it returns false
    return False, len(nodes), len(record)


#----- Main --------#
initial_state= [1,2,3,4,0,6,7,5,8]

# print("Welcome to Bertie Woosters 8-puzzle solver.")
# print("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle")
# Ans = 0
# Ans = int(input())
# if(Ans == 2):
#     print(" Enter your puzzle, use a zero to represent the blank")
#     FirstRow = input("Enter the first row, use space or tabs between numbers")
#     SecondRow = input("Enter the second row, use space or tabs between numbers")
#     ThirdRow = input("Enter the third row, use space or tabs between numbers")
#     init_state = FirstRow.split() + SecondRow.split() + ThirdRow.split()
#     print(init_state)
#     for i in range(len(init_state)):
#         init_state[i] = int(init_state[i])
#     print(init_state)
#     initial_state = list(init_state)
#     print(initial_state)
#     print("Enter your choice of algorithm")
#     print("   1. Uniform Cost Search")
#     print("   2. A* with the Misplaced Tile heuristic")
#     print("   3. A* with the Manhattan distance heuristic")
#     Alg = int(input())
#     Algor = ""
#     if(Alg == 1):
#         Algor = "justUniformCost"
#     elif(Alg == 2):
#         Algor = "utilityMisplacedTiles"
#     else:
#         Algor = "ManhattanDistance"
    
#     solve_game(initial_state, 3, 3, Algor)
# Test Cases
# trivial = [1,2,3,4,5,6,7,8,0]
# Very_Easy = [1,2,3,4,5,6,7,0,8,]
# Easy = [1,2,0,4,5,3,7,8,6]
# Doable = [0,1,2,4,5,3,7,8,6]
# Oh_Boy = [8,7,1,6,0,2,5,4,3]
# Impossible = [1,2,3,4,5,6,8,7,0]

# x_axis = ['Trivial', 'Very Easy', 'Easy', 'Doable', 'Oh_Boy']

# ManHanDist = []
# MisPlaceTiles = []
# UniCost = []

# ManHanDist.append(solve_game(trivial,3,3, ManhattanDistance))
# ManHanDist.append(solve_game(Very_Easy,3,3, ManhattanDistance))
# ManHanDist.append(solve_game(Easy,3,3, ManhattanDistance))
# ManHanDist.append(solve_game(Doable,3,3, ManhattanDistance))
# #ManHanDist.append(solve_game(Oh_Boy,3,3, ManhattanDistance))
# #ManHanDist.append(solve_game(Impossible,3,3, ManhattanDistance))
# ManHanDistQueues  = [ManHanDist[0][1], ManHanDist[1][1], ManHanDist[2][1], ManHanDist[3][1], 34255]
# ManHanDistRecords = [ManHanDist[0][2], ManHanDist[1][2], ManHanDist[2][2], ManHanDist[3][2], 63895]

# MisPlaceTiles.append(solve_game(trivial,3,3,utilityMisplacedTiles))
# MisPlaceTiles.append(solve_game(Very_Easy,3,3,utilityMisplacedTiles))
# MisPlaceTiles.append(solve_game(Easy,3,3,utilityMisplacedTiles))
# MisPlaceTiles.append(solve_game(Doable,3,3,utilityMisplacedTiles))
# #MisPlaceTiles.append(solve_game(Oh_Boy,3,3,utilityMisplacedTiles))
# #MisPlaceTiles.append(solve_game(Impossible,3,3,utilityMisplacedTiles))
# MisPlaceTilesQueues  = [MisPlaceTiles[0][1], MisPlaceTiles[1][1], MisPlaceTiles[2][1], MisPlaceTiles[3][1],  52759]
# MisPlaceTilesRecords = [MisPlaceTiles[0][2], MisPlaceTiles[1][2], MisPlaceTiles[2][2], MisPlaceTiles[3][2], 103845]


# UniCost.append(solve_game(trivial,3,3,justUniformCost))
# UniCost.append(solve_game(Very_Easy,3,3,justUniformCost))
# UniCost.append(solve_game(Easy,3,3,justUniformCost))
# UniCost.append(solve_game(Doable,3,3,justUniformCost))
# #UniCost.append(solve_game(Oh_Boy,3,3,justUniformCost))
# #UniCost.append(solve_game(Impossible,3,3,justUniformCost))
# UniCostQueues  = [UniCost[0][1], UniCost[1][1], UniCost[2][1], UniCost[3][1],  23418]
# UniCostRecords = [UniCost[0][2], UniCost[1][2], UniCost[2][2], UniCost[3][2], 114293]

# fig, ax1 = plt.subplots(figsize =(20, 10))
# ax1.plot(x_axis, ManHanDistQueues, c='r', label = 'Manhattan Distance')
# ax1.plot(x_axis, MisPlaceTilesQueues, c='b', label = 'Misplaced Tiles Heuristic')
# ax1.plot(x_axis, UniCostQueues, c='g', label = 'Uniform Cost Only')
# plt.xlabel("Level of Difficulty", fontsize=18)
# plt.ylabel("Size of Queue", fontsize=18)
# plt.yscale("log")
# ax1.legend()
# ax1.grid(True)
# plt.show()

# fig2, ax2 = plt.subplots(figsize =(20, 10))
# ax2.plot(x_axis, ManHanDistRecords, c='r', label = 'Manhattan Distance')
# ax2.plot(x_axis, MisPlaceTilesRecords, c='b', label = 'Misplaced Tiles Heuristic')
# ax2.plot(x_axis, UniCostRecords, c='g', label = 'Uniform Cost Only')
# plt.xlabel("Level of Difficulty", fontsize=18)
# plt.ylabel("Number of All Nodes Recorded", fontsize=18)
# plt.yscale("log")
# ax2.legend()
# ax2.grid(True)
# plt.show()

# fig3, ax3 = plt.subplots(figsize =(20, 10))
# ax3.plot(x_axis, (np.subtract(ManHanDistRecords, ManHanDistQueues)), c='r', label = 'Manhattan Distance')
# ax3.plot(x_axis, (np.subtract(MisPlaceTilesRecords, MisPlaceTilesQueues)), c='b', label = 'Misplaced Tiles Heuristic')
# ax3.plot(x_axis, np.subtract(UniCostRecords, UniCostQueues), c='g', label = 'Uniform Cost Only')
# plt.xlabel("Level of Difficulty", fontsize=18)
# plt.ylabel("Number of All Nodes Visited", fontsize=18)
# #plt.yscale("log")
# ax3.legend()
# ax3.grid(True)
# plt.show()
row = int(input("Input the number of rows: "))
columns = int(input("Input the number of columns: "))

for i in range (columns):
    print("Input ", columns, " numbers for", i+1, "row: ")
    for j in range (row):
        initial_state[i*columns+j] = int(input())
print("Initial State: ", initial_state)

print("Using Manhattan Distance:")
solve_game(initial_state,row,columns, ManhattanDistance)

print("Using Misplaced Tiles:")    
solve_game(initial_state,row,columns, utilityMisplacedTiles)

print("Using Uniform Cost:")    
solve_game(initial_state,row,columns, justUniformCost)
    

            
    

        
    


# In[ ]:





# In[ ]:





# In[ ]:




