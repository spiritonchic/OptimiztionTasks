import numpy as np

def print_parameter_table(supply, demand, cost):
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

    print("-------" + "------" * (len(demand) + 1))
    print(f"    |", end=' ')
    for j in range(len(demand)):
        print(f"{demand[j]:^5}|", end=' ')
    print()

def read_input_file(file_path):
    supply = []
    demand = []
    cost_matrix = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 1
        while i < len(lines) and (lines[i].startswith('#') or lines[i].strip() == ''):
            i += 1
        supply = list(map(int, lines[i].strip().split()))
        i += 1
        while i < len(lines) and (lines[i].startswith('#') or lines[i].strip() == ''):
            i += 1
        demand = list(map(int, lines[i].strip().split()))
        i += 1
        while i < len(lines):
            if lines[i].strip() != '' and not lines[i].startswith('#'):
                cost_matrix.append(list(map(int, lines[i].strip().split())))
            i += 1

    return np.array(supply), np.array(demand), np.array(cost_matrix)



def check_balance(supply, demand):
    if sum(supply) != sum(demand):
        return False
    return True

def is_valid_transportation_problem(supply, demand, cost):
    if np.any(cost < 0):
        return False

    if np.any(supply <= 0) or np.any(demand <= 0):
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

    while any(s > 0 for s in supply) and any(d > 0 for d in demand):
        row_penalties = []
        col_penalties = []
        for i, s in enumerate(supply):
            if s > 0:
                row = [cost[i][j] for j, d in enumerate(demand) if d > 0]
                if len(row) >= 2:
                    min1, min2 = np.partition(row, 1)[:2]
                    row_penalties.append((min2 - min1, i))
                else:
                    row_penalties.append((float('inf'), i))
            else:
                row_penalties.append((float('-inf'), i))
        for j, d in enumerate(demand):
            if d > 0:
                col = [cost[i][j] for i, s in enumerate(supply) if s > 0]
                if len(col) >= 2:
                    min1, min2 = np.partition(col, 1)[:2]
                    col_penalties.append((min2 - min1, j))
                else:
                    col_penalties.append((float('inf'), j))
            else:
                col_penalties.append((float('-inf'), j))
        max_row_penalty, row_idx = max(row_penalties)
        max_col_penalty, col_idx = max(col_penalties)
        if max_row_penalty >= max_col_penalty:
            min_cost = float('inf')
            min_cost_index = -1
            for j, d in enumerate(demand):
                if d > 0 and cost[row_idx][j] < min_cost:
                    min_cost = cost[row_idx][j]
                    min_cost_index = j
            allocation_amount = min(supply[row_idx], demand[min_cost_index])
            allocation[row_idx][min_cost_index] = allocation_amount
            supply[row_idx] -= allocation_amount
            demand[min_cost_index] -= allocation_amount
        else:
            min_cost = float('inf')
            min_cost_index = -1
            for i, s in enumerate(supply):
                if s > 0 and cost[i][col_idx] < min_cost:
                    min_cost = cost[i][col_idx]
                    min_cost_index = i
            allocation_amount = min(supply[min_cost_index], demand[col_idx])
            allocation[min_cost_index][col_idx] = allocation_amount
            supply[min_cost_index] -= allocation_amount
            demand[col_idx] -= allocation_amount
        for i, s in enumerate(supply):
            if s == 0:
                cost[i] = [float('inf')] * len(demand)
        for j, d in enumerate(demand):
            if d == 0:
                for row in cost:
                    row[j] = float('inf')
    return allocation


import numpy as np


def russells_approximation(supply, demand, cost):
    allocation = np.zeros((len(supply), len(demand)), dtype=int)
    supply = supply.copy().tolist()
    demand = demand.copy().tolist()
    cost = cost.copy().tolist()

    while sum(supply) > 0 and sum(demand) > 0:
        row_max_costs = [
            max([cost[i][j] for j in range(len(demand)) if demand[j] > 0]) if supply[i] > 0 else float('-inf') for i in
            range(len(supply))]
        col_max_costs = [
            max([cost[i][j] for i in range(len(supply)) if supply[i] > 0]) if demand[j] > 0 else float('-inf') for j in
            range(len(demand))]
        delta = [
            [(cost[i][j] - (row_max_costs[i] + col_max_costs[j])) if supply[i] > 0 and demand[j] > 0 else float('inf')
             for j in range(len(demand))] for i in range(len(supply))]
        min_delta = float('inf')
        min_i = -1
        min_j = -1
        for i in range(len(supply)):
            for j in range(len(demand)):
                if delta[i][j] < min_delta:
                    min_delta = delta[i][j]
                    min_i, min_j = i, j
        allocation_amount = min(supply[min_i], demand[min_j])
        allocation[min_i][min_j] = allocation_amount
        supply[min_i] -= allocation_amount
        demand[min_j] -= allocation_amount
        if supply[min_i] == 0:
            cost[min_i] = [float('inf')] * len(demand)
        if demand[min_j] == 0:
            for row in cost:
                row[min_j] = float('inf')

    return allocation


for i in range(1, 6):
    s, d, c = read_input_file(f'input{i}.txt')
    if not is_valid_transportation_problem(s, d, c):
        print("The method is not applicable!")
        print()
        continue
    if not check_balance(s, d):
        print("The problem is not balanced!")
        print()
        continue
    print_parameter_table(s, d, c)
    print("North-West Corner Method:", *north_west_corner(s, d), sep=', ')
    print("Vogel’s Approximation Method:", *vogels_approximation(s, d, c), sep=', ')
    print("Russell's Approximation Method:", *russells_approximation(s, d, c), sep=', ')
    print()

