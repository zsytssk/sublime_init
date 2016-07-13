import sublime, sublime_plugin
import sys, os, webbrowser, platform, threading
from .SideBarAPI import SideBarItem, SideBarSelection
import socket
import re
import subprocess

class zsyTest(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		file = os.path.basename(view.file_name())
		sel0 = view.sel()[0]
		rowcol = view.rowcol(sel0.begin())
		keyword = view.substr(sel0)
		rowcol = view.rowcol(sel0.begin())
		keyword = view.substr(sel0)
		pos = str(rowcol[0] + 1) + ':' + str(rowcol[1] + 1)
		print(pos)
		arr_box = []

		def analysisStructure(viewItem):
			# 如果能够按照换行来分析整个文件就好多了
			# 如果都是正规换行的, 我就可以分析原来整个文件了
			# [{file_name: ,region: ,keyword_list: [{keyword_name: ,keyword_region: ,targetPos: , }, ...]}, ...]
			arr_box = []
			file_regions = viewItem.find_all(r"## (\S+)", 0)
			keyword_regions = viewItem.find_all(r"\S+\[(\d+\:\d+)\]")
			for i, region in enumerate(file_regions):
				line = viewItem.line(region.begin())
				find_name = re.search(r"## (\S+)", viewItem.substr(line)).group(1)
				item_box = {}
				if i == len(file_regions) - 1:
					item_box['region'] = sublime.Region(region.begin(), viewItem.size())
				else:
					item_box['region'] = sublime.Region(region.begin(), file_regions[i+1].begin()-1)

				item_box['keyword_list'] = []
				for kr in keyword_regions:
					keyItem = {}
					if kr.begin() > item_box['region'].begin() and kr.end() < item_box['region'].end():
						keywordStr = re.search(r"(\S+)\[(\d+\:\d+)\]", viewItem.substr(kr))
						keyItem['keyword_name'] = keywordStr.group(1)
						keyItem['target_pos'] = keywordStr.group(2)
						keyItem['keyword_region'] = kr
						item_box['keyword_list'].append(keyItem);
				item_box['file_name'] = find_name
				arr_box.append(item_box)
			return arr_box

		def updateKeyword(viewItem):
			for item_box in arr_box:
				if item_box['file_name'] == file:
					keyword_list = item_box['keyword_list']
					for keyword_item in keyword_list:
						if keyword_item['keyword_name'] == keyword:
							if keyword_item['target_pos'] != pos:
								print(keyword  + '[' +  pos + ']', keyword_item['keyword_region'])
								viewItem.replace(edit, keyword_item['keyword_region'], keyword  + '[' +  pos + ']')

		for viewItem in view.window().views():
			view_file = viewItem.file_name()
			if view_file and os.path.basename(view_file) == 'structure.txt':
				arr_box = analysisStructure(viewItem)
				updateKeyword(viewItem)




# entity.name.type.class'
# entity.name.function

# view
# 	extract_scope(point)
# print(curPos, view.extract_scope(curPos), view.scope_name(curPos))
# 	scope_name(point)
# 	score_selector(point, selector)
# 可以用scope一级一级的列举
# 我先就update的把