# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:45:31 2017

@author: Tmn07
"""
import _winreg

class Manager(object):
	mlist = [u"桌面", u"文件夹", u"文件", u"软件（待开发）", "All", "Inkfile"]
	def __init__(self):
		pass

	def run(self):
		# while 1:
		self.mainmenu()

	def mainmenu(self):
		print u"\t\t\t右键菜单管理工具"
		# print self.mlist
		for ind, val in enumerate(self.mlist):
			print ind+1, val
		print 0, u"退出"
		c = input()

		if c == 0 or c == 4:
			print "goodbye~"
		else:
			self.secordmenu(c)

	def querystatus(self, key, subkey):
		nkey = _winreg.OpenKey(key, subkey)
		print _winreg.QueryValueEx(nkey, "Extended")
		print _winreg.QueryValueEx(nkey, "LegacyDisable")
		nkey.Close()

	def secordmenu(self, mtype):
		print u"\t\t\t%s菜单项目" % self.mlist[mtype-1]
		if mtype == 1:
			dirr = ["Directory\Background\shell"]
		elif mtype == 2:
			dirr = ["Folder\shellex\ContextMenuHandlers", "Folder\shell", "Directory\shell", "Directory\shellex\ContextMenuHandlers"]
		elif mtype == 3:
			dirr = ["*\shell", "*\shellex\ContextMenuHandlers"]
		elif mtype == 5:
			dirr = ["AllFilesystemObjects\shell", "AllFilesystemObjects\shellex\ContextMenuHandlers"]
		elif mtype == 6:
			dirr = ["lnkfile\shellex\ContextMenuHandlers"]
		else:
			pass
		subkeys = []

		num = 1

		for ind, d in enumerate(dirr):
			key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, d)
			try:
				i = 0
				while 1:
					subkey = _winreg.EnumKey(key, i)
					subkeys.append(dirr[ind]+"\\"+subkey)
					# self.querystatus(key, subkey)
					print num, subkey
					i += 1
					num += 1
			except WindowsError, e:
				print u"以上是%s目录中的" % d
		print 0, u"返回"

		c = input()
		if c == 0:
			self.mainmenu()
		else:
			self.option(subkeys[c-1], mtype)
			

	def option(self, subkey, mtype):

		print u"\t\t\t操作"

		key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, subkey, 0, _winreg.KEY_ALL_ACCESS)
		print subkey.split("\\")[-1] , u"当前状态：",

		if subkey.find("shellex") == -1:
			try:
				value = _winreg.QueryValueEx(key, "Extended")
				_winreg.DeleteValue(key, "Extended")
			except Exception, e:
				pass
			else:
				print u"已隐藏"

			try:
				value = _winreg.QueryValueEx(key, "LegacyDisable")
				_winreg.DeleteValue(key, "LegacyDisable")
			except Exception, e:
				pass
			else:
				print u"已禁用"	

			print u"\n1 禁用\n2 隐藏\n3 正常\n4 删除"
			c = input()
			if c == 1:
				_winreg.SetValueEx(key, "LegacyDisable", 1, _winreg.REG_SZ, "")
				print u"已设置禁用"
			if c == 2:
				_winreg.SetValueEx(key, "Extended", 1, _winreg.REG_SZ, "")
				print u"已设置隐藏，按 `shift`+右键 可以使用"
			elif c == 4:
				print u"暂不提供删除"

		else:
			# ---- 禁用
			value = _winreg.QueryValueEx(key, "")
			if value[0].startswith("-"):
				print u"已禁用"
			else:
				print u"正常"
			print u"\n1 禁用\n2 正常\n3 删除"
			c = input()
			if c == 1:
				_winreg.SetValueEx(key, "", 1, _winreg.REG_SZ, "-"+value[0])
			elif c == 2:
				_winreg.SetValueEx(key, "", 1, _winreg.REG_SZ, value[0][value[0].find("{"):])
			elif c == 3:
				print u"暂不提供删除"

		self.secordmenu(mtype)


if __name__ == '__main__':
	m = Manager()
	m.run()