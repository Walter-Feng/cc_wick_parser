import core

print("".join([pair.to_latex() for pair in core.cc_parser("p+q+sr, a+b+ji")]))
print("".join([pair.to_latex() for pair in core.cc_parser("p+q+sr, a+i, b+j")]))
