import cmdstanpy
'''
:description: 以下代码为解决prophet兼容性问题的一种可能解决方案 
小提示：该方法可能需要安装所在的磁盘有较多剩余空间（建议至少2G） 且需要较长的时间
'''
cmdstanpy.install_cmdstan()
cmdstanpy.install_cmdstan(compiler=True)