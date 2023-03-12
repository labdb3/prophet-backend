import cmdstanpy
'''
:description: 以下代码为解决prophet兼容性问题的一种可能解决方案
'''
cmdstanpy.install_cmdstan()
cmdstanpy.install_cmdstan(compiler=True)