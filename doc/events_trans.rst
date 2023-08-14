事件
=======

DHALSIM 支持网络事件。本章将解释这些事件的配置。

如果您想将事件放在单独的文件中，请参阅章节 :ref:`在单独的文件中的事件`。

network events
--------------

事件是由触发器启动的情况，不一定是攻击。此外，事件不需要启动额外的 Mininet 节点，也不需要使额外的 Mininet 节点与模拟交互。

示例：

.. code-block:: yaml

    network_events:
      - name: link_loss
        type: packet_loss
        target: PLC1
        trigger:
            type: time
            start: 648
            end: 792
        value: 25
        
下面的部分将解释不同的配置参数。
name
~~~~
*此选项是必需的*

这定义了事件的名称。它不能包含空格。

trigger
~~~~~~~~
*此选项是必需的*

此参数定义了何时触发事件。有4种不同类型的触发器：

* Timed events
    * :code:`time` - 这是定时事件。这意味着事件将从给定的迭代开始，到给定的迭代结束
* Sensor attacks：这些事件将在水网络中的某个特定传感器满足某个条件时触发。
    * :code:`below` - 当特定标记低于或等于给定值时，将触发此事件
    * :code:`above` - 当特定标记高于或等于给定值时，将触发此事件
    * :code:`between` - 当特定标记在两个给定值之间或等于这两个值时，将触发此事件

每种触发器类型的所需参数如下：

* 对于 :code:`time` 事件：
    * :code:`start` - 事件的开始时间（以迭代为单位）。
    * :code:`end` - 事件的结束时间（以迭代为单位）。
* 对于 :code:`below` 和 :code:`above` 事件：
    * :code:`sensor` - 将用作触发器的传感器。
    * :code:`value` - 触发事件所必须达到的值。
* 对于 :code:`between` 事件：
    * :code:`sensor` - 将用作触发器的传感器。
    * :code:`lower_value` - 下界。
    * :code:`upper_value` - 上界。

target
~~~~~~~~~
*此选项是必需的*

此参数定义将受影响的 PLC 链接。在 DHALSIM 中，PLC 仅具有一个网络链接（接口）

type
~~~~~~~
*此选项是必需的*

此参数定义网络事件的类型。目前仅支持 packet_loss

value
~~~~~~~
*此选项是必需的*
此参数定义事件期间在网络链接中将丢失的数据包百分比。

