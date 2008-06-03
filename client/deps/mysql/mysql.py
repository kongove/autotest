#!/usr/bin/python
from common.check_version import check_python_version
check_python_version()

import os
from autotest_lib.client.common_lib import utils
from autotest_lib.client.bin import autotest_utils

version = 3

def setup(tarball, topdir): 
	srcdir = os.path.join(topdir, 'src')
	if not os.path.exists(tarball):
		utils.get_file('http://mirror.x10.com/mirror/mysql/Downloads/MySQL-5.0/mysql-5.0.45.tar.gz', tarball)
	autotest_utils.extract_tarball_to_dir(tarball, 'src')
	os.chdir(srcdir)
	utils.system ('./configure --prefix=%s/mysql --enable-thread-safe-client' \
			% topdir)
	utils.system('make -j %d' % count_cpus())
	utils.system('make install')

	#
	# MySQL doesn't create this directory on it's own.  
	# This is where database logs and files are created.
	#
	try:
		os.mkdir(topdir + '/mysql/var')
	except:
		pass
	#
	# Initialize the database.
	#
	utils.system('%s/mysql/bin/mysql_install_db' % topdir)
	
	os.chdir(topdir)
	
pwd = os.getcwd()
tarball = os.path.join(pwd, 'mysql-5.0.45.tar.gz')
utils.update_version(pwd+'/src', False, version, setup, tarball, pwd)
