运行
===========

要运行DHALSIM，只需输入以下命令：

.. prompt:: bash $

    sudo dhalsim path/to/config.yaml

输出
-------------
一旦模拟完成，将在 :code:`config.yaml` 中指定的位置生成各种输出文件，位于 :ref:`output_path` 下。

PCAP
~~~~~~~~~~~~~~~~
每个网络中的PLC，每个攻击者和SCADA都会生成一个 :code:`.pcap` 文件。它们的格式为 :code:`plc_name.pcap` 和 :code:`scada.pcap`。
这些文件捕获PLC和SCADA产生的网络流量，可以在诸如 `Wireshark <https://www.wireshark.org/>`_ 之类的程序中查看。

CSV
~~~~~~~~~~~~~~~~
将生成两个 :code:`.csv` 文件，一个由水模拟软件生成，一个由SCADA生成：

* :code:`ground_truth.csv` 代表模拟运行期间所有水箱、泵、执行器、阀门、攻击等的*实际*值。
* :code:`scada_values.csv` 代表SCADA在模拟期间通过网络看到的值，它将记录网络中每个属于PLC的传感器或执行器的传感器值和执行器状态。

通过区分这两者，如果发生了一个掩盖了水箱真实值的网络攻击，例如，:code:`ground_truth.csv` 将显示真实值，而 :code:`scada_values.csv` 将显示攻击者修改后的值。

配置保存
~~~~~~~~~~~~~~~~~~
为了方便起见，所有输入文件都会自动保存在配置文件中指定的 :code:`output_folder` 中。使用这些输入文件，可以在以后重新创建并运行完全相同的实验。此外，提供了一个 :code:`/configuration/general_readme.md` 文件。此文件包含关于实验的最重要信息。此外，批处理模式将在每个批处理输出文件夹中有 :code:`/configuration/batch_readme.md`。

