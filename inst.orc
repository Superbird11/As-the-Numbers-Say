; universal format data
sr = 44100
kr = 4410
ksmps = 10
nchnls = 1


;        **************************************************************
;        * Bells / Glockenspeil                                       *
instr  1; *************************************************************
    iatk    =       p6
    irvb    =       p7
    irel    =       p3 - iatk - iatk
    irel2   =       p3 - iatk - iatk - irel

    icar    =       .0025
    imod    =       1
    kndx    =       0.5

    iamp1   =       ampdb(p4)
    ifq1    =       cpspch(p5)
    kenv1   linseg  0, iatk, iamp1, iatk, iamp1*0.4, irel, 0
    a1      foscili kenv1, ifq1, icar, imod, kndx, 1

    iamp2   =       iamp1 / 3.0
    ifq2    =       ifq1 * 4
    kenv2   linseg  0, iatk, iamp2, iatk, iamp2*0.6, irel, 0
    a2      oscili  kenv2, ifq2, 1

    iamp3   =       iamp1 / 2.0
    ifq3    =       ifq1 * 2
    kenv3   linseg  0, iatk, iamp3, iatk, iamp3*0.1, irel, 0
    a3      oscili  kenv3, ifq3, 1

    iamp4   =       iamp1 / 1.5
    ifq4    =       ifq1 * 8
    kenv4   linseg  0, iatk, iamp4, iatk, iamp4*0.2, irel, 0
    a4      oscili  kenv4, ifq4, 1

    asum    =   a1+a2+a3+a4
    arev    reverb  asum, irvb
    out     asum
endin


;        **************************************************************
;        * Electrosynth bass, frequency modulating throughout         *
instr  2; *************************************************************
    iatk    =       p6                          ; time to rise
    irel    =       p6                          ; time to release
    isus    =       p3 - iatk - irel            ; time to sustain between rise and fall
    ifmi    =       10                          ; amount of modulation
    ifmsca  =       1                           ; frequency modulation amplitude scale factor

    icar    =       1                           ; carrier frequency
    imod    =       p7                          ; modulator frequency, basically (default 1)
    indx    =       p8                          ; index of modulation (default 5)

    iamp    =       ampdb(p4)                   ; amplitude
    ifq     =       cpspch(p5)                  ; frequency
    kenv1   linseg  0, iatk, iamp, isus, 0, irel, 0
    a1      oscili  kenv1, ifq, 4
    iamp2   =       iamp / 2.0
    ifq2    =       ifq * 2.0
    kenv2   linseg  0, iatk, iamp2, isus, 0, irel, 0
    a2      oscili  kenv2, ifq2, 1
    iamp3   =       iamp / 2.0
    ifq3    =       ifq * 3.0
    kenv3   linseg  0, iatk, iamp3, isus, 0, irel, 0
    a3      oscili  kenv3, ifq3, 1
    aosc    = a1 + a2 + a3

    ; ---

    kfenv1  linseg  0, iatk, 0, isus, iamp, irel, 0
    af1     foscili kfenv1, ifq, icar, imod, indx, 1
    kfenv2  linseg  0, iatk, 0, isus, iamp2, irel, 0
    af2     foscili kfenv2, ifq2, icar, imod, indx, 1
    kfenv3  linseg  0, iatk, 0, isus, iamp3, irel, 0
    af3     foscili kfenv3, ifq3, icar, imod, indx, 1
    afm     = af1 ;+ af2 + af3

    ; ---

    out     aosc + afm
endin


;        **************************************************************
;        * Half-Decent Clarinet synth                                 *
instr  3; *************************************************************
    iatk    =       p6                          ; time in initial attack
    idecay  =       p6                          ; time in initial decay
    irel    =       p7                          ; time in final decay/release
    isus    =       p3 - iatk - idecay - irel   ; time in the sustain
    idiv    =       4


    iamp1   =       ampdb(p4) / 2               ; amplitude of sustain
    iinamp1 =       ampdb(p4)                   ; amplitude of attack
    ifq1    =       cpspch(p5)                  ; frequency
    kamp1   linseg  0, iatk, iinamp1, idecay, iamp1, isus, iamp1/idiv, irel, 0
    a1      oscili  kamp1, ifq1, 4              ; using pulse

    iamp2   =       iamp1 / 2
    iinamp2 =       iamp2 * 2
    ifq2    =       ifq1 * 2
    kamp2   linseg  0, iatk, iinamp2, idecay, iamp2, isus, iamp2/idiv, irel, 0
    a2      oscili  kamp2, ifq2, 1              ; using sine

    iamp3   =       iamp2 / 2
    iinamp3 =       iamp3 * 2
    ifq3    =       ifq1 * 3
    kamp3   linseg  0, iatk, iinamp3, idecay, iamp3, isus, iamp3/idiv, irel, 0
    a3      oscili  kamp3, ifq3, 1              ; using sine

    iamp4   =       iamp3 / 2
    iinamp4 =       iamp4 * 2
    ifq4    =       ifq1 * 4
    kamp4   linseg  0, iatk, iinamp4, idecay, iamp4, isus, iamp4/idiv, irel, 0
    a4      oscili  kamp4, ifq4, 1              ; using sine

    iamp5   =       iamp1 / 2
    ifq5    =       ifq1 / 8
    ihrd    =       0.2     ; hardness
    ipos    =       0.9     ; position on block to hit
    imp     =       12      ; table of strike impulses. I loaded f12 for this purpose
    ivfn    =       1       ; vibrato function table
    idec    =       irel    ; time before end of note when damping is introduced
    kvibf   =       44.1
    kvamp   =       12
    a5      vibes   iamp5, ifq5, ihrd, ipos, imp, kvibf, kvamp, ivfn, idec

    out     a1+a2+a3+a4;+a5
endin


;        **************************************************************
;        * Nice-ish plucked bass sound. Difficult to improve further. *
instr 4; **************************************************************
    iplk    =       0.1         ; pluck point up the string (0 is no pluck)
    kpick   =       0.985       ; proportion up the string to sample the output
    krefl   =       0.9         ; "coefficient of reflection"; lossiness, rate of decay

    ihit    =       0.1         ; how long the initial hit lasts
    isus    =       p3 - ihit   ; how long to sustain after initial hit

    ifq1     =          cpspch(p5)                      ; frequency
    iamp1    =          ampdb(p4) * ifq1 / 10              ; amplitude
    kamp1   linseg      0, ihit, iamp1, isus, 0
    a1      wgpluck2    iplk, kamp1, ifq1, kpick, krefl

    iamp2   =           iamp1 / 2.0
    ifq2    =           ifq1 * 2.0
    kamp2   linseg      0, .1, iamp2, isus, 0
    a2      wgpluck2    iplk, kamp2, ifq2, kpick, krefl

    iamp3   =           iamp2 / 2.0
    ifq3    =           ifq1 * 3.0
    kamp3   linseg      0, .1, iamp3, isus, 0
    a3      wgpluck2    iplk, kamp3, ifq3, kpick, krefl

    out     a1+a2
endin


;        **************************************************************
;        * Beepy Thing, light FM                                      *
instr  5;*************************************************************
    iatk    =       p6
    irel    =       p3 - iatk
    imfq    =       p7

    iamp1   =       ampdb(p4)
    ifq1    =       cpspch(p5)
    kenv1   linseg  0, iatk, iamp1, irel, 0
    a1      oscili  kenv1, ifq1, 1
    a2      oscili  kenv1, ifq1, 2
    a3      oscili, kenv1, ifq1, 3

    iotamp1 =       iamp1 * 0.75
    kotenv1 linseg  0, iatk, iotamp1, irel, 0
    iotfq1p =       ifq1 + (imfq * 1)
    iotfq1m =       ifq1 - (imfq * 1)
    aot1p   oscili  kotenv1, iotfq1p, 4
    aot1m   oscili  kotenv1, iotfq1m, 4

    asum    =       a1+a2+a3
    aotsum  =       aot1p + aot1m
    afin    =       asum + aotsum

    out     afin
endin


;        **************************************************************
;        * Buzzy Thing, light FM                                      *
instr  6; *************************************************************
    idur    =       p3
    iatk    =       p6
    irel    =       p7
    isus    =       idur - iatk - iatk - irel
    inmh    =       3

    iamp1   =       ampdb(p4) * 0.5
    ifq1    =       cpspch(p5)
    kenv1   linseg  0, iatk, iamp1, iatk, iamp1*0.67, isus, iamp1*0.67, irel, 0
    knh     linseg  inmh, idur, inmh

    a1      buzz    kenv1, ifq1, knh, 3
    a2      buzz    kenv1, ifq1, knh, 1

    ifq3    =       ifq1 - 1 ;ifq1 * 3
    iamp3   =       iamp1 * 0.5
    kenv3   linseg  0, iatk, iamp3, iatk, iamp3*0.67, isus, iamp3*0.67, irel, 0
    a3      oscil   kenv3, ifq3, 4

    ifq5    =       ifq1 + 1 ;ifq1 * 5
    iamp5   =       iamp1 * 0.5
    kenv5   linseg  0, iatk, iamp5, iatk, iamp5*0.67, isus, iamp5*0.67, irel, 0
    a5      oscil   kenv5, ifq5, 4

    out     a1+a2+a3+a5
endin


;        **************************************************************
;        * Drumbell, modified from ACCCI 03                           *
instr  7; *************************************************************
    idur    =       p3
    iamp7   =       ampdb(p4)*2.5
    ifq1    =       cpspch(p5)
    iamp2   =       iamp7 * .8
    ifq3    =       ifq1 * .5
    iamp4   =       iamp7 * .3
    ifq7    =       ifq1 * .25

    a5      oscili  iamp7, 1/idur, 51
    a5      oscili  a5, ifq7, 5

    a3      oscili  iamp4, 1/idur, 51
    a3      oscili  a3, ifq3, 5

    a1      oscili  iamp2, 1/idur, 51
    a1      oscili  a1, ifq1, 1

    out     a1+a3+a5
endin


;        **************************************************************
;        * Scratchy/rough Wayou                                       *
instr  8; *************************************************************
    idur    =       p3
    iatk    =       p6
    irel    =       p7
    isus    =       idur - iatk - iatk - irel

    iamp1   =       ampdb(p4)*.6
    ifq1    =       cpspch(p5)
    imh     =       8
    ilh     =       1
    iintv   =       iatk / imh
    iints   =       isus / imh

    kenv1   linseg  0, iatk, iamp1, iatk, iamp1*.25, isus, 0, irel, 0
    knh1    linseg  ilh, iatk, imh, iatk, imh, isus, ilh, irel, ilh
    knh0    line    5, idur, 9

    a1      buzz    kenv1, ifq1, knh1, 3   ; do it manually - instead of making knh an envelope, make other buzzes and envelope them
    a2      buzz    kenv1, ifq1, knh1, 2
    a3      oscili  kenv1*.6, ifq1, 1
    out     a1+a2+a3
endin


;        **************************************************************
;        * Churchbell                                                 *
instr  9; *************************************************************
    idur    =       p3
    iamp1   =       ampdb(p4)
    ifq1    =       cpspch(p5)

    ihrd    =       p6      ; hardness
    ipos    =       p7      ; position on block to hit
    imp     =       12      ; table of strike impulses. I loaded f12 for this purpose
    ivfn    =       1       ; vibrato function table
    idec    =       0.1    ; time before end of note when damping is introduced
    kvibf   =       p8
    kvamp   =       p9

    a1      vibes   iamp1, ifq1, ihrd, ipos, imp, kvibf, kvamp, ivfn, idec
    a2      vibes   iamp1*1.25, ifq1, ihrd, ipos, imp, 0, 0, ivfn, idec
    out     a1+a2
endin


;        **************************************************************
;        * Waveguided instruments fusion                              *
instr 10; *************************************************************

    idur    =       p3
    iatk    =       p6
    irel    =       p7
    isus    =       idur - iatk - irel

    iamp1   =       ampdb(p4) * 2
    ifq1    =       cpspch(p5)

    kpres   =       3
    krat    =       0.127236
    kvibf   =       6.12723
    kvib    linseg  0, iatk, 0, isus, 1, irel, 1				; amplitude envelope for the vibrato.
    kvamp   =       kvib * 0.01
    kenv1   linseg  0, iatk, iamp1, isus, iamp1, irel, 0

    a1      wgbow   kenv1, ifq1, kpres, krat, kvibf, kvamp, 2

    kstiff  =       -0.44
    iatt    =       0.1
    idetk   =       0.1
    kngain  =       0.05
    kvibf   =       45; 5.735
    kvamp   =       0.1

    a2      wgclar  kenv1, ifq1*2, kstiff, iatt, idetk, kngain, kvibf, kvamp, 4

    out     a1+a2
endin


;        **************************************************************
;        * Waveguided instruments fade                                *
instr 11; *************************************************************

    idur    =       p3
    iatk    =       p6
    irel    =       p7
    isus    =       idur - iatk - irel

    iamp1   =       ampdb(p4)
    ifq1    =       cpspch(p5)

    kpres   =       3
    krat    =       0.127236
    kvibf   =       6.12723
    kvib    linseg  0, iatk, 0, isus, 1, irel, 1				; amplitude envelope for the vibrato.
    kvamp   =       kvib * 0.01
    kenv1   linseg  0, iatk, iamp1, isus, 0, irel, 0

    a1      wgbow   kenv1, ifq1, kpres, krat, kvibf, kvamp, 2

    kstiff  =       -0.44
    iatt    =       0.1
    idetk   =       0.1
    kngain  =       0.05
    kvibf   =       45; 5.735
    kvamp   =       0.1
    kenv2   linseg  0, iatk, 0, isus, iamp1, irel, 0

    a2      wgclar  kenv1, ifq1*2, kstiff, iatt, idetk, kngain, kvibf, kvamp, 4

    out     a1+a2
endin