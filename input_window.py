#!/usr/bin/python

import Tkinter
from Tkinter import Entry, RIDGE, NSEW, END
import tkMessageBox
import sys
from nash_calc import NashCalc

top = Tkinter.Tk()
top.title('Nash Equilibrium Calculator')


def convert_matrix(matrix):
    p1_payoff_matrix = []
    p2_payoff_matrix = []
    m_payoff_matrix = []
    for row in matrix:
        p1_row_arr = []
        p2_row_arr = []
        m_row_arr = []
        for col in row:
            p1_row_arr.append(int(col.get().split(",")[0]))
            p2_row_arr.append(int(col.get().split(",")[1]))
            m_row_arr.append([int(payoff) for payoff in col.get().split(",")])
        p1_payoff_matrix.append(p1_row_arr)
        p2_payoff_matrix.append(p2_row_arr)
        m_payoff_matrix.append(m_row_arr)
    return p1_payoff_matrix, p2_payoff_matrix, m_payoff_matrix


def nash_calc(matrix):
    p1_payoff_matrix, p2_payoff_matrix, m_payoff_matrix = convert_matrix(matrix)
    nc = NashCalc(p1_payoff_matrix, p2_payoff_matrix, m_payoff_matrix)
    for arg in sys.argv:
        if arg == "-pure":
            tkMessageBox.showinfo("Pure Strategies", nc.compute_pure_strategies())
        if arg == "-mixed":
            tkMessageBox.showinfo("Mixed Strategies", nc.compute_mixed_strategies())


def usage():
    raise ValueError("Usage: num_of_rows num_of_cols -pure / -mixed")


while len(sys.argv) != 4:
    usage()

rows = []
e = None
n_rows = int(sys.argv[1])
n_cols = int(sys.argv[2])
for i in range(n_rows):
    cols = []
    for j in range(n_cols):
        top = Entry(relief=RIDGE)
        top.grid(row=i, column=j, sticky=NSEW)
        top.insert(END, 0)
        cols.append(top)
    rows.append(cols)

b = Tkinter.Button(text="Generate", command=lambda: nash_calc(rows))
b.grid(row=n_rows, column=n_cols)

top.mainloop()

