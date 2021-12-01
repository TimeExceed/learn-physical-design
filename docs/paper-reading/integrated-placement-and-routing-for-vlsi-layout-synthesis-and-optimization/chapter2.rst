Chapter 2: Placement Using Efficient 2-D Compaction
===================================================

2D Placement: The Problem
-------------------------

2D placement本质是在解下面这个方程：

..  math:: \min\sum_{i\in\text{nets}} \text{HPWL}(i)

使得对于任意两个cells :math:`i,j`，以下两个条件至少成立其一

..  math::

    \left|x_i - x_j\right| &\geqslant \frac{w_i + w_j}{2}\\
    \left|y_i - y_j\right| &\geqslant \frac{h_i + h_j}{2}

其中 :math:`(x_i,y_i)` 是cell i的中心点坐标， :math:`w_i/h_i` 是其宽度/高度，
HPWL (half-perimeter wire length) 是一个net的bounding box的半周长。
显而易见，HPWL是真实线长的下界。

..  note::

    对于是否应使用HPWL作为placement的优化目标，学术界尚有争议。
    HPWL实质是manhattan distance，而quadratic cost (后述)在优化Euclidean distance。
    Harry认为后者优化出来的结果更接近正方形，这对routing有好处。

然而“或”的部分使得问题空间在本质上非凸，因此没有高效的最优算法。

品山算法的整体框架
------------------

整体有三个大的步骤：

#.  粗放：Gauss-Seidel method on simple quadratic cost
#.  细调：考虑cell的几何形状
#.  精修：针对HPWL

在每个大步骤的结果都不能保证placement合法（即没有overlap），
所以需要用2D compaction修一修再进入下一步骤。
因此这里有四个算法要讲。

2D Compaction with RULD graph
-----------------------------

2D compaction需要解决的问题：
给定任意一个placement，拍拍紧；如果有重叠，撑撑开。

..  list-table::

    *   -   ..  image:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/compaction-1.png
                :scale: 50%
        -   ..  image:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/compaction-ruld.png
                :scale: 50%

..  note::

    一个直觉的解法：横里俄罗斯方块，竖里俄罗斯方块。
    然而不行。

    ..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/compaction-1d.png
        :scale: 50%

RULD graph的想法是在拍紧/撑开的同时保持cells之间的相对位置。
具体来说，

*   从任何一个cell(的中心)看出去，周围的cell的角顺序不变。
*   任何两个cell直观上的上下、左右关系不变。

..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/ruld-graph.png
    :align: center

*   每个cell变成一个node。后者的坐标是前者的中心。并且增加四方边界点。
*   平面被切割成许多个小三角形 (triangulation)
*   除了四方边界点之间，其他边都被赋予 **垂直** 或 **水平** 的属性。
*   每个node都有四向边(legal constraint)

核心定理：
满足以下条件的合法RULD图不会有重叠的cells。

*   explicit constraints:
    对于每一条水平边（垂直边类似）相连的两个cells :math:`i,j`，

    ..  math::

        \left|x_i-x_j\right|\geqslant\frac{w_i+w_j}{2}

*   implicit constraints (猜的):
    对于任意一条垂直边的两端 :math:`p,q`， :math:`i` 是 :math:`p` 的右节点， :math:`j` 是 :math:`q` 的左节点，则

    ..  math::

        x_i - x_j \geqslant \frac{w_i + w_j}{2}

..  note::

    证明的大致思路：
    以水平方向为例，任意两个cells，以下二者必居其一：

    *   要么他俩同处一条从左边界到右边界由水平边连成的路径上；
    *   要么他俩分处一条从上边界到下边界由垂直边连成的路径的两边。

在该定理的基础上就可以构建使任何placement合法化的算法：
在构建完RULD graph之后，抛弃所有cells的原有坐标，在explicit/implicit constraints下重建各个cells的坐标。

RULD Graph的构建
++++++++++++++++

Triangulation
^^^^^^^^^^^^^

*   随便建一个triangulation graph

    *   四方点先放好。左右连起来。
    *   每次丢进去一个节点：找到该点的包围三角形，分别连三条边。
*   每一条边横竖换一换，如果以下目标能改善，则保留。

    ..  math::

        &\min\sum_{(i,j)\in\text{edges}} X_\text{adj}^2(i,j) + Y_\text{adj}^2(i,j)
        \\
        X_\text{adj}&=\begin{cases}
            \frac{2\left|x_i-x_j\right|}{w_i+w_j}    &\text{if }\left|x_i-x_j\right|\leqslant\frac{w_i+w_j}{2}\\
            \left|x_i-x_j\right|-\frac{w_i+w_j}{2}+1    &\text{otherwise}
        \end{cases}

    ..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/edge-swapping.png
        :align: center
        :scale: 50%

        横边换竖边

..  note::

    不理解otherwise部分为什么不直接除。

Edge-direction assignment
^^^^^^^^^^^^^^^^^^^^^^^^^

#.  对于每一条边， :math:`\pm 45^\circ` 标成水平边，其他垂直边。

    *   同一个点的边按四方位（右、上、左、下）排好
    *   同一个点不可能有连续两个方位里没有边
#.  对于每一条边，在保持上述性质的条件下，考虑两端cell的大小。

    ..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/critical_slope.png
        :align: center
#.  legalization: 保证每个点的四方位都有边。
    有几个patterns，按情况套用。
    举个例子：

    ..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/ruld-legalization.png
        :align: center

2D Compaction
+++++++++++++

..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/compaction-algo.png
    :align: center

*   每次优化一个方向
*   AspectRatio: 用水平和垂直方向上的critical path的长度除出来。
*   SelectAndAdjust从一个方向上的critical path里找一条边来调整，
    使得另一个方向上的critical path增加最少。
    
    *   调整的方法只有少数几种local patterns。
        不需要每次调整都重新算一遍全局RULD。
        局部改改就行。
        因此该算法很快。
*   EvalPlacement是对placement的度量，不同的阶段不一样。

Initial placement
-----------------

优化目标：simple quadratic function

..  math::

    F=\frac{1}{2}\sum_{i,j\in\text{cells}\cup\text{pads}}c_{ij}((x_i-x_j)^2+(y_i-y_j)^2)

该目标函数是可微的。
在Gauss-Seidel method之下，每迭代的步进是

..  math::

    x_i^{(t+1)}-x_i^{(t)}&=\frac{1}{b_i}\sum_j c_{ij}(x_j^{(t)}-x_i^{(t)})\\
    b_i&=\sum_j c_{ij}

*   :math:`(x_i,y_i)` 是cell i的中心点坐标。
*   该优化函数是一种引力。
    所以如果没有IO pads，这个公式会把所有cells堆到一起去。
    所以，事先要把IO pads固定下来。
    公式里最后几个 :math:`(x_i,y_i)` 是IO pads的坐标，不能挪。
*   :math:`c_{ij}` 度量cell i和j之间的连接数。
    但为了避免multiple-pin nets的影响过大，这个系数需要调整。
    详见论文。
*   一次迭代的时间复杂度是 :math:`O(cN)` ， :math:`c` 是平均连接数， :math:`N` 是节点数。
    通常 :math:`c` 不会很大，所以基本线性。


1st refinement
--------------

细调的目标是考虑macro cells的形状。

*   macro cells的pins往往不在其中心。
    
    *   pins可以建模成距离其中心的固定偏移。
*   macro cells的旋转与翻转
    
    *   利用 quadratic function 表现出的“引力”，推动cell旋转。

..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/1st-refinement-algo.png
    :align: center
    :scale: 66%

其中CellShift算法如下图。
这里有两个改进。

..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/cell-shift-algo.png
    :align: center

*   改进1：防止过度优化浪费算力。
    根据前面展示的实验的结果，compaction的结果可能大大高于cell shifting。
    所以没必要在一轮迭代里面在illegal placement上花费太多算力。
*   改进2：第一次只移动冲击巨大的moves。
    这里“冲击巨大”的定义是：
    对于cell i和j在RULD graph里被一条水平边相连（以水平方西为例），
    且 :math:`x_i^{(t)}<x_j^{(t)}` ，则 :math:`x_i^{(t+1)}>x_j^{(t+1)}`。

    ..  note::
        
        这里的考虑是：
        如果不破坏RULD graph，那么后面的compaction往往会把cell推回原来的位置（附近）。
        但是shock moves破坏了RULD graph，每次迭代都重建一遍太费事。
        所以只在第一次迭代考虑shock moves。

CellOrient和CellShift总能改善cost，但2dCompact往往反之。
实验表明，当CellOrient和CellShift的结果和2dCompact的结果大幅收紧，再多跑的意义就不大了。

..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/quad_cost.png
    :align: center

2nd refinement
--------------

本轮的目标是把 quadratic cost 换成 HPWL。

..  figure:: ../../../pics/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/qcf-hpwl-algo.png
    :align: center

*   SwapNeighbours
    
    *   对于每个cell，在其RULD graph四跳或六跳之内再找一个cell，交换。
        如果能改善HPWL，则保留。
    *   这个操作不会改变RULD graph的结构。
*   Orientate
    
    *   对于每个cell，原地尝试其8个方向，如果能改善HPWL则保留。
    *   这个操作也不会改变RULD graph。

