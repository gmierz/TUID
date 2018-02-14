# Experimental TUID Project

TUID is an acronym for "temporally unique identifiers". These are numbers that effectively track "blame" throughout the source code.

## Overview

This is an attempt to provide a high speed cache for TUIDs. It is intended for use by CodeCoverage; mapping codecoverage by `tuid` rather than `(revsion, file, line)` triples.

More details can be gleaned from the [motivational document](https://github.com/mozilla/TUID/tree/dev/docs)
