#!/usr/bin/env python
# encoding: utf-8
# Created by Daniel Koehler - 04/03/2014

import platform

class FlatUI():

		def __init__(self):
				self.colours = FlatUIColours()
				self.platformsafevalue = {'Windows': {
								'admin-button-padding': (15,11),
								'entry-width': 16,
								'entry-padding': (18,10),
								'listbox-padding': (50,10),
								'admin-font': ("",8),
								'green-button-padding':[40,11],
								'add-group-entry-width': 50,
								'add-group-label-padding': [20,10],

							},'Normal': {
								'admin-button-padding': (10,10),
								'admin-font': ("",13),
								'entry-width': 12,
								'entry-padding': [9,10],
								'green-button-padding':[40,10],
								'listbox-padding': [10,10],
								'add-group-entry-width': 26,
								'add-group-label-padding': [20,10],
							},
						}
		def getPlaformSafeValue(self, key):
			if platform.system() != "Windows":
				return self.platformsafevalue['Normal'][key]  
			else:
				return  self.platformsafevalue['Windows'][key]

		def initiateWithStyle(self, style = 0):
				if style:
						self.style = style

				self.style.theme_create("FlatUI")

				self.style.theme_settings("FlatUI", {
					 "TButton": {
							 "configure": {
										"padding": [40,10],
										"width": 12, # 182px approx.
										"anchor":"CENTER"

										},
							 "map": {

									 "background": [("active", self.colours.peterRiver()),
																	("!disabled", self.colours.belizeHole())],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.clouds()),
																	("!disabled", "#FFF")]
							 }
					 },
					 "InputBorder.TFrame": {
							 "configure": {
										"padding": self.getPlaformSafeValue('listbox-padding'),
										"bd": 4,
										},
							 "map": {

									 "background": [("active", self.colours.peterRiver()),
																	("!disabled", self.colours.belizeHole())],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.clouds()),
																	("!disabled", "#FFF")]
							 }
					 },
					 "InputBorderError.TFrame": {
							 "configure": {
										"padding": [10,10],
										"bd": 4,
										},
							 "map": {

									 "background": [("active", self.colours.alizarin()),
																	("!disabled", self.colours.alizarin())],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.clouds()),
																	("!disabled", "#FFF")]
							 }
					 },
					 "Admin.TButton": {
							 "configure": {
										"padding": self.getPlaformSafeValue('admin-button-padding'),
										"width": 0,
										"anchor":"CENTER",
										"font":self.getPlaformSafeValue('admin-font')
										},
							 "map": {
									 "background": [("active", self.colours.peterRiver()),
																	("!disabled", self.colours.belizeHole())],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.clouds()),
																	("!disabled", "#FFF")]
							 }
					 },
					 "AdminGreen.TButton": {
							 "configure": {
										"padding": [10,10],
										"width": 0,
										"anchor":"CENTER"
										},
							 "map": {
									 "background": [("active", self.colours.turquoise()),
																	("!disabled", self.colours.greenSea())],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.clouds()),
																	("!disabled", "#FFF")]
							 }
					 },
					 "Wide.TButton": {
							 "configure": {
										"padding": [10,10],
										"width": 60, # 182px approx.
										"anchor":"CENTER"
										},
							 "map": {
									 "background": [("active", self.colours.peterRiver()),
																	("!disabled", self.colours.belizeHole())],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.clouds()),
																	("!disabled", "#FFF")]
							 }
					 },
					 "Green.TButton": {
							 "configure": {
										"padding": self.getPlaformSafeValue('green-button-padding'),
										"width": 12, # 182px approx.
										"anchor":"CENTER",
										"font":self.getPlaformSafeValue('admin-font')
										},
							 "map": {
									 "background": [("active", self.colours.turquoise()),
																	("!disabled", self.colours.greenSea())],
									 "cursor": [("active", "plus")],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.clouds()),
																	("!disabled", "#FFF")]
							 }
					 },
					 "Wide.Green.TButton": {
							 "configure": {
										"padding": [40,10],
										"width": 16,
										"anchor":"CENTER"
										},
							 "map": {
									 "background": [("active", self.colours.turquoise()),
																	("!disabled", self.colours.greenSea())],
									 "cursor": [("active", "plus")],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.clouds()),
																	("!disabled", "#FFF")]
							 }
					 },"InputBorder.TEntry": {
							 "configure": {
										"padding": self.getPlaformSafeValue('entry-padding'),
										"width": self.getPlaformSafeValue('entry-width'), # 182px approx.
										"anchor":"CENTER",
										"border":1,
										 "foreground": self.colours.clouds(),
										 "fieldbackground": self.colours.peterRiver()
										},
							 "map": {
									 "background": [("active", self.colours.clouds()),
																	("!disabled", self.colours.clouds())],
							 }
					 },
						 "InputBorderError.TEntry": {
							 "configure": {
										"padding": self.getPlaformSafeValue('entry-padding'),
										"width": self.getPlaformSafeValue('entry-width'), # 182px approx.
										"anchor":"CENTER",
										"border":1,
										 "foreground": self.colours.clouds(),
										 "fieldbackground": self.colours.alizarin()
										},
							 "map": {
									 "background": [("active", self.colours.clouds()),
																	("!disabled", self.colours.clouds())],
							 }
					 },
						 "GroupPopup.TEntry": {
							 "configure": {
										"padding": self.getPlaformSafeValue('entry-padding'),
										"width": self.getPlaformSafeValue('add-group-entry-width'), # 182px approx.
										"anchor":"CENTER",
										"border":0,
										 "foreground": self.colours.midnightBlue(),
										 "fieldbackground": self.colours.clouds()
										},
							 "map": {
									 "background": [("active", self.colours.clouds()),
																	("!disabled", self.colours.clouds())],
							 }
					 },
					 "GroupPopup.TLabel": {
							 "configure": {
										"padding": self.getPlaformSafeValue('add-group-label-padding'),
										"anchor":"CENTER",
										"width":20
										},
							 "map": {
									 "background": [("active", self.colours.belizeHole()),
																	("!disabled", self.colours.belizeHole())],
									 "fieldbackground": [("!disabled", self.colours.clouds())],
									 "foreground": [("focus", self.colours.clouds()),
																	("!disabled", "#FFF")]
							 }
					 },
					 "ProfileImage.TLabel": {
							 "configure": {
										"padding": [5,5],
										"anchor":"CENTER"
										},
							 "map": {
									 "background": [("active", self.colours.peterRiver()),
																	("!disabled", self.colours.belizeHole())],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.midnightBlue()),
																	("!disabled", "#FFF")]
							 }
					 },
					 "Questionnaire.TLabel": {
							 "configure": {
										"padding": [2,2],
										"anchor":"LEFT"
										},
							 "map": {
									 "background": [("active", self.colours.midnightBlue()),
																	("!disabled", self.colours.clouds())],
							 }
					 },
					 "InputBorder.TFrame": {
							"configure": {
										"padding": [2,2],
									},  
							"map": {
									 "background": [("active", self.colours.peterRiver()),
																	("!disabled", self.colours.peterRiver())],
							 }
					 },
					 "TFrame": {
							 "map": {
									 "background": [("active", self.colours.clouds()),
																	("!disabled", self.colours.clouds())],
							 }
					 },
					 "TLabel": {
					 		"configure": {
										"padding": [5,2],
										"anchor":"CENTER"
										},
							 "map": {
									 "highlightbackground": [("active", self.colours.clouds()),
																	("!disabled", self.colours.clouds())],
									 "background": [("active", self.colours.clouds()),
																	("!disabled", self.colours.clouds())],
									 "fieldbackground": [("!disabled", self.colours.midnightBlue())],
									 "foreground": [("focus", self.colours.midnightBlue()),
																	("!disabled", self.colours.midnightBlue() )]
							 }
					 },
					 "Question.Image": {
							 "map": {
									 "highlightbackground": [("active", self.colours.clouds()),
																	("!disabled", self.colours.clouds())],
							 }
					 },
					 "Question.Label": {
							 "map": {
									 "highlightbackground": [("active", self.colours.clouds()),
																	("!disabled", self.colours.clouds())],
							 }
					 }
				})

				self.style.theme_use("FlatUI")

class FlatUIColours():
		def __init__(self):
						pass
		def white(self):
				return "#FFFFFF"
		
		def cardiff(self):
				return "#d73647"
		
		def turquoise(self):
				return "#1ABC9C"

		def greenSea(self):
				return "#16A085"

		def emerland(self):
				return "#2ECC71"

		def nephritis(self):
				return "#27AE60"

		def peterRiver(self):
				return "#3498DB"

		def belizeHole(self):
				return "#2980B9"

		def amethyst(self):
				return "#9B59B6"

		def wisteria(self):
				return "#8E44AD"

		def wetAsphalt(self):
				return "#34495E"

		def midnightBlue(self):
				return "#2C3E50"

		def sunflower(self):
				return "#F1C40F"

		def tangerine(self):
				return "#F39C12"

		def carrot(self):
				return "#E67E22"

		def pumpkin(self):
				return "#D35400"

		def alizarin(self):
				return "#E74C3C"

		def pomegranate(self):
				return "#C0392B"

		def clouds(self):
				return "#ECF0F1"

		def silver(self):
				return "#BDC3C7"

		def concrete(self):
				return "#95A5A6"

		def asbestos(self):
				return "#7F8C8D"    
