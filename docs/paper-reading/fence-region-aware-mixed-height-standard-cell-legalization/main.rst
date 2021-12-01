===========================================================================
Fence-Region-Aware Mixed-Height Standard Cell Legalization
===========================================================================

..  contents::

资源
====

*   `原始论文 <Fence-Region-AwareMixed-HeightStandardCellLegalization.pdf>`_

解决的问题
===========

多行std cell的detail placement。

步骤
========

..  figure:: ../../../pics/fence-region-aware-mixed-height-standard-cell-legalization/whole-picture.png
    :align: center

Pre-legalization
----------------

Global placement 有可能将cells放在不能放的区域。
本步骤将错放的cells推到最近的可以放的区域，不考虑overlapping。

Cell arrangement
----------------

*   对于每个cell，以global placement的结果为起点，用FRA-BFS算法找到最近合适的位置，放下。
*   实现中，先把多行cell放掉，再放单行cell。
*   FRA-BFS算法只处理有限大小的领域，所以还是有可能有些cell找不到地方放。

.. _local-cell-shifting:

Local cell shifting
-------------------

*   对于上一步骤没有放下的cell P，

    ..  list-table::
        :align: center

        *   +   ..  image:: ../../../pics/fence-region-aware-mixed-height-standard-cell-legalization/local-cell-shifting-ab.png
                    :scale: 25%
            +   ..  image:: ../../../pics/fence-region-aware-mixed-height-standard-cell-legalization/local-cell-shifting-d.png
                    :scale: 25%
        *   +   a
            +   b

    #.  看把P的一个领域（a左图）。
        把跨过边界的cells认为不可移动（a右图深色块），其他cells认为可以移动（a右图浅色块）。
    #.  把可移动块(a-f)先拿走。
    #.  把P放下。
        再依次用FRA-BFS算法把a-f放下（论文中说按大小降序排列，OpenROAD实现成随意顺序）。
        得到图b。
*   但是可能global placement在某些区域的密度太高，以至于无法在有限领域内解决。

Corner weight move
------------------

..  todo::

    没看懂。
    代码里没实现。

模拟退火
---------

以cell-move和cell-swap为手段，以总错位值最小为优化目标。

..  note::

    错位是指global placement放的位置是 :math:`P`，
    legalization之后放在 :math:`P'`。
    那么错位值是 :math:`\left|P'_x-P_x\right| + \left|P'_y-P_y\right|` 。

..  note::

    代码里没有实现。
    仅实现了随机交换。

    实现的代码也没有用起来。


Cell move
---------

在前面legalization的过程中，一个cell被放置在位置 :math:`P'`。
在固定其他cells的位置的条件下，在 :math:`P'` 的领域里重新找个位置 :math:`P''`。
如果 :math:`P''` 改进了 :math:`P'` 的错位，则替换。

..  note::

    论文里没有讲清楚进行此项优化的条件。
    查代码，是指 :math:`P''` 距离 :math:`P` 足够近。

Cell swap
---------

交换两个形状一样的cells。
因为形状一样，所以不会改变layout。
如果能减少整体的错位，就保留。

FRA-BFS算法
===========

..  code:: python
    :number-lines:

    def fra_bfs(g, c, p):
        '''
        g: 已经放了一些cells的布局图
        c: 准备放下的cell
        p: 开始搜索的位置
        '''
        a = [] # 可以放下c的位置
        s = INIT_WINDOW_SIZE
        while True:
            if s超过阈值:
                return None
            h = 从g构造以p为中心s为范围的窗口
            for t in h内可以放置c的位置:
                a.append(t)
            if len(a) > 0:
                return a中距离p最近的位置t
            增大s

*   从G构造H的方法如 :ref:`local-cell-shifting` 之图a。
*   由于s一点一点增大，实际的效果就是由近及远一圈一圈找合适的位置。

    ..  note::

        代码里s是hard code的3。
*   把s的阈值去掉，可以处理全图。

评述
====

密度对算法的影响体现在两个方面。

速度的方面

    如果密度不太高，那么在小领域就能把目标cell放下。
    算法很快就能结束。
    并且可以并行处理多个待放的cell，只要它们的领域不重叠。

效果的方面

    如果密度高，那么随机涨落之下，有些区域就是不足以放下所有global placement丢进去的cells。

    *   论文说用 corner weight move 来解决。
        一来没看懂，二来没代码。
        不知道怎么搞。
    *   把FRA-BFS中s的阈值去掉，一个迭代内轮流使用cell arrangement和local cell shifting可以处理全图。
        但这样有可能把一个cell推到非常远的位置。
        想象一下两种做法：

        #.  把一个cell丢到很远，其他cell待在原地。
        #.  把cells一圈一圈往外推。

        很难绝对地说何者更优。
        直观上似乎后者适应更多的designs。
    *   直觉上，论文quality refinement并不能把前者修成后者。
