bandparams
==========
Calculate parameters of a band: max, barycenter, width etc

It works for single bands. Works best for unimodal bands (single maximum),
but may also work for bands having side maxima in addition to the main max.
In such cases, max_pos and max_val refer to the global maximum.
FWHM determination may need to be carefully checked in such cases.
