==================================================================================
Almost Optimum Placement Legalization by Minimum Cost Flow and Dynamic Programming
==================================================================================

..  contents::

资源
====

*   `原始论文 <AlmostOptimumPlacementLegalizationbyMinimumCostFlowandDynamicProgramming.pdf>`_

解决的问题
==========

在单行std cell的条件下，高速地做到接近最优的detail placement。

步骤
====

..  code:: python
    :number-lines:

    assignment = assign每个cell到其中心所在的region
    while assignment is illegal:
        f = 构造图并计算最小费用最大流(assignment)
        assignment = 将f实现成cell-region assignment
    placement = 诱导(assignment)
    postoptimize(placement)

最大流图
--------

..  figure:: ../../../pics/almost-optimum-placement-legalization-by-minimum-cost-flow-and-dynamic-programming/concepts.png
    :align: center

zone
    一个zone是从blockade或边界到blockade或边界连续的一行。

region
    一个zone可以继续被切分成多个regions。
    论文里说region都是等宽的，是zone和chip-wide columns相交的方块。
    但算法里似乎并不需要这一假设。

    论文里以 :math:`A_i` 代表region i，
    其宽度为 :math:`w(A_i)`。
    :math:`C^i=\{C^i_1,\dots,C^i_k\}` 为assign给该region的所有cells，从左往右一字排开。
    其中 :math:`C^i_j` 的宽度是 :math:`w(C^i_j)`。
    并且简记 :math:`w(C^i)=\sum_j w(C^i_j)`。

..  note::

    region可以包含多个工艺要求的grids。
    这样一方面可以减少需要处理的节点数量。
    另外论文里假设任何cell最多只会和两个region有重叠（即跨过一次region-region边界）。
    
    所以，实现中需要考虑怎样确定region的宽度。
    论文里没讲怎么做。

Soft boundary feasible
    简称 **SB-feasible**。
    在一个assignment诱导的placement里，如果所有cells的中心都在其assign的region内，
    则称此assignment为SB-feasible。

Hard boundary feasible
    简称 **HB-feasible**。
    在SB-feasible的基础上额外约束所有cells不跨region的边界。

Interval
    假设一个zone内从左往右有 :math:`\{A_1,\dots,A_k\}`。
    那么其中一个Interval为 :math:`A_{\mu,\nu}=\{A_\mu,\dots,A_\nu\}`，
    其中 :math:`1\leq \mu leq \nu \leq k`。
    定义Interval的宽度 :math:`w(A_{\mu,\nu})=\sum_{\mu\leq j\leq \nu}w(A_j)`。

净负载
    假设 :math:`A` 是一个region或一个interval，
    :math:`C` 是中心点在 :math:`A` 内的所有cells，
    其中 :math:`C_1` 和 :math:`C_k` 是 :math:`A` 两头的cells。
    定义 :math:`A` 的净负载为

    ..  math::

        s(A) = w(C) - w(A) - \frac{1}{2}(w(C_1)+w(C_k))

    背后的直观是，净负载大于0意味着其中有些cells需要被挪出去，
    小于0意味着它可以接收更多的cells。

供应
    对于任意一个interval :math:`A_{\mu,\nu}`，我们定义

需求

Soft boundary minimum cost flow
    简称 **SB-MCF**。


Assignment诱导的placement
-------------------------

单行内的布局
------------

Postoptimization
----------------

下界
====

评述
====

