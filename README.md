# CC-Wick-Parser
A parser that helps contract the creation/annihilation operators with phase factor. 

This repository follows the style of numpy's `einsum` function that automatically parses the symbols in a string.
It implements the Wick's theorem, taking good care of the phase factor for each term, with consideration to the 
occupied / virtual orbitals during the contraction. The symbols follow the convention of 

```angular2html
"a", "b", .... -> virtual
"i", "j", .... -> occupied
"p", "q", .... -> general
```

which can also be customized.

Should be good to go, running the unit test, after exporting, the directory to this repository, to $PYTHONPATH.
