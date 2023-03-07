# -*- coding: UTF-8 -*-
# Part of wordCount add-on
# Module for dialogs
# written by Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
from .update import *
from .variables import *
# Necessary For translation process
addonHandler.initTranslation()


class WordListDialog(wx.Dialog):
	# A dialog  to insert words from a list.
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Title of the dialog showing the list of words
		self.SetTitle(_("Words and its occurrences"))
		loadWords()
		from .variables import wdsList

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		# Translators: Ordering options
		self.radio_box_1 = wx.RadioBox(self, wx.ID_ANY, _("Order by:"), choices=[_("Alphabetically"), _("By number of occurences")], majorDimension=2) 
		self.radio_box_1.SetSelection(config.conf[ourAddon.name]["order"])
		sizer_1.Add(self.radio_box_1, 0, 0, 0)

		# Translators: Button to reorder the list
		self.button_0 = wx.Button(self, wx.ID_ANY, _("&Reorder"))
		sizer_1.Add(self.button_0, 0, 0, 0)
		self.button_0.Hide()

		self.list_box_1 = wx.ListBox(self, wx.ID_ANY, choices= wdsList, style=wx.LB_SINGLE)
		self.list_box_1.SetMinSize((800, 500))
		self.list_box_1.SetFocus()
		self.list_box_1.SetSelection(0)
		sizer_1.Add(self.list_box_1, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		# Translators: Name of button to show the list of lines containing the selected word
		self.button_1 = wx.Button(self, wx.ID_ANY, _("&Show occurrences"))
		self.button_1.SetDefault()
		sizer_2.Add(self.button_1, 0, 0, 0)

		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetEscapeId(self.button_CLOSE.GetId())
		self.Bind(wx.EVT_RADIOBOX, self.reload, self.radio_box_1)
		self.Bind(wx.EVT_BUTTON, self.reload1, self.button_0)
		self.Bind(wx.EVT_BUTTON, self.onOkButton, self.button_1)

		self.Layout()
		self.CentreOnScreen()

	def reload(self, event):
		event.Skip()
		config.conf[ourAddon.name]["order"] = self.radio_box_1.GetSelection()
		self.button_0.Show()

	def reload1(self, event):
		self.Destroy()
		gui.mainFrame._popupSettingsDialog(WordListDialog)

	def onOkButton(self, event):
		from .variables import wdsList
		index = self.list_box_1.GetSelection()
		global ourWord
		ourWord = str(wdsList[index])
		x = ourWord.index(",")
		ourWord = ourWord[:x]
		self.Destroy()
		gui.mainFrame._popupSettingsDialog(showOccursDialog)
		return ourWord

	def Destroy(self):
		super(WordListDialog, self).Destroy()


class showOccursDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Name of dialog showing the list of lines containing the selected word
		self.SetTitle(_("Lines containing our word"))
		loadLines()
		from .variables import lns1

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		self.windowsListBox = wx.ListBox(self, wx.ID_ANY, choices = lns1)
		sizer_1.Add(self.windowsListBox, 0, 0, 0)
		if self.windowsListBox.GetCount():
			self.windowsListBox.SetSelection(0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_OK = wx.Button(self, wx.ID_OK, "")
		self.button_OK.SetDefault()
		sizer_2.AddButton(self.button_OK)

		self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
		sizer_2.AddButton(self.button_CLOSE)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_OK.GetId())
		self.SetEscapeId(self.button_CLOSE.GetId())

		self.Layout()
		self.CentreOnScreen()
