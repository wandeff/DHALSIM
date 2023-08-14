Configuration
=======================

要运行DHALSIM，您将需要一个配置YAML文件。在本页中，解释了每个参数。

带有所有选项的示例：

.. code-block:: yaml

    inp_file: map.inp

    plcs:
      - name: PLC1
        sensors:
          - Tank1
          - Junction5
          - Pump2F
        actuators:
          - Pump1
          - Valve1
      - name: PLC2
        sensors:
          - Tank2
          - Valve2F
        actuators:
          - Valve2

    network_topology_type: complex
    output_path: output
    iterations: 500
    mininet_cli: False
    log_level: info
    demand: pdd
    simulator: wntr
    noise_scale: 0.1
    batch_simulations: 20
    saving_interval: 2
    initial_tank_data: initial_tank.csv
    demand_patterns: demand_patterns/
    network_loss_data: losses.csv
    network_delay_data: delays.csv

    attacks:
      device_attacks:
        - name: attack1
          trigger:
            type: time
            start: 5
            end: 10
          actuator: Pump1
          command: closed

      network_attacks:
        - name: attack2
          type: mitm
          trigger:
            type: above
            sensor: Valve2F
            value: 0.16
          tags:
            - tag: Tank2
              value: 2.0
          target: PLC2
        - name: attack3
          type: naive_mitm
          trigger:
            type: between
            sensor: Tank1
            lower_value: 0.10
            upper_value: 0.16
          value: 0.5
          target: PLC1

在以下各节中，将解释每个条目。

inp_file
------------------------
*此选项为必填项*

inp文件是主要用于EPANET水模拟的文件，它存储水网络的描述以及模拟值，如持续时间；以及阀门、泵等的控制规则。

:code:`inp_file` 选项应该是要在实验中使用的inp文件的路径。
这可以是绝对路径或相对于配置文件的路径。

plcs
------------------------
*此选项为必填项*

:code:`plcs` 部分是DHALSIM的必需选项之一。它定义了网络中有哪些PLC以及这些PLC控制的传感器/执行器。:code:`plcs` 是PLC的列表。PLC的格式如下：

.. code-block:: yaml

  - name: plc_name
    sensors:
      - sensor_1
      - sensor_2
    actuators:
      - actuator_1
      - actuator_2

:code:`name`、:code:`sensors` 和 :code:`actuators` 只能包含字符 :code:`a-z`、:code:`A-Z`、:code:`0-9` 和 :code:`_`。并且长度必须在1到10个字符之间。

如果要将PLCs放在单独的文件中，请参见 :ref:`PLCs in a separate file` 部分。

sensors
~~~~~~~~~~~~
传感器可以是以下类型之一：

* 水箱水位
    * 使用 :code:`.inp` 文件中的水箱名称。
* 管道压力
    * 使用 :code:`.inp` 文件中的管道名称。
* 阀门流量
    * 使用 :code:`.inp` 文件中的阀门名称 + :code:`F`。示例： :code:`V3F`。
* 泵流量
    * 使用 :code:`.inp` 文件中的泵名称 + :code:`F`。示例： :code:`P2F`。

actuators
~~~~~~~~~~~~
执行器可以是以下类型之一：

* 阀门状态
    * 使用 :code:`.inp` 文件中的阀门名称。
* 泵状态
    * 使用 :code:`.inp` 文件中的泵名称。

network_topology_type
--------------------------------
*此选项为必填项*

此选项表示将使用的mininet网络拓扑。有两个选项，:code:`simple` 和 :code:`complex`。

如果使用 :code:`simple` 选项，那么将生成一个具有所有PLC和SCADA的网络拓扑，它们位于同一个本地网络中。
PLC连接到一个交换机，SCADA连接到另一个交换机，然后这些交换机连接到一个路由器。

.. figure:: static/simple_topo.svg
    :align: center
    :alt: 简单拓扑图
    :figclass: align-center
    :width: 50%

    简单拓扑图

如果使用 :code:`complex` 选项，那么将生成一个具有所有PLC和SCADA的独立网络拓扑。它们都有一个交换机和一个路由器，然后通过其公共IP地址连接到中央路由器。
这使得对攻击（例如中间人攻击）的测试更加逼真。

.. figure:: static/complex_topo.svg
    :align: center
    :alt: 复杂拓扑图
    :figclass: align-center
    :width: 50%

    复杂拓扑图

output_path
------------------------
*这是一个带有默认值的可选值*: :code:`output`

此选项表示用于创建输出文件（.pcap、.csv 等）的文件夹路径。
默认为 output，路径相对于配置文件。

注意：如果您以批处理模式运行，则将自动创建形式为 :code:`output_path/batch_number` 的子文件夹

iterations
------------------------
*这是一个带有默认值的可选值*: 持续时间 / 液压时间步长

iterations 值表示您希望水模拟运行多少次迭代。
一个迭代表示一个液压时间步长。

mininet_cli
------------------------
*这是一个带有默认值的可选值*: :code:`False`

如果 :code:`mininet_cli` 选项为 :code:`True`，则在网络设置完成后，将启动mininet CLI界面。
有关更多信息，请参见 `mininet CLI教程 <http://mininet.org/walkthrough/#part-3-mininet-command-line-interface-cli-commands>`_。

:code:`mininet_cli` 应为布尔值。

log_level
------------------------
*这是一个带有默认值的可选值*: :code:`info`

DHALSIM使用Python的内置 :code:`logging` 模块记录事件。通过配置文件中的 `log_level` 属性，可以更改DHALSIM应报告的事件的严重级别。接受五种不同的日志级别，每个日志级别还打印出更高优先级的日志。例如，将 `log_level` 设置为 `warning` 将把所有 `warning`、`error` 和 `critical` 语句记录到控制台。

* :code:`debug`
    * Debug是一种特殊类型的日志级别：这将打印出DHALSIM的所有调试语句，以及所有由MiniCPS和mininet打印出的日志。由于MiniCPS使用打印语句作为其日志系统，因此MiniCPS将无法使用我们的日志系统。
* :code:`info`
    * Info将DHALSIM的info语句记录到控制台。这是log_level的默认值，建议用于正常使用DHALSIM。
* :code:`warning`
* :code:`error`
* :code:`critical`
    * 严重错误是导致DHALSIM崩溃的错误。这将始终记录到控制台。

demand
------------------------
*这是一个带有默认值的可选值*: :code:`PDD`

配置文件中的 demand 选项表示WNTR模拟使用的需求模型。
有效选项为 :code:`PDD` 和 :code:`DD`。然后该值将传递给 `WNTR水力需求模型选项 <https://wntr.readthedocs.io/en/latest/hydraulics.html>`_。

simulator
------------------------
*这是一个带有默认值的可选值*: :code:`wntr`

配置文件中的 simulator 选项表示物理模拟使用的EPANET包装器。
有效选项为 :code:`wntr` 和 :code:`epynet`。WNTR是由美国环境保护局开发的Python包装器，与开发EPANET的同一团队。WNTR文档在 `WNTR网站 <https://wntr.readthedocs.io/en/latest>`_ 中可用。Epynet是由Vitens开发的Python包装器，并由 `Davide Salaorni <https://github.com/Daveonwave/DHALSIM-epynet>`_ 进行了修改。Epynet的主要特点是实现逐步模拟，与WNTR相比性能更好。

noise_scale
------------------------
*这是一个带有默认值的可选值*: :code:`0`

该参数影响传感器值添加到由PLC发送的传感器值的高斯噪声的规模。如果未设置该参数，它将默认为0。这将导致传感器值不添加噪声。

batch_simulations
------------------------
*这是一个可选值*

如果设置了 :code:`batch_simulations` 选项，那么模拟将以批处理模式运行。这意味着您可以提供带有初始水箱条件、需求模式和网络损失/延迟的 :code:`.csv` 文件，以在不同条件下运行模拟。完整的模拟将运行 :code:`batch_simulations` 次，输出将进入 :code:`output_path/batch_number` 文件夹。

注意：您提供的 :code:`.csv` 文件（除需求模式外）应至少有 :code:`batch_simulations` 行。

:code:`batch_simulations` 应为一个数字。

saving_interval
------------------------
*这是一个可选值*

当使用一个值设置了此选项时，模拟将每隔 x 次迭代保存一次 :code:`ground_truth.csv` 和 :code:`scada_values.csv` 文件，其中 x 是设置的值。

:code:`saving_interval` 应为大于0的整数。

initial_tank_data
------------------------
*这是一个可选值*

:code:`initial_tank_data` 字段提供了一个 :code:`.csv` 文件的名称，其中包含模拟的初始水箱值。每一列应该是一个水箱，行是初始值。如果在批处理模式下运行，则它将使用与模拟编号相对应的行（例如，对于模拟3，将使用索引为3的列）；如果不在批处理模式下运行，则将使用第一行（第0行）。如果您只想为某些水箱提供初始值，那么您可以这样做，其余的水箱将使用 :code:`.inp` 文件中的默认初始值。

一个示例可能是这样的：

.. csv-table:: initial_tank_data
   :header: "tank_1", "tank_2", "tank_3"
   :widths: 5, 5, 5

    1.02,2.45,3.17
    4.02,5.45,6.17
    7.02,8.45,9.17

demand_patterns
------------------------
*这是一个可选值*

:code:`demand_patterns` 字段提供了在模拟中使用的需求模式 :code:`.csv` 文件的路径。如果您不使用批处理模式，那么这只需是文件位置的路径（例如 :code:`demand_patterns: demands.csv`）。如果您正在使用批处理模式运行，则 :code:`.csv` 文件必须遵循名称约定 :code:`number.csv`，其中 :code:`number` 是要使用这些需求模式的批次号。例如，对于第一个批次，您将拥有 :code:`0.csv`，然后是 :code:`1.csv`，依此类推。并且 :code:`demand_patterns` 的值将是您的需求模式文件（例如 :code:`demand_patterns: demand_patterns/`，其中 demand_patterns 是包含 :code:`number.csv` 文件的文件夹）的 *路径*。

:code:`.csv` 文件将包含消费者名称作为标头，行中为模拟的不同需求值。

一个示例可能是这样的：

.. csv-table:: initial_demand_patterns
   :header: "Consumer01", "Consumer02"
   :widths: 10, 10

    21.02,28.45
    42.02,55.45
    17.02,18.45

network_loss_data
------------------------
*这是一个可选值*

:code:`network_loss_data` 字段提供了模拟的网络丢失值的 :code:`.csv` 文件的名称。
如果提供了 :code:`network_loss_data` 字段，则网络模拟将使用网络丢失进行运行。这意味着您可以提供带有网络丢失的 :code:`.csv` 文件，以在非完美的网络条件下进行模拟。如果您不在批处理模式下运行DHALSIM，那么使用的网络丢失将是CSV中的第一行。如果您在批处理模式下运行DHALSIM，则它将使用与水箱水平、需求模式等相同的索引（即与当前批次对应的行，因此对于批次5，将使用第5行数据）。

如果未提供 :code:`network_loss_data` 字段，则模拟将在没有网络丢失的情况下运行（0％数据包丢失）。

:code:`.csv` 文件的每一列应该是一个PLC/SCADA，行是损失值（每个值是0-100之间的百分比）。
如果要仅为某些节点提供损失，您可以这样做，其余节点将使用默认值（none）。请注意，PLC名称必须与 :code:`plcs` 部分中的名称相同，SCADA名称必须为 'scada'。

一个示例可能是这样的：

.. csv-table:: network_loss_data
   :header: "PLC1", "PLC2", "scada"
   :widths: 5, 5, 5

    0.02,0.45,0.17
    0.03,0.46,0.18
    0.04,0.47,0.19

network_delay_data
------------------------
*这是一个可选值*

:code:`network_delay_data` 字段提供了模拟的网络延迟值的 :code:`.csv` 文件的名称。
如果提供了 :code:`network_delay_data` 选项，则网络模拟将使用网络延迟进行运行。这意味着您可以提供带有网络延迟的 :code:`.csv` 文件，以在非完美的网络条件下进行模拟。如果您不在批处理模式下运行DHALSIM，那么使用的网络延迟将是CSV中的第一行。如果您在批处理模式下运行DHALSIM，则它将使用与水箱水平、需求模式等相同的索引（即与当前批次对应的行，因此对于批次5，将使用第5行数据）。

如果未提供 :code:`network_delay_data` 字段，则模拟将在没有网络延迟的情况下运行（0秒延迟）。

:code:`.csv` 文件的每一列应该是一个PLC/SCADA，行是延迟值（以秒为单位）。
如果要仅为某些节点提供延迟，您可以这样做，其余节点将使用默认值（0秒）。请注意，PLC名称必须与 :code:`plcs` 部分中的名称相同，SCADA名称必须为 'scada'。

一个示例可能是这样的：

.. csv-table:: network_delay_data
   :header: "PLC1", "PLC2", "scada"
   :widths: 5, 5, 5

    22.02,42.45,17.17
    22.03,42.46,17.18
    22.04,42.47,17.19

attacks
------------------------
*这是一个可选值*

有许多类型的攻击可用。它们在 :ref:`Attacks` 部分中进行了描述。
如果省略或注释掉此选项，则模拟将在没有攻击的情况下运行。

如果您希望将攻击放在单独的文件中，请参阅  :ref:`Attacks in a separate file` 部分。



Splitting up the config file(将配置文件分割)
==============================
如果您希望轻松地将攻击更换为其他攻击, 或者更换PLC, 你可以将配置文件拆分为多个文件。
可以使用 :code:`!include` 关键字来实现。

以下是一些示例:

PLCs in a separate file(将PLC存储在单独的文件中)
------------------------
如果您希望将 :code:`plcs` 存储在单独的yaml文件中, 可用通过使用 :code:`!include` 来实现。

配置文件中将如下所示:

.. code-block:: yaml

    plcs: !include plcs.yaml

而 :code:`plcs.yaml` 将如下所示:

.. code-block:: yaml

  - name: PLC1
    sensors:
      - Tank1
      - Junction5
      - Pump2F
    actuators:
      - Pump1
      - Valve1
  - name: PLC2
    sensors:
      - Tank2
      - Valve2F
    actuators:
      - Valve2

Attacks in a separate file(将攻击存储在单独的文件中)
----------------------------

如果您希望将 :code:`attacks` 存储在单独的yaml文件中, 可用通过使用 :code:`!include` 来实现。

配置文件中将如下所示:

.. code-block:: yaml

    attacks: !include attacks.yaml

而 :code:`attacks.yaml` 将如下所示:

.. code-block:: yaml

   device_attacks:
     - name: attack1
       trigger:
         type: time
         start: 5
         end: 10
       actuator: Pump1
       command: closed

   network_attacks:
     - name: attack2
       type: mitm
       trigger:
         type: above
         sensor: Valve2F
         value: 0.16
       tags:
         - tag: Tank2
           value: 2.0
       target: PLC2
     - name: attack3
       type: naive_mitm
       trigger:
         type: between
         sensor: Tank1
         lower_value: 0.10
         upper_value: 0.16
       value: 0.5
       target: PLC1
       direction: source
       
events
------------------------
*这是一个可选值*
事件是由触发器启动的情况，不一定是攻击。此外，事件不需要启动额外的mininet节点，也不需要额外的mininet节点与模拟交互。目前，仅支持网络事件。网络事件的逻辑由拓扑中的交换机或路由器实现。网络事件遵循与网络攻击相同的设计原则。 

目前支持的网络事件是 "packet_loss"，它使用Linux tc工具模拟丢失在链接上发送的一定百分比的数据包。如果省略或注释掉此选项，则模拟将在没有事件的情况下运行。

如果您希望将事件放在单独的文件中，请参阅 :ref:`Events in a separate file` 部分。

Events in a separate file(将事件存储在单独的文件中)
----------------------------

如果您希望将 :code:`events` 存储在单独的yaml文件中, 可用通过使用 :code:`!include` 来实现。

配置文件中将如下所示:

.. code-block:: yaml

    events: !include events.yaml

而 :code:`events.yaml` 将如下所示:

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
