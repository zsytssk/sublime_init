import sublime_plugin
import os
import subprocess
from .SideBarAPI import SideBarItem, SideBarSelection

class openTerminalHere(sublime_plugin.WindowCommand):
	def run(self, paths = []):
		for item in SideBarSelection(paths).getSelectedItemsWithoutChildItems():
			path = item.path().replace("\\","/")
			subprocess.Popen("D:\zsytssk\other\software\ConEmu\ConEmu.exe /dir " + path)

class showInExplorer(sublime_plugin.WindowCommand):
	def run(self, paths = []):
		for item in SideBarSelection(paths).getSelectedItemsWithoutChildItems():
			path = item.path().replace("\\","/")
			if os.path.isfile(path):
				item_path = os.path.dirname(item.path())
				item_file = os.path.basename(item.path())
				self.window.run_command('open_dir', { "dir": item_path, "file": item_file})
			else:
				self.window.run_command("open_dir", {"dir": path})
