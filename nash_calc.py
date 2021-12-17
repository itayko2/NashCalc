#!/usr/bin/python

import numpy as np

P1 = 0
P2 = 1


class NashCalc:
    def __init__(self, p1_payoff_matrix, p2_payoff_matrix, m_payoff_matrix):
        self.p1_payoff_matrix = p1_payoff_matrix
        self.p2_payoff_matrix = p2_payoff_matrix
        self.m_payoff_matrix = m_payoff_matrix
        self.p1_row_labels = list(range(len(self.p1_payoff_matrix)))
        self.p1_col_labels = list(range(len(self.p1_payoff_matrix[0])))
        self.p2_row_labels = list(range(len(self.p2_payoff_matrix)))
        self.p2_col_labels = list(range(len(self.p2_payoff_matrix[0])))
        self.m_row_labels = list(range(len(self.m_payoff_matrix)))
        self.m_col_labels = list(range(len(self.m_payoff_matrix[0])))

    def pure_strategy_solutions(self):
        best_payoffs = {}
        row_num = len(self.p1_payoff_matrix)
        col_num = len(self.p1_payoff_matrix[0])
        p1_max_index_payoff = np.argmax(self.p1_payoff_matrix, axis=0)
        for r in range(row_num):
            best_payoffs[(r, p1_max_index_payoff[r])] = (self.p1_row_labels[r], self.p1_col_labels[p1_max_index_payoff[r]])
        best_payoff_labels = []
        p2_max_index_payoff = np.argmax(self.p2_payoff_matrix, axis=1)
        for c in range(col_num):
            if (p2_max_index_payoff[c], c) in best_payoffs:
                best_payoff_labels.append(best_payoffs[(p2_max_index_payoff[c], c)])
        return best_payoff_labels

    def remove_dominated_moves(self):
        while self.remove_dominated_p1() | self.remove_dominated_p2():
            pass

    def remove_dominated_p1(self):
        row_num = len(self.m_payoff_matrix)
        max_values = []
        max_payoff_index = [item[0] for item in np.argmax(self.m_payoff_matrix, axis=0)]
        for i in max_payoff_index:
            rows_to_keep = set()
            rows_to_keep.add(i)
            max_values.append(rows_to_keep)
        rows_to_keep = []
        while max_values:
            max_i = max_values[0].copy()
            for c in range(1, len(max_values)):
                if len(max_i & max_values[c]) != 0:
                    max_i = max_i & max_values[c]
            max_index = max_i.pop()
            rows_to_keep.append(max_index)
            max_values = [row for row in max_values if max_index not in row]

        new_m_payoff_matrix = [self.m_payoff_matrix[i] for i in sorted(rows_to_keep)]
        self.m_payoff_matrix = new_m_payoff_matrix
        self.m_row_labels = [self.m_row_labels[i] for i in sorted(rows_to_keep)]
        return row_num != len(rows_to_keep)

    def remove_dominated_p2(self):
        row_num = len(self.m_payoff_matrix)
        col_num = len(self.m_payoff_matrix[0])
        max_values = []
        max_payoff_index = [item[1] for item in np.argmax(self.m_payoff_matrix, axis=1)]
        for i in max_payoff_index:
            cols_to_keep = set()
            cols_to_keep.add(i)
            max_values.append(cols_to_keep)
        cols_to_keep = []
        while max_values:
            max_i = max_values[0].copy()
            for c in range(1, len(max_values)):
                if len(max_i & max_values[c]) != 0:
                    max_i = max_i & max_values[c]
            max_index = max_i.pop()
            cols_to_keep.append(max_index)
            max_values = [col for col in max_values if max_index not in col]

        new_m_payoff_matrix = [[] for _ in range(row_num)]
        for c in sorted(cols_to_keep):
            for r in range(row_num):
                new_m_payoff_matrix[r].append(self.m_payoff_matrix[r][c])
        self.m_payoff_matrix = new_m_payoff_matrix
        self.m_col_labels = [self.m_col_labels[i] for i in sorted(cols_to_keep)]
        return col_num != len(cols_to_keep)

    def mixed_strategy_solutions(self):
        self.remove_dominated_moves()
        p1_strategy_ratios = {}
        p2_strategy_ratios = {}
        side_len = len(self.m_payoff_matrix)
        if side_len == 1:
            p1_strategy_ratios[self.m_row_labels[0]] = 100
            p2_strategy_ratios[self.m_col_labels[0]] = 100
            return p1_strategy_ratios, p2_strategy_ratios

        p1_outcomes = [[1] * side_len]
        for c in range(1, side_len):
            p1_outcomes.append([self.m_payoff_matrix[r][c][P2] - self.m_payoff_matrix[r][0][P2] for r in range(side_len)])
        p1_solutions = np.zeros((side_len,), dtype=int)
        p1_solutions[0] += 1
        p1_outcomes = np.linalg.solve(np.array(p1_outcomes), p1_solutions)
        p1_strategy_ratios = p1_outcomes * 100

        p2_outcomes = [[1] * side_len]
        for r in range(1, side_len):
            p2_outcomes.append([self.m_payoff_matrix[r][c][P1] - self.m_payoff_matrix[0][c][P1] for c in range(side_len)])
        p2_solutions = np.zeros((side_len,), dtype=int)
        p2_solutions[0] += 1
        p2_outcomes = np.linalg.solve(np.array(p2_outcomes), p2_solutions)
        p2_strategy_ratios = p2_outcomes * 100

        return p1_strategy_ratios, p2_strategy_ratios

    def print_pure_results(self, results):
        answers = "The equilibrium points are: \n"
        for s in results:
            p1_cell = self.p1_payoff_matrix[s[P1]][s[P2]]
            p2_cell = self.p2_payoff_matrix[s[P1]][s[P2]]
            answers += str("(" + str(p1_cell) + "," + str(p2_cell) + ")" + '\n')
        if len(results) == 0:
            return "No pure strategies"
        return answers

    def print_mixed_results(self, results):
        str1 = "% of the time\n"
        answers = ""
        if len(self.m_row_labels) == 1 & len(self.m_col_labels) == 1:
            p1 = self.m_row_labels[0]
            p2 = self.m_col_labels[0]
            answers += str("Player 1 plays " + str(p1) + " " + str(results[0][p1]) + str1)
            answers += str("Player 2 plays " + str(p2) + " " + str(results[1][p2]) + str1)
        else:
            for r in range(len(self.m_row_labels)):
                answers += str("Player 1 plays " + str(self.m_row_labels[r]) + " " + str(results[0][r]) + str1)
            for c in range(len(self.m_col_labels)):
                answers += str("Player 2 plays " + str(self.m_col_labels[c]) + " " + str(results[1][c]) + str1)
        return answers

    def compute_pure_strategies(self):
        results = self.pure_strategy_solutions()
        return self.print_pure_results(results)

    def compute_mixed_strategies(self):
        results = self.mixed_strategy_solutions()
        return self.print_mixed_results(results)
