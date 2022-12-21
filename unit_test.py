import cc_wick_parser

print("".join([pair.to_latex() for pair in cc_wick_parser.parse("p+q+sr, a+b+ji")]))
print("".join([pair.to_latex() for pair in cc_wick_parser.parse("p+q+sr, a+i, b+j")]))
