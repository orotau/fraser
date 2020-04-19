'''
This module contains the regexes used in
the word frequency work
'''

##################################################################
#1 Open Compounds - "oc"
##################################################################
def get_oc_regex(open_compound):
    '''
    This function gets the open compound to search for
    and returns the regex that will find it
    Ensures that we don't consume part of a closed compound
    '''

    oc_regex_start = "((?<!-)"      # 1 capturing group
    oc_regex_middle = r"\b" + open_compound + r"\b"
    oc_regex_end = "(?!-))"

    return oc_regex_start + oc_regex_middle + oc_regex_end

    
static_regexes = []
##################################################################
#Group 2 - Vanilla Open Compounds
##################################################################
static_regexes.insert(0, ("voc", r"""
(                       # capturing group 1 of 1
(?:
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]+             # one or more alphanumeric characters
[ ]+                    # one or more spaces
)
+                       # one or more

(?:
\b
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]+             # one or more alphanumeric characters
\b
)

(?!
-                       # Don't bump into a closed compound
)

)                       # End of capturing group 1 of 1
"""
))

##################################################################
#Group 3 - Mixed Open Compounds
##################################################################
static_regexes.insert(1, ("moc", r"""
# first - capitalised non-closed-compound word
(                       # capturing group 1 of 1
(?:
\b
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]*             # zero or more alphabetic characters
[ ]+                    # 1 or more spaces
)


# second - capitalised closed compound
(?:    

(?:
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]+              
)

(?:  
-                       # dash
[A-Za-zĀĒĪŌŪāēīōū]+     # one word
)+                      # one or more times

)
)                       # End of Capturing Group 1 of 1
"""
))

##################################################################
#Group 4 - Isolated Capitalised Non-Compound Word
# The regex will find all Capitalised Non-Compound Words
# but if they are contained in Compound Words previously found
# they will be rejected (classed as "all inside")
# resulting in isolated.
##################################################################
static_regexes.insert(2, ("icncw", r"""
(                       # capturing group 1 of 1
(?<!
-                       # Don't select part of a closed compound
)
               
(?:
\b
[A-ZĀĒĪŌŪ]              # capital letter to start
[a-zāēīōū]*             # zero or more alphabetic characters
\b
)

(?!
-                       # Don't select part of a closed compound
)
)                       # End of capturing group 1 of 1
"""
))

##################################################################
#Group 5 - Isolated Closed-Compound Words
# The regex will find all Closed-Compound Words
# but if they are contained in Mixed Open Compound Words previously found
# they will be rejected (classed as "all inside")
# resulting in isolated.
##################################################################
static_regexes.insert(3, ("iccw", r"""
(                       # capturing group 1 of 1
(?:    

(?:
[A-Za-zĀĒĪŌŪāēīōū]+     # one word 
)

(?:  
-                       # dash
[A-Za-zĀĒĪŌŪāēīōū]+     # one word
)+                      # one or more times

)
)                       # End of capturing group 1 of 1
"""
))

##################################################################
# Group 6 - Isolated Lower Case Non-Compound Word
# The regex will find all Lower Case Non-Compound Words
# but if they are contained in Compound Words previously found
# they will be rejected (classed as "all inside")
# resulting in isolated.
##################################################################
static_regexes.insert(4, ("ilcncw", r"""
(                       # capturing group 1 of 1
(?<!
-                       # Don't select part of a closed compound
)
               
(?:
\b
[a-zāēīōū]+             # one or more alphabetic characters
\b
)

(?!
-                       # Don't select part of a closed compound
)
)                       # End of capturing group 1 of 1
"""
))

##################################################################
# Group 7a - Misc - Numbers + Units + things like R18 and 7a
##################################################################
static_regexes.insert(5, ("misc_number", r"""
(                       # capturing group 1 of 1
[A-Za-z]?
[0-9]+
[A-Za-z]?
[¼½¾]?
|
[¼½¾]
)                       # End of capturing group 1 of 1
"""
))

##################################################################
# Group 7b - Misc - Prefixes
##################################################################
static_regexes.insert(6, ("misc_prefix", r"""
(                       # capturing group 1 of 1
[A-Za-zĀĒĪŌŪāēīōū]+
)                       # End of capturing group 1 of 1
-                       # dash
(?!
[A-Za-zĀĒĪŌŪāēīōū]      # Not if part of a closed compound
)
"""
))

##################################################################
# Group 7c - Misc - Suffixes
##################################################################
static_regexes.insert(7, ("misc_suffix", r"""
(?<!
[A-Za-zĀĒĪŌŪāēīōū]      # Don't select part of a closed compound
)
-                       # dash
(                       # capturing group 1 of 1
[A-Za-zĀĒĪŌŪāēīōū]+
)                       # End of capturing group 1 of 1
"""
))

##################################################################
# Group 7d - Misc - Two or More capital letter words
##################################################################
static_regexes.insert(8, ("misc_all_caps", r"""
(                       # capturing group 1 of 1
\b
[A-ZĀĒĪŌŪ]{2,}
\b
)                       # End of capturing group 1 of 1
"""
))

##################################################################
# Group 8 - Punctuation and Whitespace
##################################################################
static_regexes.insert(9, ("paws", r"""
(                       # capturing group 1 of 1
\W+
)                       # End of capturing group 1 of 1
"""
))


sentence_boundaries = []

sentence_boundaries.insert(0, r"""

(?:
\A                      # Start of text chunk only
['"]                    # single or double quote
[ ]*                    # 0, 1 or more spaces
)

""")

sentence_boundaries.insert(1, r"""

(?:
[ ]+                    # 1 or more spaces
['"]                    # single or double quote
[ ]*                    # 0, 1 or more spaces
)

""")

sentence_boundaries.insert(2, r"""

(?:
[:]
[ ]+
)

""")

sentence_boundaries.insert(3, r"""

(?:
[.?!]
['"]?
[ ]+
)

""")

sentence_boundaries.insert(4, r"""
(?:
(?<!            #Avoid matching a name like T. D. Smith
[ ]             #works so long as it is not the first thing in the text chunk
[A-Z]
)
[.]
[ ]+
)

""")



maori_word = r"""
\b                      # capture whole words only

(?:

(?:                     
ng                      # needs to be before the n
|
wh                      # needs to be before the w and h
|
[hkmnprtw]
)
?                       # 0 or 1 times

(?:
[aeiouāēīōū]
)

)                      
+                       # one or more of the above
\b
"""

