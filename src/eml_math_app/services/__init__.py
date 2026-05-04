"""Domain services for EML-Math-App.

These modules sit between the GUI and ``eml_math``. The screen layer
depends on them via small abstract surfaces (a parser, a formatter, a
hit-tester) so each can be swapped, extended or reused without touching
the view code — see SOLID's DIP and OCP.
"""
