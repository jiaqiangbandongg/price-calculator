import streamlit as st
from ortools.linear_solver import pywraplp
import re
st.write("# 凑单计算器")

st.write("在输入框输入多个商品价格，用`逗号`或者`空格`隔开隔开，然后点击`计算`按钮，即可得到最佳凑单商品的价格")

prices_text = st.text_area("商品价格 例如: 15.8,57,38.5,22.8,65,355,19,28,58,88,63.1")

click = st.button("计算", type="primary")


def fun(prices):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    x = {}
    for i in range(len(prices)):
        x[i] = solver.IntVar(0, 1, "x[%i]" % i)
    solver.Add(sum(x[i]*price for i,price in enumerate(prices)) >= 600)
    solver.Minimize(solver.Sum([x[i]*price for i,price in enumerate(prices)]))
    solver.Solve()
    s = 0
    ret = []
    for i in range(len(prices)):
        if x[i].solution_value() == 1:
            ret.append(prices[i])
            s += prices[i]
    return s,ret

if click:
    prices = re.findall("\d+\.?\d+",prices_text)
    prices = list(map(float,prices))
    s,ret = fun(prices)
    st.write(f'最优价格总和:{s}')
    st.write(f'选择这些商品:{ret}')
