安装
============

在本指南中，我们将描述如何在Ubuntu计算机上安装DHALSIM。我们提供两种安装模式，一种是自动安装，它使用一个脚本来安装所有的依赖项。如果自动安装无法完成，还提供了手动安装的步骤。

Ubuntu版本
~~~~~~~~~~~~~~~~~~~~~~~~
DHALSIM已经在Ubuntu 20.04 LTS上开发和测试。因此，我们建议在Ubuntu 20.04上安装和运行DHALSIM。可以使用 ``./install.sh`` 运行安装脚本。安装脚本没有在其他版本上进行测试过。如果您想使用其他版本，我们建议进行手动安装。

安装脚本还可以安装所有测试和文档依赖项。要做到这一点，只需运行带有 `-t` 选项用于测试或 `-d` 选项用于文档的 ``./install.sh``，例如 ``./install.sh -t -d``。

自动安装
----------------------
克隆存储库后，您可以使用安装脚本来安装DHALSIM及其先决条件。

.. prompt:: bash $

    git clone git@github.com:afmurillo/DHALSIM.git
    cd dhalsim
    sudo chmod +x install.sh
    ./install.sh

手动安装
-------------------
对于其他Ubuntu版本，DHALSIM也可以手动安装。为此，您可以使用以下说明。

Python和pip
~~~~~~~~~~~~~~~~~~~~~~~~
DHALSIM需要Python 2，而在较新的Ubuntu版本上不再自动安装Python 2。可以使用 ``sudo apt install python2`` 来安装Python 2。您可以通过 ``curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py`` 来获取Python 2的pip，然后使用 ``sudo python2 get-pip.py``。

还需要Python 3和``python3-pip``。

Mininet和MiniCPS安装
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MiniCPS和Mininet的安装说明可以在 `这里
<https://github.com/scy-phy/minicps/blob/master/docs/userguide.rst>`_ 找到。

请注意，cpppo的安装应该替换为 ``cpppo==4.0.*``。

其他依赖项
~~~~~~~~~~~~~~~~~~~~~~
最后，DHALSIM需要pathlib和pyyaml。其他Python 3依赖项应该可以通过在DHALSIM根目录中运行 ``sudo python3 -m pip install -e .`` 来自动安装。

