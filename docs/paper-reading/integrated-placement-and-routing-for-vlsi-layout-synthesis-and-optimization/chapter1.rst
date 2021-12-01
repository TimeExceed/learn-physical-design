Chapter 1: Introduction
=======================

核心问题：

*   非常多的cells (e.g., :math:`10^{10}`)
*   route尽可能短的线/塞进非常小的面积
*   算法尽可能地快

业界通行的“习俗”是将元器件封装成若干高度相同的standard cells
（今天也有2倍、3倍高度的std cells），
然后一行一行排列std cells。

..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/stdcell_row.png
    :align: center
    
    std cells排成行

..  note::

    *   品山认为该做法是为了降低算法复杂度。
    *   Archer认为主要是为了PDN (power distribution network)走线方便。

但是除了统一高度的std cells，还有大小不一的macro cells。
硬将macro cells也一行一行排列则过于浪费空间。

..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/macro_cells_placement.png

因此需要真正的2D placement algorithm。

..  note::

    品山所说的placement涵盖了今天的floorplaning+global placement+detail placement。
