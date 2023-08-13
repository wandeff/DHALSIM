攻击
====

DHALSIM支持设备攻击和网络攻击。本章将解释这些攻击的配置。

如果您想将攻击放在单独的文件中，请参见章节 :ref:`将攻击放在单独的文件中`。

设备攻击
--------

设备攻击是在PLC本身上执行的攻击。可以将其想象为攻击者对受攻击的PLC具有物理访问权限时执行的攻击。

示例：

.. code-block:: yaml

   device_attacks:
     - name: "Close_PRAW1_from_iteration_5_to_10"
       trigger:
         type: time
         start: 5
         end: 10
       actuator: P_RAW1
       command: closed

以下各节将解释不同的配置参数。

name
~~~~
*此选项为必填*

这定义了攻击的名称。它不能包含空格。

trigger
~~~~~~~~
*此选项为必填*

此参数定义何时触发攻击。有4种不同类型的触发器：

* Timed attacks
    * :code:`time` - 这是一个定时攻击。这意味着攻击将在给定迭代开始并在给定迭代结束时开始
* Sensor attacks：这些是当水网中某个传感器满足特定条件时将被触发的攻击。
    * :code:`below` - 这将在特定标签低于或等于给定值时触发攻击
    * :code:`above` - 这将在特定标签高于或等于给定值时触发攻击
    * :code:`between` - 这将确保在特定标签在两个给定值之间或等于这两个值之间时执行攻击

根据触发器类型，以下是所需的参数：

* 对于 :code:`time` attacks：
    * :code:`start` - 攻击的开始时间（以迭代为单位）。
    * :code:`end` - 攻击的结束时间（以迭代为单位）。
* 对于 :code:`below` 和 :code:`above` attacks：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`value` - 触发攻击所需达到的值。
* 对于 :code:`between` attacks：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`lower_value` - 下限值。
    * :code:`upper_value` - 上限值。

actuator
~~~~~~~~~
*此选项为必填*

此参数定义要在 :code:`actuator` 上执行的 :code:`command`。

command
~~~~~~~
*此选项为必填*

此参数定义要在提供的 :code:`actuator` 上执行的命令。有两个可能的命令：

* :code:`open` - 打开执行器
* :code:`closed` - 关闭执行器

示例
~~~~~~~~

以下是一个攻击YAML文件中 :code:`device_attacks` 部分的示例：

.. code-block:: yaml

    device_attacks:
      - name: "Close_PRAW_from_iteration_5_to_10"
       trigger:
         type: time
         start: 5
         end: 10
       actuator: P_RAW1
       command: closed
      - name: "Close_PRAW1_when_T2_<_0.16"
       trigger:
         type: below
         sensor: T2
         value: 0.16
       actuators: P_RAW1
       command: closed
      - name: "Close_PRAW1_when_0.10_<_T2_<_0.16"
       trigger:
         type: between
         sensor: T2
         lower_value: 0.10
         upper_value: 0.16
       actuators: P_RAW1
       command: closed

网络攻击
--------------

网络攻击是向mininet网络拓扑添加新节点的攻击。这个节点是一个“攻击者”，可以对网络进行各种攻击。主要有两种类型的网络攻击：中间人攻击（MiTM）和拒绝服务攻击（DoS）。

中间人攻击的多种类型：
* 超级简单的中间人攻击：这是最简单的攻击，它将操纵通过网络链路传递的所有CIP数据包，而不考虑包含的标签（传感器/执行器的值）。
* 中间人攻击：此攻击允许用户配置要操纵的标签列表。攻击者不会操纵未在列表中的标签通过的数据包。
* 服务器中间人攻击：此攻击使攻击者启动一个CIP服务器，然后使用该服务器为目标提供服务。它将在攻击者和受害者之间创建新的TCP连接和ENIP会话。
* 隐蔽中间人攻击：此攻击区分去往PLC和去往SCADA服务器的流量。对于PLC，它将使用攻击值操纵标签值。对于SCADA，它将使用隐蔽值操纵标签值。

这些在以下各节中有解释。

Naive Man-in-the-middle Attack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Naive中间人攻击是攻击者会位于PLC和其连接的交换机之间。攻击者会修改CIP数据包中所有标签的值，从而操纵其他PLC的数据。

.. figure:: static/simple_topo_attack.svg
    :align: center
    :alt: 带有攻击者的简单拓扑
    :figclass: align-center
    :width: 50%

    带有攻击者的简单拓扑

.. figure:: static/complex_topo_attack.svg
    :align: center
    :alt: 带有攻击者的复杂拓扑
    :figclass: align-center
    :width: 50%

    带有攻击者的复杂拓扑

以下是 :code:`naive_mitm` 攻击定义的示例：

.. code-block:: yaml

   network_attacks:
     name: "test1"
     type: naive_mitm
     trigger:
       type: time
       start: 5
       end: 10
     value: 0.2
     target: PLC1
     direction: destination

以下各节将解释配置参数。

name
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了攻击的名称。它还用作mininet网络上攻击者节点的名称。
名称只能包含字符 :code:`a-z`、:code:`A-Z`、:code:`0-9` 和 :code:`_`。并且必须在1到10个字符之间。

type
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了网络攻击的类型。对于Naive中间人攻击，应为 :code:`naive_mitm`。

trigger
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

此参数定义何时触发攻击。有4种不同类型的触发器：

* Timed attacks
    * :code:`time` - 这是一个定时攻击。这意味着攻击将在给定迭代开始并在给定迭代结束时开始
* Sensor attacks：这些是当水网中某个传感器满足特定条件时将被触发的攻击。
    * :code:`below` - 这将在特定标签低于或等于给定值时触发攻击
    * :code:`above` - 这将在特定标签高于或等于给定值时触发攻击
    * :code:`between` - 这将确保在特定标签在两个给定值之间或等于这两个值之间时执行攻击

根据触发器类型，以下是所需的参数：

* 对于 :code:`time` attacks：
    * :code:`start` - 攻击的开始时间（以迭代为单位）。
    * :code:`end` - 攻击的结束时间（以迭代为单位）。
* 对于 :code:`below` 和 :code:`above` attacks：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`value` - 触发攻击所需达到的值。
* 对于 :code:`between` attacks：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`lower_value` - 下限值。
    * :code:`upper_value` - 上限值。

value/offset
^^^^^^^^^^^^^^^^
*这两个选项中有一个为必填*

如果要用绝对值覆盖所有内容，使用 :code:`value` 选项，并将其设置为所需的值。
如果要用相对值覆盖所有内容，使用 :code:`offset` 选项，并将其设置为所需的偏移量。

target
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这将定义网络攻击的目标。对于MITM攻击，这是攻击者将位于的PLC。

direction
^^^^^^^^^^^^^^^^^^^^^^^^^
*这是一个可选参数*

这将定义我们发起MITM攻击的通信方向。如果目标是消息的"source"或"destination"，则消息可以被拦截。此参数的有效值为"source"和"destination"，默认值为"source"。

Man-in-the-middle Attack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
中间人攻击是攻击者会位于PLC和其连接的交换机之间。攻击者会解析CIP数据包，如果它们在配置的目标列表中，它将修改标签的值以操纵其他PLC的数据。

.. figure:: static/simple_topo_attack.svg
    :align: center
    :alt: 带有攻击者的简单拓扑
    :figclass: align-center
    :width: 50%

    带有攻击者的简单拓扑

.. figure:: static/complex_topo_attack.svg
    :align: center
    :alt: 带有攻击者的复杂拓扑
    :figclass: align-center
    :width: 50%

    带有攻击者的复杂拓扑

以下是 :code:`mitm` 攻击定义的示例：

.. code-block:: yaml

   network_attacks:
     name: "test1"
     type: mitm
     trigger:
       type: time
       start: 5
       end: 10
     value: 0.2
     target: PLC1
     direction: destination

以下各节将解释配置参数。

name
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了攻击的名称。它还用作mininet网络上攻击者节点的名称。
名称只能包含字符 :code:`a-z`、:code:`A-Z`、:code:`0-9` 和 :code:`_`。并且必须在1到10个字符之间。

type
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了网络攻击的类型。对于中间人攻击，应为 :code:`mitm`。

trigger
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

此参数定义何时触发攻击。有4种不同类型的触发器：

* Timed attacks
    * :code:`time` - 这是一个定时攻击。这意味着攻击将在给定迭代开始并在给定迭代结束时开始
* Sensor attacks：这些是当水网中某个传感器满足特定条件时将被触发的攻击。
    * :code:`below` - 这将在特定标签低于或等于给定值时触发攻击
    * :code:`above` - 这将在特定标签高于或等于给定值时触发攻击
    * :code:`between` - 这将确保在特定标签在两个给定值之间或等于这两个值之间时执行攻击

根据触发器类型，以下是所需的参数：

* 对于 :code:`time` attacks：
    * :code:`start` - 攻击的开始时间（以迭代为单位）。
    * :code:`end` - 攻击的结束时间（以迭代为单位）。
* 对于 :code:`below` 和 :code:`above` attacks：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`value` - 触发攻击所需达到的值。
* 对于 :code:`between` attacks：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`lower_value` - 下限值。
    * :code:`upper_value` - 上限值。

value/offset
^^^^^^^^^^^^^^^^
*这两个选项中有一个为必填*

如果要用绝对值覆盖所有内容，使用 :code:`value` 选项，并将其设置为所需的值。
如果要用相对值覆盖所有内容，使用 :code:`offset` 选项，并将其设置为所需的偏移量。

direction
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这将定义网络攻击的目标。对于MITM攻击，这是攻击者将位于的PLC。

tag
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了在MITM攻击中将被欺骗的标签。它包含一个"元组"列表，定义标签及其相应的值或偏移量。

例如，要覆盖T1的值：

.. code-block:: yaml

   tags:
     - tag: T1
       value: 0.12

或者，要偏移T1的值：

.. code-block:: yaml

   tags:
     - tag: T1
       offset: -0.2

Server Man-in-the-middle Attack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
服务器中间人攻击是攻击者会位于PLC和其连接的交换机之间。攻击者会解析CIP数据包，并使用CIP服务器的值进行修改。

.. figure:: static/simple_topo_attack.svg
    :align: center
    :alt: 带有攻击者的简单拓扑
    :figclass: align-center
    :width: 50%

    带有攻击者的简单拓扑

.. figure:: static/complex_topo_attack.svg
    :align: center
    :alt: 带有攻击者的复杂拓扑
    :figclass: align-center
    :width: 50%

    带有攻击者的复杂拓扑

以下是 :code:`server_mitm` 攻击定义的示例：

.. code-block:: yaml

   network_attacks:
     - name: attack1
       type: server_mitm
       trigger:
         type: time
         start: 5
         end: 10
       tags:
         - tag: T0
           value: 0.1
         - tag: T2
           value: 0.2
       target: PLC1

以下各节将解释配置参数。

name
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了攻击的名称。它还用作mininet网络上攻击者节点的名称。
名称只能包含字符 :code:`a-z`、:code:`A-Z`、:code:`0-9` 和 :code:`_`。并且必须在1到10个字符之间。

type
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了网络攻击的类型。对于服务器中间人攻击，应为 :code:`server_mitm`。

trigger
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

此参数定义何时触发攻击。有4种不同类型的触发器：

* Timed attacks
    * :code:`time` - 这是一个定时攻击。这意味着攻击将在给定迭代开始并在给定迭代结束时开始
* Sensor attacks：这些是当水网中某个传感器满足特定条件时将被触发的攻击。
    * :code:`below` - 这将在特定标签低于或等于给定值时触发攻击
    * :code:`above` - 这将在特定标签高于或等于给定值时触发攻击
    * :code:`between` - 这将确保在特定标签在两个给定值之间或等于这两个值之间时执行攻击

根据触发器类型，以下是所需的参数：

* 对于 :code:`time` 攻击：
    * :code:`start` - 攻击的开始时间（以迭代为单位）。
    * :code:`end` - 攻击的结束时间（以迭代为单位）。
* 对于 :code:`below` 和 :code:`above` 攻击：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`value` - 触发攻击所需达到的值。
* 对于 :code:`between` 攻击：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`lower_value` - 下限值。
    * :code:`upper_value` - 上限值。

value/offset
^^^^^^^^^^^^^^^^
*这两个选项中有一个为必填*

如果要用绝对值覆盖所有内容，使用 :code:`value` 选项，并将其设置为所需的值。
如果要用相对值覆盖所有内容，使用 :code:`offset` 选项，并将其设置为所需的偏移量。

tags
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了在MITM攻击中将被欺骗的标签。它包含一个"元组"列表，定义标签及其相应的值或偏移量。

例如，要覆盖T1的值：

.. code-block:: yaml

   tags:
     - tag: T1
       value: 0.12

或者，要偏移T1的值：

.. code-block:: yaml

   tags:
     - tag: T1
       offset: -0.2

target
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这将定义网络攻击的目标。对于服务器MITM攻击，这是攻击者将位于的PLC。


Concealment Man-in-the-middle Attack
~~~~~~~~~~~~~~~~~~~~~~~~~~
隐蔽中间人攻击是一种高级中间人攻击。攻击者会位于PLC和其连接的交换机之间，但会区分去往PLC和去往SCADA服务器的流量。对于PLC，攻击者会操纵标签值。对于SCADA，攻击者会操纵传感器值。

以下是 :code:`concealment_mitm` 攻击定义的示例：

.. code-block:: yaml

   network_attacks:
     name: "test1"
     type: concealment_mitm
     trigger:
       type: time
       start: 5
       end: 10
     value: 0.2
     target: PLC1
     direction: destination
     tags:
       - tag: T1
         value: 0.25
     concealment_data:
      type: value
      concealment_value:
        - tag: T3
          value: 42.0
        - tag: T4
          value: 84.0

以下各节将解释配置参数。

name
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了攻击的名称。它还用作mininet网络上攻击者节点的名称。
名称只能包含字符 :code:`a-z`、:code:`A-Z`、:code:`0-9` 和 :code:`_`。并且必须在1到10个字符之间。

type
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了网络攻击的类型。对于隐蔽中间人攻击，应为 :code:`concealment_mitm`。

trigger
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

此参数定义何时触发攻击。有4种不同类型的触发器：

* Timed attacks
    * :code:`time` - 这是一个定时攻击。这意味着攻击将在给定迭代开始并在给定迭代结束时开始
* Sensor attacks：这些是当水网中某个传感器满足特定条件时将被触发的攻击。
    * :code:`below` - 这将在特定标签低于或等于给定值时触发攻击
    * :code:`above` - 这将在特定标签高于或等于给定值时触发攻击
    * :code:`between` - 这将确保在特定标签在两个给定值之间或等于这两个值之间时执行攻击

根据触发器类型，以下是所需的参数：

* 对于 :code:`time` 攻击：
    * :code:`start` - 攻击的开始时间（以迭代为单位）。
    * :code:`end` - 攻击的结束时间（以迭代为单位）。
* 对于 :code:`below` 和 :code:`above` 攻击：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`value` - 触发攻击所需达到的值。
* 对于 :code:`between` 攻击：
    * :code:`sensor` - 作为触发器的传感器。
    * :code:`lower_value` - 下限值。
    * :code:`upper_value` - 上限值。

value/offset
^^^^^^^^^^^^^^^^
*这两个选项中有一个为必填*

如果要用绝对值覆盖所有内容，使用 :code:`value` 选项，并将其设置为所需的值。
如果要用相对值覆盖所有内容，使用 :code:`offset` 选项，并将其设置为所需的偏移量。

target
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这将定义网络攻击的目标。对于隐蔽中间人攻击，这是攻击者将位于的PLC。

destination
^^^^^^^^^^^^^^^^^^^^^^^^^
*这是一个可选参数*

这将定义我们发起MITM攻击的通信方向。如果目标是消息的“源”或“目标”，则消息可以被拦截。此参数的有效值为“源”和“目标”，默认值为“源”。

tags
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填*

这定义了在MITM攻击中将被欺骗的标签。它包含一个"元组"列表，定义标签及其相应的值或偏移量。

例如，要覆盖T1,T2,T3的值：

.. code-block:: yaml

   tags:
     - tag: T1
       value: 0.12
     - tag: T2
       value: 0.15
     - tag: T3
       value: 0.20

或者，要偏移T1的值：

.. code-block:: yaml

   tags:
     - tag: T1
       offset: -0.12

concealment_data
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填项*

此选项配置了隐蔽类型和隐蔽的值。有两种类型的隐蔽数据可用：
* Path: 此选项用于定义一个包含每个标签的隐蔽值的 .csv 文件的路径。这个 .csv 的格式要求第一列是应用隐蔽的迭代次数，随后的列表示隐蔽值。第一行的名称必须是 "Iteration"，每个随后的列必须有标签名称。
* Value: 此选项用于在整个攻击过程中定义特定的值。这些值可以配置为绝对值或偏移值。


For example, to conceal the values of T3, T4:
  concealment_data:
    type: value
    concealment_value:
      - tag: T3
        value: 42.0
      - tag: T4
        value: 84.0
        

Simple Denial of Service Attack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
此攻击中断了包含数据的 CIP 消息在 PLC 之间的流动。此攻击首先对目标执行 ARP 欺骗攻击，然后停止转发 CIP 消息。这将导致 PLC 无法使用新的系统状态信息更新其缓存。可能导致错误的控制动作决策。

This is an example of a :code:`simple_dos` attack definition:

.. code-block:: yaml

    network_attacks:
        - name: plc1attack
          target: PLC2
          trigger:
            type: time
            start: 648
            end: 936
          type: simple_dos
          direction: source
   
The following sections will explain the configuration parameters.

name
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填项*

这定义了攻击的名称。它还用作mininet网络上攻击者节点的名称。
名称只能包含字符 :code:`a-z`、:code:`A-Z`、:code:`0-9` 和 :code:`_`。并且必须在1到10个字符之间。

trigger
^^^^^^^^^^^^^^^^^^^^^^^^^
*此选项为必填项*

This parameter defines when the attack is triggered. There are 4 different types of triggers:

* Timed attacks
    * :code:`time` - This is a timed attack. This means that the attack will start at a given iteration and stop at a given iteration
* Sensor attacks: These are attacks that will be triggered when a certain sensor in the water network meets a certain condition.
    * :code:`below` - This will make the attack trigger while a certain tag is below or equal to a given value
    * :code:`above` - This will make the attack execute while a certain tag is above or equal to a given value
    * :code:`between` - This will ensure that the attack is executed when a certain tag is between or equal to two given values

These are the required parameters per type of trigger:

* For :code:`time` attacks:
    * :code:`start` - The start time of the attack (in iterations).
    * :code:`end` - The end time of the attack (in iterations).
* For :code:`below` and :code:`above` attacks:
    * :code:`sensor` - The sensor of which the value will be used as the trigger.
    * :code:`value` - The value which has to be reached in order to trigger the attack.
* For :code:`between` attacks:
    * :code:`sensor` - The sensor of which the value will be used as the trigger.
    * :code:`lower_value` - The lower bound.
    * :code:`upper_value` - The upper bound.

target
^^^^^^^^^^^^^^^^^^^^^^^^^
*This option is required*

This will define the target of the network attack. For a MITM attack, this is the PLC at which the attacker will sit.

direction
^^^^^^^^^^^^^^^^^^^^^^^^^
*This an optional parameter*

This will define the direction of the communication that we are launching the MiTM attack. Messages can be intercepted if the target is the "source" or "destination" of the messages. The valid values for this parameter are "source" and "destionation", the default value is "source"
