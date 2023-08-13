# 用于Sphinx文档的最小化Makefile
#

# 你可以从命令行设置这些变量，也可以从环境中设置前两个变量。
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# 将其放在最前面，以便不带参数的 "make" 与 "make help" 相同。
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all 目标：将所有未知目标通过新的 "make mode" 选项路由到 Sphinx。
# $(O) 被用作 $(SPHINXOPTS) 的快捷方式。
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

