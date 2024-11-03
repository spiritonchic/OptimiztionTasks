import numpy as np

def print_parameter_table(supply, demand, cost):
    # Print the input parameter table
    print("\nInput Parameter Table:")
    # Create a header for the table
    print("\n     |", end=' ')
    for j in range(len(demand)):
        print(f" D{j + 1} |", end='  ')
    print(" Supply")

    print("-------" + "------" * (len(demand) + 1))

    for i in range(len(supply)):
        print(f" S{i + 1} |", end=' ')
        for j in range(len(demand)):
            print(f"{cost[i][j]:^4} |", end=' ')
        print(f" {supply[i]}")


def read_input_file(file_path):
    supply = []
    demand = []
    cost_matrix = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Read supply
        i = 1  # Start after the supply header
        while i < len(lines) and (lines[i].startswith('#') or lines[i].strip() == ''):
            i += 1
        supply = list(map(int, lines[i].strip().split()))

        # Read demand
        i += 1  # Move to the next line
        while i < len(lines) and (lines[i].startswith('#') or lines[i].strip() == ''):
            i += 1
        demand = list(map(int, lines[i].strip().split()))

        # Read cost matrix
        i += 1  # Move to the next line
        while i < len(lines):
            if lines[i].strip() != '' and not lines[i].startswith('#'):
                cost_matrix.append(list(map(int, lines[i].strip().split())))
            i += 1

    return np.array(supply), np.array(demand), np.array(cost_matrix)


def allocation_to_vectors(allocation):
    x0_vector = allocation.flatten()
    return x0_vector

def check_balance(supply, demand):
    if sum(supply) != sum(demand):
        print("The problem is not balanced!")
        print()
        return False
    return True

def is_valid_transportation_problem(supply, demand, cost):
    if np.any(cost < 0):
        print("The method is not applicable!")
        print()
        return False

    if np.any(supply <= 0) or np.any(demand <= 0):
        print("The method is not applicable!")
        print()
        return False

    return True


def north_west_corner(supply, demand):
    allocation = np.zeros((len(supply), len(demand)), dtype=int)
    supply = supply.copy()
    demand = demand.copy()
    i = j = 0
    while i < len(supply) and j < len(demand):
        allocated_amount = min(supply[i], demand[j])
        allocation[i][j] = allocated_amount
        supply[i] -= allocated_amount
        demand[j] -= allocated_amount
        if supply[i] == 0 and i < len(supply) - 1:
            i += 1
        elif demand[j] == 0 and j < len(demand) - 1:
            j += 1
        else:
            break
    return allocation


def vogels_approximation(supply, demand, cost):
    allocation = np.zeros((len(supply), len(demand)), dtype=int)
    supply = supply.copy().tolist()
    demand = demand.copy().tolist()
    cost = cost.copy().tolist()
    while sum(supply) > 0 and sum(demand) > 0:
        row_penalties = []
        col_penalties = []
        for i in range(len(supply)):
            if supply[i] > 0:
                row = [c for c, d in zip(cost[i], demand) if d > 0]
                if len(row) >= 2:
                    row_penalties.append((sorted(row)[1] - sorted(row)[0], i))
                else:
                    row_penalties.append((float('inf'), i))
            else:
                row_penalties.append((float('-inf'), i))
        for j in range(len(demand)):
            if demand[j] > 0:
                col = [cost[i][j] for i in range(len(supply)) if supply[i] > 0]
                if len(col) >= 2:
                    col_penalties.append((sorted(col)[1] - sorted(col)[0], j))
                else:
                    col_penalties.append((float('inf'), j))
            else:
                col_penalties.append((float('-inf'), j))
        max_row_penalty, row_idx = max(row_penalties)
        max_col_penalty, col_idx = max(col_penalties)
        if max_row_penalty >= max_col_penalty:
            min_cost = float('inf')
            min_cost_index = -1
            for j in range(len(demand)):
                if demand[j] > 0 and cost[row_idx][j] < min_cost:
                    min_cost = cost[row_idx][j]
                    min_cost_index = j
            allocation_amount = min(supply[row_idx], demand[min_cost_index])
            allocation[row_idx][min_cost_index] = allocation_amount
            supply[row_idx] -= allocation_amount
            demand[min_cost_index] -= allocation_amount
        else:
            min_cost = float('inf')
            min_cost_index = -1
            for i in range(len(supply)):
                if supply[i] > 0 and cost[i][col_idx] < min_cost:
                    min_cost = cost[i][col_idx]
                    min_cost_index = i
            allocation_amount = min(supply[min_cost_index], demand[col_idx])
            allocation[min_cost_index][col_idx] = allocation_amount
            supply[min_cost_index] -= allocation_amount
            demand[col_idx] -= allocation_amount
        for i in range(len(supply)):
            if supply[i] == 0:
                cost[i] = [float('inf')] * len(demand)
        for j in range(len(demand)):
            if demand[j] == 0:
                for row in cost:
                    row[j] = float('inf')
    return allocation

def russells_approximation(supply, demand, cost):
    allocation = np.zeros((len(supply), len(demand)), dtype=int)
    supply = supply.copy().tolist()
    demand = demand.copy().tolist()
    cost = cost.copy().tolist()
    while sum(supply) > 0 and sum(demand) > 0:
        row_penalties = []
        col_penalties = []
        for i in range(len(supply)):
            if supply[i] > 0:
                min_costs = sorted([cost[i][j] for j in range(len(demand)) if demand[j] > 0])
                if len(min_costs) >= 2:
                    row_penalties.append(min_costs[1] - min_costs[0])
                else:
                    row_penalties.append(float('inf'))
            else:
                row_penalties.append(float('-inf'))
        for j in range(len(demand)):
            if demand[j] > 0:
                min_costs = sorted([cost[i][j] for i in range(len(supply)) if supply[i] > 0])
                if len(min_costs) >= 2:
                    col_penalties.append(min_costs[1] - min_costs[0])
                else:
                    col_penalties.append(float('inf'))
            else:
                col_penalties.append(float('-inf'))
        max_row_penalty = max(row_penalties)
        max_col_penalty = max(col_penalties)
        if max_row_penalty >= max_col_penalty:
            row_idx = row_penalties.index(max_row_penalty)
            min_cost = float('inf')
            min_cost_index = -1
            for j in range(len(demand)):
                if demand[j] > 0 and cost[row_idx][j] < min_cost:
                    min_cost = cost[row_idx][j]
                    min_cost_index = j
            allocation_amount = min(supply[row_idx], demand[min_cost_index])
            allocation[row_idx][min_cost_index] = allocation_amount
            supply[row_idx] -= allocation_amount
            demand[min_cost_index] -= allocation_amount
        else:
            col_idx = col_penalties.index(max_col_penalty)
            min_cost = float('inf')
            min_cost_index = -1
            for i in range(len(supply)):
                if supply[i] > 0 and cost[i][col_idx] < min_cost:
                    min_cost = cost[i][col_idx]
                    min_cost_index = i
            allocation_amount = min(supply[min_cost_index], demand[col_idx])
            allocation[min_cost_index][col_idx] = allocation_amount
            supply[min_cost_index] -= allocation_amount
            demand[col_idx] -= allocation_amount
        for i in range(len(supply)):
            if supply[i] == 0:
                cost[i] = [float('inf')] * len(demand)
        for j in range(len(demand)):
            if demand[j] == 0:
                for row in cost:
                    row[j] = float('inf')

    return allocation
'''
s = np.array([140, 180, 160])
d = np.array([60, 70, 120, 130, 100])
c = np.array([
    [2, 3, 4, 2, 4],
    [8, 4, 1, 4, 1],
    [9, 7, 3, 7, 2]
])
'''
for i in range(1, 6):
    s, d, c = read_input_file(f'input{i}.txt')
    if not is_valid_transportation_problem(s, d, c):
        continue
    if not check_balance(s, d):
        continue
    print_parameter_table(s, d, c)
    print("North-West Corner Method:", allocation_to_vectors(north_west_corner(s, d)))
    print("Vogel’s Approximation Method:", allocation_to_vectors(vogels_approximation(s, d, c)))
    print("Russell's Approximation Method:", allocation_to_vectors(russells_approximation(s, d, c)))
    print()

