RUNE_STATS={
	'ad':'Attack damage',
	'adpl':'Attack damage per level',
	'ar':'Armor',
	'arpl':'Armon per level',
	'arpen':'Armor pen.',
	'as':'Attack speed',
	'ap':'Ability power',
	'appl':'Ability power per level',
	'cdr':'Cooldown reduction',
	'cdrpl':'Cooldown reduction per level',
	'critcha':'Crit chance',
	'critdmg':'Crit damage',
	'energy':'Energy',
	'energypl':'Energy per level',
	'energyreg':'Energy regen.',
	'energyregpl':'Energy regen per level',
	'hp':'HP',
	'hppct':'HP %',
	'hppl':'HP per level',
	'hpreg':'HP regen',
	'hpregpl':'HP regen per level',
	'mana':'Mana',
	'manapl':'Mana per level',
	'manareg':'Mana regen',
	'manaregpl':'Mana regen per level',
	'mpen':'Magic pen.',
	'mr':'Magic resist',
	'mrpl':'Magic resist per level',
	'gold':'Gold/10sec.',
	'ls':'Lifesteal',
	'ms':'Movespeed',
	'res':'',
	'sv':'Spellvamp',
	'xp':'Experience gained'
}

RUNES={
	5001: {
		"name": "Lesser Mark of Strength",
		"description": "+0.53 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 0.53
		}]
	},
	5002: {
		"name": "Lesser Mark of Might",
		"description": "+0.08 attack damage per level (+1.35 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.08
		}]
	},
	5003: {
		"name": "Lesser Mark of Alacrity",
		"description": "+0.94% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 0.94
		}]
	},
	5005: {
		"name": "Lesser Mark of Furor",
		"description": "+1.24% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 1.24
		}]
	},
	5007: {
		"name": "Lesser Mark of Malice",
		"description": "+0.52% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.52
		}]
	},
	5009: {
		"name": "Lesser Mark of Desolation",
		"description": "+0.93 armor penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 0.93
		}]
	},
	5011: {
		"name": "Lesser Mark of Fortitude",
		"description": "+1.93 health",
		"effect": [{
			"stat": "hp",
			"amount": 1.93
		}]
	},
	5012: {
		"name": "Lesser Mark of Vitality",
		"description": "+0.3 health per level (+5.4 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 0.3
		}]
	},
	5013: {
		"name": "Lesser Mark of Resilience",
		"description": "+0.51 armor",
		"effect": [{
			"stat": "ar",
			"amount": 0.51
		}]
	},
	5015: {
		"name": "Lesser Mark of Warding",
		"description": "+0.54 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 0.54
		}]
	},
	5016: {
		"name": "Lesser Mark of Shielding",
		"description": "+0.04 magic resist per level (+0.72 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.04
		}]
	},
	5021: {
		"name": "Lesser Mark of Focus",
		"description": "-0.09% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.09
		}]
	},
	5023: {
		"name": "Lesser Mark of Potency",
		"description": "+0.33 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.33
		}]
	},
	5024: {
		"name": "Lesser Mark of Force",
		"description": "+0.06 ability power per level (+1.08 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.06
		}]
	},
	5025: {
		"name": "Lesser Mark of Intellect",
		"description": "+3.28 mana",
		"effect": [{
			"stat": "mana",
			"amount": 3.28
		}]
	},
	5026: {
		"name": "Lesser Mark of Knowledge",
		"description": "+0.65 mana per level (+11.7 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 0.65
		}]
	},
	5027: {
		"name": "Lesser Mark of Replenishment",
		"description": "+0.15 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.15
		}]
	},
	5029: {
		"name": "Lesser Mark of Insight",
		"description": "+0.53 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 0.53
		}]
	},
	5031: {
		"name": "Lesser Glyph of Strength",
		"description": "+0.16 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 0.16
		}]
	},
	5032: {
		"name": "Lesser Glyph of Might",
		"description": "+0.02 attack damage per level (+0.36 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.02
		}]
	},
	5033: {
		"name": "Lesser Glyph of Alacrity",
		"description": "+0.35% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 0.35
		}]
	},
	5035: {
		"name": "Lesser Glyph of Furor",
		"description": "+0.31% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 0.31
		}]
	},
	5037: {
		"name": "Lesser Glyph of Malice",
		"description": "+0.15% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.15
		}]
	},
	5041: {
		"name": "Lesser Glyph of Fortitude",
		"description": "+1.49 health",
		"effect": [{
			"stat": "hp",
			"amount": 1.49
		}]
	},
	5042: {
		"name": "Lesser Glyph of Vitality",
		"description": "+0.3 health per level (+5.4 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 0.3
		}]
	},
	5043: {
		"name": "Lesser Glyph of Resilience",
		"description": "+0.39 armor",
		"effect": [{
			"stat": "ar",
			"amount": 0.39
		}]
	},
	5045: {
		"name": "Lesser Glyph of Warding",
		"description": "+0.83 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 0.83
		}]
	},
	5046: {
		"name": "Lesser Glyph of Shielding",
		"description": "+0.08 magic resist per level (+1.44 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.08
		}]
	},
	5047: {
		"name": "Lesser Glyph of Vigor",
		"description": "+0.15 health regen / 5 sec.",
		"effect": [{
			"stat": "hpreg",
			"amount": 0.15
		}]
	},
	5051: {
		"name": "Lesser Glyph of Focus",
		"description": "-0.36% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.36
		}]
	},
	5052: {
		"name": "Lesser Glyph of Celerity",
		"description": "-0.03% cooldowns per level (-0.54% at champion level 18)",
		"effect": [{
			"stat": "cdrpl",
			"amount": 0.03
		}]
	},
	5053: {
		"name": "Lesser Glyph of Potency",
		"description": "+0.55 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.55
		}]
	},
	5054: {
		"name": "Lesser Glyph of Force",
		"description": "+0.1 ability power per level (+1.8 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.1
		}]
	},
	5055: {
		"name": "Lesser Glyph of Intellect",
		"description": "+6.25 mana",
		"effect": [{
			"stat": "mana",
			"amount": 6.25
		}]
	},
	5056: {
		"name": "Lesser Glyph of Knowledge",
		"description": "+0.79 mana per level (+14.22 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 0.79
		}]
	},
	5057: {
		"name": "Lesser Glyph of Replenishment",
		"description": "+0.17 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.17
		}]
	},
	5058: {
		"name": "Lesser Glyph of Clarity",
		"description": "+0.03 mana regen / 5 sec. per level (+0.54 at champion level 18)",
		"effect": [{
			"stat": "manaregpl",
			"amount": 0.03
		}]
	},
	5059: {
		"name": "Lesser Glyph of Insight",
		"description": "+0.32 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 0.32
		}]
	},
	5061: {
		"name": "Lesser Seal of Strength",
		"description": "+0.24 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 0.24
		}]
	},
	5062: {
		"name": "Lesser Seal of Might",
		"description": "+0.03 attack damage per level (+0.61 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.03
		}]
	},
	5063: {
		"name": "Lesser Seal of Alacrity",
		"description": "+0.42% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 0.42
		}]
	},
	5065: {
		"name": "Lesser Seal of Furor",
		"description": "+0.43% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 0.43
		}]
	},
	5067: {
		"name": "Lesser Seal of Malice",
		"description": "+0.23% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.23
		}]
	},
	5071: {
		"name": "Lesser Seal of Fortitude",
		"description": "+2.97 health",
		"effect": [{
			"stat": "hp",
			"amount": 2.97
		}]
	},
	5072: {
		"name": "Lesser Seal of Vitality",
		"description": "+0.6 health per level (+10.8 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 0.6
		}]
	},
	5073: {
		"name": "Lesser Seal of Resilience",
		"description": "+0.78 armor",
		"effect": [{
			"stat": "ar",
			"amount": 0.78
		}]
	},
	5074: {
		"name": "Lesser Seal of Defense",
		"description": "+0.08 armor per level (+1.44 at champion level 18)",
		"effect": [{
			"stat": "arpl",
			"amount": 0.08
		}]
	},
	5075: {
		"name": "Lesser Seal of Warding",
		"description": "+0.41 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 0.41
		}]
	},
	5076: {
		"name": "Lesser Seal of Shielding",
		"description": "+0.05 magic resist per level (+0.9 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.05
		}]
	},
	5077: {
		"name": "Lesser Seal of Vigor",
		"description": "+0.24 health regen / 5 sec.",
		"effect": [{
			"stat": "hpreg",
			"amount": 0.24
		}]
	},
	5078: {
		"name": "Lesser Seal of Regeneration",
		"description": "+0.06 health regen / 5 sec. per level (+1.08 at champion level 18)",
		"effect": [{
			"stat": "hpregpl",
			"amount": 0.06
		}]
	},
	5081: {
		"name": "Lesser Seal of Focus",
		"description": "-0.16% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.16
		}]
	},
	5083: {
		"name": "Lesser Seal of Potency",
		"description": "+0.33 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.33
		}]
	},
	5084: {
		"name": "Lesser Seal of Force",
		"description": "+0.06 ability power per level (+1.08 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.06
		}]
	},
	5085: {
		"name": "Lesser Seal of Intellect",
		"description": "+3.83 mana",
		"effect": [{
			"stat": "mana",
			"amount": 3.83
		}]
	},
	5086: {
		"name": "Lesser Seal of Knowledge",
		"description": "+0.65 mana per level (+11.7 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 0.65
		}]
	},
	5087: {
		"name": "Lesser Seal of Replenishment",
		"description": "+0.23 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.23
		}]
	},
	5088: {
		"name": "Lesser Seal of Clarity",
		"description": "+0.036 mana regen / 5 sec. per level (+0.65 at champion level 18)",
		"effect": [{
			"stat": "manaregpl",
			"amount": 0.036
		}]
	},
	5091: {
		"name": "Lesser Quintessence of Strength",
		"description": "+1.25 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 1.25
		}]
	},
	5092: {
		"name": "Lesser Quintessence of Might",
		"description": "+0.14 attack damage per level (+2.52 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.14
		}]
	},
	5093: {
		"name": "Lesser Quintessence of Alacrity",
		"description": "+1.89% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 1.89
		}]
	},
	5095: {
		"name": "Lesser Quintessence of Furor",
		"description": "+2.48% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 2.48
		}]
	},
	5097: {
		"name": "Lesser Quintessence of Malice",
		"description": "+1.03% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 1.03
		}]
	},
	5099: {
		"name": "Lesser Quintessence of Desolation",
		"description": "+1.85 armor penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 1.85
		}]
	},
	5101: {
		"name": "Lesser Quintessence of Fortitude",
		"description": "+14.5 health",
		"effect": [{
			"stat": "hp",
			"amount": 14.5
		}]
	},
	5102: {
		"name": "Lesser Quintessence of Vitality",
		"description": "+1.5 health per level (+27 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 1.5
		}]
	},
	5103: {
		"name": "Lesser Quintessence of Resilience",
		"description": "+2.37 armor",
		"effect": [{
			"stat": "ar",
			"amount": 2.37
		}]
	},
	5104: {
		"name": "Lesser Quintessence of Defense",
		"description": "+0.21 armor per level (+3.78 at champion level 18)",
		"effect": [{
			"stat": "arpl",
			"amount": 0.21
		}]
	},
	5105: {
		"name": "Lesser Quintessence of Warding",
		"description": "+2.5 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 2.5
		}]
	},
	5106: {
		"name": "Lesser Quintessence of Shielding",
		"description": "+0.21 magic resist per level (+3.78 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.21
		}]
	},
	5107: {
		"name": "Lesser Quintessence of Vigor",
		"description": "+1.5 health regen / 5 sec.",
		"effect": [{
			"stat": "hpreg",
			"amount": 1.5
		}]
	},
	5108: {
		"name": "Lesser Quintessence of Regeneration",
		"description": "+0.16 health regen / 5 sec. per level (+2.88 at champion level 18)",
		"effect": [{
			"stat": "hpregpl",
			"amount": 0.16
		}]
	},
	5111: {
		"name": "Lesser Quintessence of Focus",
		"description": "-0.91% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.91
		}]
	},
	5112: {
		"name": "Lesser Quintessence of Celerity",
		"description": "-0.07% cooldowns per level (-1.26% at champion level 18)",
		"effect": [{
			"stat": "cdrpl",
			"amount": 0.07
		}]
	},
	5113: {
		"name": "Lesser Quintessence of Potency",
		"description": "+2.75 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 2.75
		}]
	},
	5114: {
		"name": "Lesser Quintessence of Force",
		"description": "+0.24 ability power per level (+4.32 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.24
		}]
	},
	5115: {
		"name": "Lesser Quintessence of Intellect",
		"description": "+20.83 mana",
		"effect": [{
			"stat": "mana",
			"amount": 20.83
		}]
	},
	5116: {
		"name": "Lesser Quintessence of Knowledge",
		"description": "+2.31 mana per level (+41.58 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 2.31
		}]
	},
	5117: {
		"name": "Lesser Quintessence of Replenishment",
		"description": "+0.69 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.69
		}]
	},
	5118: {
		"name": "Lesser Quintessence of Clarity",
		"description": "+0.14 mana regen / 5 sec. per level (+2.52 at champion level 18)",
		"effect": [{
			"stat": "manaregpl",
			"amount": 0.14
		}]
	},
	5119: {
		"name": "Lesser Quintessence of Insight",
		"description": "+1.05 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 1.05
		}]
	},
	5121: {
		"name": "Lesser Quintessence of Swiftness",
		"description": "+0.83% movement speed",
		"effect": [{
			"stat": "ms",
			"amount": 0.83
		}]
	},
	5123: {
		"name": "Mark of Strength",
		"description": "+0.74 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 0.74
		}]
	},
	5124: {
		"name": "Mark of Might",
		"description": "+0.1 attack damage per level (+1.89 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.1
		}]
	},
	5125: {
		"name": "Mark of Alacrity",
		"description": "+1.32% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 1.32
		}]
	},
	5127: {
		"name": "Mark of Furor",
		"description": "+1.74% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 1.74
		}]
	},
	5129: {
		"name": "Mark of Malice",
		"description": "+0.72% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.72
		}]
	},
	5131: {
		"name": "Mark of Desolation",
		"description": "+1.29 armor penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 1.29
		}]
	},
	5133: {
		"name": "Mark of Fortitude",
		"description": "+2.7 health",
		"effect": [{
			"stat": "hp",
			"amount": 2.7
		}]
	},
	5134: {
		"name": "Mark of Vitality",
		"description": "+0.42 health per level (+7.56 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 0.42
		}]
	},
	5135: {
		"name": "Mark of Resilience",
		"description": "+0.71 armor",
		"effect": [{
			"stat": "ar",
			"amount": 0.71
		}]
	},
	5137: {
		"name": "Mark of Warding",
		"description": "+0.75 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 0.75
		}]
	},
	5138: {
		"name": "Mark of Shielding",
		"description": "+0.06 magic resist per level (+1.08 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.06
		}]
	},
	5143: {
		"name": "Mark of Focus",
		"description": "-0.13% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.13
		}]
	},
	5145: {
		"name": "Mark of Potency",
		"description": "+0.46 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.46
		}]
	},
	5146: {
		"name": "Mark of Force",
		"description": "+0.08 ability power per level (+1.44 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.08
		}]
	},
	5147: {
		"name": "Mark of Intellect",
		"description": "+4.59 mana",
		"effect": [{
			"stat": "mana",
			"amount": 4.59
		}]
	},
	5148: {
		"name": "Mark of Knowledge",
		"description": "+0.91 mana per level (+16.38 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 0.91
		}]
	},
	5149: {
		"name": "Mark of Replenishment",
		"description": "+0.2 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.2
		}]
	},
	5151: {
		"name": "Mark of Insight",
		"description": "+0.74 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 0.74
		}]
	},
	5153: {
		"name": "Glyph of Strength",
		"description": "+0.22 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 0.22
		}]
	},
	5154: {
		"name": "Glyph of Might",
		"description": "+0.03 attack damage per level (+0.57 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.03
		}]
	},
	5155: {
		"name": "Glyph of Alacrity",
		"description": "+0.5% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 0.5
		}]
	},
	5157: {
		"name": "Glyph of Furor",
		"description": "+0.43% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 0.43
		}]
	},
	5159: {
		"name": "Glyph of Malice",
		"description": "+0.22% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.22
		}]
	},
	5163: {
		"name": "Glyph of Fortitude",
		"description": "+2.08 health",
		"effect": [{
			"stat": "hp",
			"amount": 2.08
		}]
	},
	5164: {
		"name": "Glyph of Vitality",
		"description": "+0.42 health per level (+7.56 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 0.42
		}]
	},
	5165: {
		"name": "Glyph of Resilience",
		"description": "+0.55 armor",
		"effect": [{
			"stat": "ar",
			"amount": 0.55
		}]
	},
	5167: {
		"name": "Glyph of Warding",
		"description": "+1.16 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 1.16
		}]
	},
	5168: {
		"name": "Glyph of Shielding",
		"description": "+0.12 magic resist per level (+2.16 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.12
		}]
	},
	5169: {
		"name": "Glyph of Vigor",
		"description": "+0.21 health regen / 5 sec.",
		"effect": [{
			"stat": "hpreg",
			"amount": 0.21
		}]
	},
	5173: {
		"name": "Glyph of Focus",
		"description": "-0.51% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.51
		}]
	},
	5174: {
		"name": "Glyph of Celerity",
		"description": "-0.04% cooldowns per level (-0.72% at champion level 18)",
		"effect": [{
			"stat": "cdrpl",
			"amount": 0.04
		}]
	},
	5175: {
		"name": "Glyph of Potency",
		"description": "+0.77 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.77
		}]
	},
	5176: {
		"name": "Glyph of Force",
		"description": "+0.13 ability power per level (+2.34 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.13
		}]
	},
	5177: {
		"name": "Glyph of Intellect",
		"description": "+8.75 mana",
		"effect": [{
			"stat": "mana",
			"amount": 8.75
		}]
	},
	5178: {
		"name": "Glyph of Knowledge",
		"description": "+1.1 mana per level (+19.8 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 1.1
		}]
	},
	5179: {
		"name": "Glyph of Replenishment",
		"description": "+0.24 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.24
		}]
	},
	5180: {
		"name": "Glyph of Clarity",
		"description": "+0.04 mana regen / 5 sec. per level (+0.72 at champion level 18)",
		"effect": [{
			"stat": "manaregpl",
			"amount": 0.04
		}]
	},
	5181: {
		"name": "Glyph of Insight",
		"description": "+0.44 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 0.44
		}]
	},
	5183: {
		"name": "Seal of Strength",
		"description": "+0.33 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 0.33
		}]
	},
	5184: {
		"name": "Seal of Might",
		"description": "+0.05 attack damage per level (+0.85 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.05
		}]
	},
	5185: {
		"name": "Seal of Alacrity",
		"description": "+0.59% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 0.59
		}]
	},
	5187: {
		"name": "Seal of Furor",
		"description": "+0.61% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 0.61
		}]
	},
	5189: {
		"name": "Seal of Malice",
		"description": "+0.32% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.32
		}]
	},
	5193: {
		"name": "Seal of Fortitude",
		"description": "+4.16 health",
		"effect": [{
			"stat": "hp",
			"amount": 4.16
		}]
	},
	5194: {
		"name": "Seal of Vitality",
		"description": "+0.84 health per level (+15.12 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 0.84
		}]
	},
	5195: {
		"name": "Seal of Resilience",
		"description": "+1.09 armor",
		"effect": [{
			"stat": "ar",
			"amount": 1.09
		}]
	},
	5196: {
		"name": "Seal of Defense",
		"description": "+0.12 armor per level (+2.16 at champion level 18)",
		"effect": [{
			"stat": "arpl",
			"amount": 0.12
		}]
	},
	5197: {
		"name": "Seal of Warding",
		"description": "+0.58 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 0.58
		}]
	},
	5198: {
		"name": "Seal of Shielding",
		"description": "+0.08 magic resist per level (+1.44 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.08
		}]
	},
	5199: {
		"name": "Seal of Vigor",
		"description": "+0.34 health regen / 5 sec.",
		"effect": [{
			"stat": "hpreg",
			"amount": 0.34
		}]
	},
	5200: {
		"name": "Seal of Regeneration",
		"description": "+0.09 health regen / 5 sec. per level (+1.62 at champion level 18)",
		"effect": [{
			"stat": "hpregpl",
			"amount": 0.09
		}]
	},
	5203: {
		"name": "Seal of Focus",
		"description": "-0.23% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.23
		}]
	},
	5205: {
		"name": "Seal of Potency",
		"description": "+0.46 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.46
		}]
	},
	5206: {
		"name": "Seal of Force",
		"description": "+0.08 ability power per level (+1.44 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.08
		}]
	},
	5207: {
		"name": "Seal of Intellect",
		"description": "+5.36 mana",
		"effect": [{
			"stat": "mana",
			"amount": 5.36
		}]
	},
	5208: {
		"name": "Seal of Knowledge",
		"description": "+0.91 mana per level (+16.38 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 0.91
		}]
	},
	5209: {
		"name": "Seal of Replenishment",
		"description": "+0.32 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.32
		}]
	},
	5210: {
		"name": "Seal of Clarity",
		"description": "+0.05 mana regen / 5 sec. per level (+0.9 at champion level 18)",
		"effect": [{
			"stat": "manaregpl",
			"amount": 0.05
		}]
	},
	5213: {
		"name": "Quintessence of Strength",
		"description": "+1.75 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 1.75
		}]
	},
	5214: {
		"name": "Quintessence of Might",
		"description": "+0.19 attack damage per level (+3.42 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.19
		}]
	},
	5215: {
		"name": "Quintessence of Alacrity",
		"description": "+2.64% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 2.64
		}]
	},
	5217: {
		"name": "Quintessence of Furor",
		"description": "+3.47% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 3.47
		}]
	},
	5219: {
		"name": "Quintessence of Malice",
		"description": "+1.44% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 1.44
		}]
	},
	5221: {
		"name": "Quintessence of Desolation",
		"description": "+2.59 armor penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 2.59
		}]
	},
	5223: {
		"name": "Quintessence of Fortitude",
		"description": "+20 health",
		"effect": [{
			"stat": "hp",
			"amount": 20
		}]
	},
	5224: {
		"name": "Quintessence of Vitality",
		"description": "+2.1 health per level (+37.8 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 2.1
		}]
	},
	5225: {
		"name": "Quintessence of Resilience",
		"description": "+3.32 armor",
		"effect": [{
			"stat": "ar",
			"amount": 3.32
		}]
	},
	5226: {
		"name": "Quintessence of Defense",
		"description": "+0.29 armor per level (+5.22 at champion level 18)",
		"effect": [{
			"stat": "arpl",
			"amount": 0.29
		}]
	},
	5227: {
		"name": "Quintessence of Warding",
		"description": "+3.5 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 3.5
		}]
	},
	5228: {
		"name": "Quintessence of Shielding",
		"description": "+0.29 magic resist per level (+5.22 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.29
		}]
	},
	5229: {
		"name": "Quintessence of Vigor",
		"description": "+2.1 health regen / 5 sec.",
		"effect": [{
			"stat": "hpreg",
			"amount": 2.1
		}]
	},
	5230: {
		"name": "Quintessence of Regeneration",
		"description": "+0.22 health regen / 5 sec. per level (+3.96 at champion level 18)",
		"effect": [{
			"stat": "hpregpl",
			"amount": 0.22
		}]
	},
	5233: {
		"name": "Quintessence of Focus",
		"description": "-1.27% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 1.27
		}]
	},
	5234: {
		"name": "Quintessence of Celerity",
		"description": "-0.1% cooldowns per level (-1.8% at champion level 18)",
		"effect": [{
			"stat": "cdrpl",
			"amount": 0.1
		}]
	},
	5235: {
		"name": "Quintessence of Potency",
		"description": "+3.85 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 3.85
		}]
	},
	5236: {
		"name": "Quintessence of Force",
		"description": "+0.34 ability power per level (+6.12 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.34
		}]
	},
	5237: {
		"name": "Quintessence of Intellect",
		"description": "+29.17 mana",
		"effect": [{
			"stat": "mana",
			"amount": 29.17
		}]
	},
	5238: {
		"name": "Quintessence of Knowledge",
		"description": "+3.24 mana per level (+58.32 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 3.24
		}]
	},
	5239: {
		"name": "Quintessence of Replenishment",
		"description": "+0.97 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.97
		}]
	},
	5240: {
		"name": "Quintessence of Clarity",
		"description": "+0.19 mana regen / 5 sec. per level (+3.42 at champion level 18)",
		"effect": [{
			"stat": "manaregpl",
			"amount": 0.19
		}]
	},
	5241: {
		"name": "Quintessence of Insight",
		"description": "+1.47 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 1.47
		}]
	},
	5243: {
		"name": "Quintessence of Swiftness",
		"description": "+1.17% movement speed",
		"effect": [{
			"stat": "ms",
			"amount": 1.17
		}]
	},
	5245: {
		"name": "Greater Mark of Strength",
		"description": "+0.95 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 0.95
		}]
	},
	5246: {
		"name": "Greater Mark of Might",
		"description": "+0.13 attack damage per level (+2.43 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.13
		}]
	},
	5247: {
		"name": "Greater Mark of Alacrity",
		"description": "+1.7% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 1.7
		}]
	},
	5249: {
		"name": "Greater Mark of Furor",
		"description": "+2.23% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 2.23
		}]
	},
	5251: {
		"name": "Greater Mark of Malice",
		"description": "+0.93% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.93
		}]
	},
	5253: {
		"name": "Greater Mark of Desolation",
		"description": "+1.66 armor penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 1.66
		}]
	},
	5255: {
		"name": "Greater Mark of Fortitude",
		"description": "+3.47 health",
		"effect": [{
			"stat": "hp",
			"amount": 3.47
		}]
	},
	5256: {
		"name": "Greater Mark of Vitality",
		"description": "+0.54 health per level (+9.72 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 0.54
		}]
	},
	5257: {
		"name": "Greater Mark of Resilience",
		"description": "+0.91 armor",
		"effect": [{
			"stat": "ar",
			"amount": 0.91
		}]
	},
	5259: {
		"name": "Greater Mark of Warding",
		"description": "+0.97 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 0.97
		}]
	},
	5260: {
		"name": "Greater Mark of Shielding",
		"description": "+0.07 magic resist per level (+1.26 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.07
		}]
	},
	5265: {
		"name": "Greater Mark of Focus",
		"description": "-0.16% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.16
		}]
	},
	5267: {
		"name": "Greater Mark of Potency",
		"description": "+0.59 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.59
		}]
	},
	5268: {
		"name": "Greater Mark of Force",
		"description": "+0.1 ability power per level (+1.8 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.1
		}]
	},
	5269: {
		"name": "Greater Mark of Intellect",
		"description": "+5.91 mana",
		"effect": [{
			"stat": "mana",
			"amount": 5.91
		}]
	},
	5270: {
		"name": "Greater Mark of Knowledge",
		"description": "+1.17 mana per level (+21.06 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 1.17
		}]
	},
	5271: {
		"name": "Greater Mark of Replenishment",
		"description": "+0.26 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.26
		}]
	},
	5273: {
		"name": "Greater Mark of Insight",
		"description": "+0.95 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 0.95
		}]
	},
	5275: {
		"name": "Greater Glyph of Strength",
		"description": "+0.28 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 0.28
		}]
	},
	5276: {
		"name": "Greater Glyph of Might",
		"description": "+0.04 attack damage per level (+0.73 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.04
		}]
	},
	5277: {
		"name": "Greater Glyph of Alacrity",
		"description": "+0.64% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 0.64
		}]
	},
	5279: {
		"name": "Greater Glyph of Furor",
		"description": "+0.56% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 0.56
		}]
	},
	5281: {
		"name": "Greater Glyph of Malice",
		"description": "+0.28% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.28
		}]
	},
	5285: {
		"name": "Greater Glyph of Fortitude",
		"description": "+2.67 health",
		"effect": [{
			"stat": "hp",
			"amount": 2.67
		}]
	},
	5286: {
		"name": "Greater Glyph of Vitality",
		"description": "+0.54 health per level (+9.72 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 0.54
		}]
	},
	5287: {
		"name": "Greater Glyph of Resilience",
		"description": "+0.7 armor",
		"effect": [{
			"stat": "ar",
			"amount": 0.7
		}]
	},
	5289: {
		"name": "Greater Glyph of Warding",
		"description": "+1.34 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 1.34
		}]
	},
	5290: {
		"name": "Greater Glyph of Shielding",
		"description": "+0.15 magic resist per level (+2.7 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.15
		}]
	},
	5291: {
		"name": "Greater Glyph of Vigor",
		"description": "+0.27 health regen / 5 sec.",
		"effect": [{
			"stat": "hpreg",
			"amount": 0.37
		}]
	},
	5295: {
		"name": "Greater Glyph of Focus",
		"description": "-0.65% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.65
		}]
	},
	5296: {
		"name": "Greater Glyph of Celerity",
		"description": "-0.05% cooldowns per level (-0.9% at champion level 18)",
		"effect": [{
			"stat": "cdrpl",
			"amount": 0.05
		}]
	},
	5297: {
		"name": "Greater Glyph of Potency",
		"description": "+0.99 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.99
		}]
	},
	5298: {
		"name": "Greater Glyph of Force",
		"description": "+0.17 ability power per level (+3.06 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.17
		}]
	},
	5299: {
		"name": "Greater Glyph of Intellect",
		"description": "+11.25 mana",
		"effect": [{
			"stat": "mana",
			"amount": 11.25
		}]
	},
	5300: {
		"name": "Greater Glyph of Knowledge",
		"description": "+1.42 mana per level (+25.56 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 1.42
		}]
	},
	5301: {
		"name": "Greater Glyph of Replenishment",
		"description": "+0.31 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.31
		}]
	},
	5302: {
		"name": "Greater Glyph of Clarity",
		"description": "+0.055 mana regen / 5 sec. per level (+0.99 at champion level 18)",
		"effect": [{
			"stat": "manaregpl",
			"amount": 0.055
		}]
	},
	5303: {
		"name": "Greater Glyph of Insight",
		"description": "+0.57 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 0.57
		}]
	},
	5305: {
		"name": "Greater Seal of Strength",
		"description": "+0.43 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 0.43
		}]
	},
	5306: {
		"name": "Greater Seal of Might",
		"description": "+0.06 attack damage per level (+1.09 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.06
		}]
	},
	5307: {
		"name": "Greater Seal of Alacrity",
		"description": "+0.76% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 0.76
		}]
	},
	5309: {
		"name": "Greater Seal of Furor",
		"description": "+0.78% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 0.78
		}]
	},
	5311: {
		"name": "Greater Seal of Malice",
		"description": "+0.42% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.42
		}]
	},
	5315: {
		"name": "Greater Seal of Fortitude",
		"description": "+5.35 health",
		"effect": [{
			"stat": "hp",
			"amount": 5.35
		}]
	},
	5316: {
		"name": "Greater Seal of Vitality",
		"description": "+1.08 health per level (+19.44 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 1.08
		}]
	},
	5317: {
		"name": "Greater Seal of Resilience",
		"description": "+1.41 armor",
		"effect": [{
			"stat": "ar",
			"amount": 1.41
		}]
	},
	5318: {
		"name": "Greater Seal of Defense",
		"description": "+0.15 armor per level (+2.7 at champion level 18)",
		"effect": [{
			"stat": "arpl",
			"amount": 0.15
		}]
	},
	5319: {
		"name": "Greater Seal of Warding",
		"description": "+0.74 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 0.74
		}]
	},
	5320: {
		"name": "Greater Seal of Shielding",
		"description": "+0.1 magic resist per level (+1.8 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.1
		}]
	},
	5321: {
		"name": "Greater Seal of Vigor",
		"description": "+0.43 health regen / 5 sec.",
		"effect": [{
			"stat": "hpreg",
			"amount": 0.43
		}]
	},
	5322: {
		"name": "Greater Seal of Regeneration",
		"description": "+0.11 health regen / 5 sec. per level (+1.98 at champion level 18)",
		"effect": [{
			"stat": "hpregpl",
			"amount": 0.11
		}]
	},
	5325: {
		"name": "Greater Seal of Focus",
		"description": "-0.29% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.29
		}]
	},
	5327: {
		"name": "Greater Seal of Potency",
		"description": "+0.59 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.59
		}]
	},
	5328: {
		"name": "Greater Seal of Force",
		"description": "+0.1 ability power per level (+1.8 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.1
		}]
	},
	5329: {
		"name": "Greater Seal of Intellect",
		"description": "+6.89 mana",
		"effect": [{
			"stat": "mana",
			"amount": 6.89
		}]
	},
	5330: {
		"name": "Greater Seal of Knowledge",
		"description": "+1.17 mana per level (+21.06 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 1.17
		}]
	},
	5331: {
		"name": "Greater Seal of Replenishment",
		"description": "+0.41 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 0.41
		}]
	},
	5332: {
		"name": "Greater Seal of Clarity",
		"description": "+0.065 mana regen / 5 sec. per level (+1.17 at champion level 18)",
		"effect": [{
			"stat": "manaregpl",
			"amount": 0.065
		}]
	},
	5335: {
		"name": "Greater Quintessence of Strength",
		"description": "+2.25 attack damage",
		"effect": [{
			"stat": "ad",
			"amount": 2.25
		}]
	},
	5336: {
		"name": "Greater Quintessence of Might",
		"description": "+0.25 attack damage per level (+4.5 at champion level 18)",
		"effect": [{
			"stat": "adpl",
			"amount": 0.25
		}]
	},
	5337: {
		"name": "Greater Quintessence of Alacrity",
		"description": "+3.4% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 3.4
		}]
	},
	5339: {
		"name": "Greater Quintessence of Furor",
		"description": "+4.46% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 4.46
		}]
	},
	5341: {
		"name": "Greater Quintessence of Malice",
		"description": "+1.86% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 1.86
		}]
	},
	5343: {
		"name": "Greater Quintessence of Desolation",
		"description": "+3.33 armor penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 3.33
		}]
	},
	5345: {
		"name": "Greater Quintessence of Fortitude",
		"description": "+26 health",
		"effect": [{
			"stat": "hp",
			"amount": 26
		}]
	},
	5346: {
		"name": "Greater Quintessence of Vitality",
		"description": "+2.7 health per level (+48.6 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 2.7
		}]
	},
	5347: {
		"name": "Greater Quintessence of Resilience",
		"description": "+4.26 armor",
		"effect": [{
			"stat": "ar",
			"amount": 4.26
		}]
	},
	5348: {
		"name": "Greater Quintessence of Defense",
		"description": "+0.38 armor per level (+6.84 at champion level 18)",
		"effect": [{
			"stat": "arpl",
			"amount": 0.38
		}]
	},
	5349: {
		"name": "Greater Quintessence of Warding",
		"description": "+4.5 magic resist",
		"effect": [{
			"stat": "mr",
			"amount": 4.5
		}]
	},
	5350: {
		"name": "Greater Quintessence of Shielding",
		"description": "+0.37 magic resist per level (+6.66 at champion level 18)",
		"effect": [{
			"stat": "mrpl",
			"amount": 0.37
		}]
	},
	5351: {
		"name": "Greater Quintessence of Vigor",
		"description": "+2.7 health regen / 5 sec.",
		"effect": [{
			"stat": "hpreg",
			"amount": 2.7
		}]
	},
	5352: {
		"name": "Greater Quintessence of Regeneration",
		"description": "+0.28 health regen / 5 sec. per level (+5.04 at champion level 18)",
		"effect": [{
			"stat": "hpregpl",
			"amount": 0.28
		}]
	},
	5355: {
		"name": "Greater Quintessence of Focus",
		"description": "-1.64% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 1.64
		}]
	},
	5356: {
		"name": "Greater Quintessence of Celerity",
		"description": "-0.13% cooldowns per level (-2.34% at champion level 18)",
		"effect": [{
			"stat": "cdrpl",
			"amount": 0.13
		}]
	},
	5357: {
		"name": "Greater Quintessence of Potency",
		"description": "+4.95 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 4.95
		}]
	},
	5358: {
		"name": "Greater Quintessence of Force",
		"description": "+0.43 ability power per level (+7.74 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.43
		}]
	},
	5359: {
		"name": "Greater Quintessence of Intellect",
		"description": "+37.5 mana",
		"effect": [{
			"stat": "mana",
			"amount": 37.5
		}]
	},
	5360: {
		"name": "Greater Quintessence of Knowledge",
		"description": "+4.17 mana per level (+75.06 at champion level 18)",
		"effect": [{
			"stat": "manapl",
			"amount": 4.17
		}]
	},
	5361: {
		"name": "Greater Quintessence of Replenishment",
		"description": "+1.25 mana regen / 5 sec.",
		"effect": [{
			"stat": "manareg",
			"amount": 1.25
		}]
	},
	5362: {
		"name": "Greater Quintessence of Clarity",
		"description": "+0.24 mana regen / 5 sec. per level (+4.32 at champion level 18)",
		"effect": [{
			"stat": "manaregpl",
			"amount": 0.24
		}]
	},
	5363: {
		"name": "Greater Quintessence of Insight",
		"description": "+1.89 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 1.89
		}]
	},
	5365: {
		"name": "Greater Quintessence of Swiftness",
		"description": "+1.5% movement speed",
		"effect": [{
			"stat": "ms",
			"amount": 1.5
		}]
	},
	5366: {
		"name": "Greater Quintessence of Revival",
		"description": "-5% time dead",
		"effect": [{
			"stat": "res",
			"amount": 5
		}]
	},
	5367: {
		"name": "Greater Quintessence of Avarice",
		"description": "+1 gold / 10 sec.",
		"effect": [{
			"stat": "gold",
			"amount": 1
		}]
	},
	5368: {
		"name": "Greater Quintessence of Wisdom",
		"description": "+2% experience gained",
		"effect": [{
			"stat": "xp",
			"amount": 2
		}]
	},
	5369: {
		"name": "Greater Seal of Meditation",
		"description": "+0.63 Energy regen/5 sec",
		"effect": [{
			"stat": "energyreg",
			"amount": 0.63
		}]
	},
	5370: {
		"name": "Greater Seal of Lucidity",
		"description": "+0.064 Energy regen/5 sec per level (+1.15 at champion level 18)",
		"effect": [{
			"stat": "energyregpl",
			"amount": 0.064
		}]
	},
	5371: {
		"name": "Greater Glyph of Acumen",
		"description": "+2.2 Energy",
		"effect": [{
			"stat": "energy",
			"amount": 2.2
		}]
	},
	5372: {
		"name": "Greater Glyph of Sapience",
		"description": "+0.161 Energy/level (+2.89 at level 18)",
		"effect": [{
			"stat": "energypl",
			"amount": 0.161
		}]
	},
	5373: {
		"name": "Greater Quintessence of Meditation",
		"description": "+1.575 Energy regen/5 sec",
		"effect": [{
			"stat": "energyreg",
			"amount": 1.575
		}]
	},
	5374: {
		"name": "Greater Quintessence of Acumen",
		"description": "+5.4 Energy",
		"effect": [{
			"stat": "energy",
			"amount": 5.4
		}]
	},
	5400: {
		"name": "Lesser Mark of Destruction",
		"description": "+0.56 Armor Penetration / +0.32 Magic Penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 0.56
		}, {
			"stat": "mpen",
			"amount": 0.32
		}]
	},
	5401: {
		"name": "Mark of Destruction",
		"description": "+0.74 Armor Penetration / +0.44 Magic Penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 0.74
		}, {
			"stat": "mpen",
			"amount": 0.44
		}]
	},
	5402: {
		"name": "Greater Mark of Destruction",
		"description": "+1.0 Armor Penetration / +0.57 Magic Penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 1
		}, {
			"stat": "mpen",
			"amount": 0.57
		}]
	},
	5403: {
		"name": "Greater Seal of Avarice",
		"description": "+0.25 gold / 10 sec.",
		"effect": [{
			"stat": "gold",
			"amount": 0.25
		}]
	},
	5404: {
		"name": "Lesser Quintessence of Endurance",
		"description": "+0.84% increased health.",
		"effect": [{
			"stat": "hppct",
			"amount": 0.84
		}]
	},
	5405: {
		"name": "Quintessence of Endurance",
		"description": "+1.17% increased health.",
		"effect": [{
			"stat": "hppct",
			"amount": 1.17
		}]
	},
	5406: {
		"name": "Greater Quintessence of Endurance",
		"description": "+1.5% increased health.",
		"effect": [{
			"stat": "hppct",
			"amount": 1.5
		}]
	},
	5407: {
		"name": "Lesser Quintessence of Transmutation",
		"description": "+1.12% Spellvamp.",
		"effect": [{
			"stat": "sv",
			"amount": 1.12
		}]
	},
	5408: {
		"name": "Quintessence of Transmutation",
		"description": "+1.56% Spellvamp.",
		"effect": [{
			"stat": "sv",
			"amount": 1.56
		}]
	},
	5409: {
		"name": "Greater Quintessence of Transmutation",
		"description": "+2% Spellvamp.",
		"effect": [{
			"stat": "sv",
			"amount": 2
		}]
	},
	5410: {
		"name": "Lesser Quintessence of Vampirism",
		"description": "+1.12% Lifesteal",
		"effect": [{
			"stat": "ls",
			"amount": 1.12
		}]
	},
	5411: {
		"name": "Quintessence of Vampirism",
		"description": "+1.56% Lifesteal",
		"effect": [{
			"stat": "ls",
			"amount": 1.56
		}]
	},
	5412: {
		"name": "Greater Quintessence of Vampirism",
		"description": "+2% Lifesteal.",
		"effect": [{
			"stat": "ls",
			"amount": 2
		}]
	},
	5413: {
		"name": "Lesser Seal of Endurance",
		"description": "+0.28% Health.",
		"effect": [{
			"stat": "hppct",
			"amount": 0.28
		}]
	},
	5414: {
		"name": "Seal of Endurance",
		"description": "+0.39% Health.",
		"effect": [{
			"stat": "hppct",
			"amount": 0.39
		}]
	},
	5415: {
		"name": "Greater Seal of Endurance",
		"description": "+0.5% Health.",
		"effect": [{
			"stat": "hppct",
			"amount": 0.5
		}]
	},
	5416: {
		"name": "Lesser Quintessence of Destruction",
		"description": "+1.11 Armor Penetration / +0.63 Magic Penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 1.11
		}, {
			"stat": "mpen",
			"amount": 0.63
		}]
	},
	5417: {
		"name": "Quintessence of Destruction",
		"description": "+1.55 Armor Penetration / +0.88 Magic Penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 1.55
		}, {
			"stat": "mpen",
			"amount": 0.88
		}]
	},
	5418: {
		"name": "Greater Quintessence of Destruction",
		"description": "+2.0 Armor Penetration / +1.13 Magic Penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 2
		}, {
			"stat": "mpen",
			"amount": 1.13
		}]
	},
	8001: {
		"name": "Mark of the Crippling Candy Cane",
		"description": "+2% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 2
		}]
	},
	8002: {
		"name": "Lesser Mark of the Yuletide Tannenbaum ",
		"description": "+0.62% critical chance",
		"effect": [{
			"stat": "critcha",
			"amount": 0.62
		}]
	},
	8003: {
		"name": "Glyph of the Special Stocking",
		"description": "-0.58% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.58
		}]
	},
	8005: {
		"name": "Lesser Glyph of the Gracious Gift",
		"description": "+0.12 ability power per level (+2.16 at champion level 18)",
		"effect": [{
			"stat": "appl",
			"amount": 0.12
		}]
	},
	8006: {
		"name": "Lesser Seal of the Stout Snowman",
		"description": "+0.72 health per level (+12.96 at champion level 18)",
		"effect": [{
			"stat": "hppl",
			"amount": 0.72
		}]
	},
	8007: {
		"name": "Lesser Mark of Alpine Alacrity",
		"description": "+1.13% attack speed",
		"effect": [{
			"stat": "as",
			"amount": 1.13
		}]
	},
	8008: {
		"name": "Mark of the Combatant",
		"description": "+2% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 2
		}]
	},
	8009: {
		"name": "Lesser Seal of the Medalist",
		"description": "+3.56 health",
		"effect": [{
			"stat": "hp",
			"amount": 3.56
		}]
	},
	8011: {
		"name": "Lesser Glyph of the Challenger",
		"description": "+0.66 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 0.66
		}]
	},
	8012: {
		"name": "Glyph of the Soaring Slalom",
		"description": "-0.58% cooldowns",
		"effect": [{
			"stat": "cdr",
			"amount": 0.58
		}]
	},
	8013: {
		"name": "Quintessence of the Headless Horseman",
		"description": "+3.08 armor penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 3.08
		}]
	},
	8014: {
		"name": "Quintessence of the Piercing Screech",
		"description": "+1.75 magic penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 1.75
		}]
	},
	8015: {
		"name": "Quintessence of Bountiful Treats",
		"description": "+24 health",
		"effect": [{
			"stat": "hp",
			"amount": 24
		}]
	},
	8016: {
		"name": "Quintessence of the Speedy Specter",
		"description": "+1.39% movement speed",
		"effect": [{
			"stat": "ms",
			"amount": 1.39
		}]
	},
	8017: {
		"name": "Quintessence of the Witches Brew",
		"description": "+4.56 ability power",
		"effect": [{
			"stat": "ap",
			"amount": 4.56
		}]
	},
	8019: {
		"name": "Greater Quintessence of the Piercing Present",
		"description": "+1.89 magic penetration",
		"effect": [{
			"stat": "mpen",
			"amount": 1.89
		}]
	},
	8020: {
		"name": "Greater Quintessence of the Deadly Wreath",
		"description": "+3.33 armor penetration",
		"effect": [{
			"stat": "arpen",
			"amount": 3.33
		}]
	},
	8021: {
		"name": "Greater Quintessence of Frosty Fortitude",
		"description": "+26 health",
		"effect": [{
			"stat": "hp",
			"amount": 26
		}]
	},
	8022: {
		"name": "Greater Quintessence of Sugar Rush",
		"description": "+1.5% movement speed",
		"effect": [{
			"stat": "ms",
			"amount": 1.5
		}]
	},
	8035: {
		"name": "Greater Quintessence of Studio Rumble",
		"description": "+1.5% movement speed",
		"effect": [{
			"stat": "ms",
			"amount": 1.5
		}]
	},
	10001: {
		"name": "Razer Mark of Precision",
		"description": "+2.23% critical damage",
		"effect": [{
			"stat": "critdmg",
			"amount": 2.23
		}]
	},
	10002: {
		"name": "Razer Quintessence of Speed",
		"description": "+1.5% movement speed",
		"effect": [{
			"stat": "ms",
			"amount": 1.5
		}]
	}
}
