# 水力数字孪生仿真器 (DHALSIM)

供水系统的数字孪生系统 | 新加坡科技设计大学关键基础设施系统实验室、代尔夫特理工大学水管理系、CISPA 和 iTrust 联合开发

DHALSIM 使用 WNTR 的 EPANET 包装器对供水系统进行建模与仿真。此外，DHALSIM 结合 Mininet 和 MiniCPS 模拟工业控制系统（包含PLC、SCADA服务器等网络设备和工控设备），从而不仅支持物理数据仿真，还可提供完整的网络流量抓包（包括工控协议通信）。

该系统曾在 ACSAC'20 的 ICSS 工作会议上发表论文：

《高保真网络-物理联合仿真：供水系统的网络安全实验》

[Co-Simulating Physical Processes and Network Data for High-Fidelity Cyber-Security Experiments](https://doi.org/10.1145/3442144.3442147)

两篇详细阐述 DHALSIM 架构、功能与能力的期刊论文发表于《水资源规划与管理杂志》：

1. 高保真网络-物理仿真 I：模型与数据
   
   [High-fidelity cyber and physical simulation of water distribution systems. I: Models and Data](https://doi.org/10.1061/JWRMD5.WRENG-5853)

2. 高保真网络-物理仿真 II：网络攻击定位方法
   
   [High-fidelity cyber and physical simulation of water distribution systems. II: Enabling cyber-physical attack localization](https://doi.org/10.1061/JWRMD5.WRENG-5854)

## 安装

为简化安装流程，我们提供了适用于 Ubuntu 20.04 的一键安装脚本。该脚本位于仓库根目录，可通过以下命令运行：

```./install.sh```

## 运行

使用以下命令启动 DHALSIM：

```sudo dhalsim path/to/config.yaml```

将 < > 中的内容替换为示例拓扑文件路径或自定义配置文件路径。例如运行 anytown 示例时：

```sudo dhalsim <examples/anytown_topology/anytown_config.yaml>```

建议学习者在使用时：

- 在本地复现 anytown 示例验证安装

- 通过修改 config.yaml 参数理解仿真器配置逻辑

- 结合论文阅读理解多物理域联合仿真机制
