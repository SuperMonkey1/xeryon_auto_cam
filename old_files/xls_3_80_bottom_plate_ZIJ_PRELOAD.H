  BEGIN PGM ZIJ_PRELOAD MM
  ;  
  ; WERKSTUK: BODY 1103_080_001_G8 - BEWERKING ZIJ_PRELOAD 
  ;  
  BLK FORM 0.1 Z X-40 Y+0 Z-47.6
  BLK FORM 0.2 X+40 Y+12.3 Z+0
  ;  
  M36 ; SPAANAFVOER AAN 
  M38 ; AFZUIGING AAN 
  ;  
  ; OPLETTEN: UITSTULPING M3 CHECKEN, EVENTUEEL TAP VERVANGEN 
  ; NOG AAN TE PASSEN: 
  ; TYPE BOOR EVT. VERVANGEN NAAR ATORN 12280474 (GOEDKOPER)??? 
  ;  
  ; ------------------------------- 
  ; #0 - OPMETEN REFERENTIE X-AS 
  ; PROGRAMMA NIET ONDERBREKEN WANT DAN NULPUNT NIET MEER JUIST 
  ; ------------------------------- 
  ;  
  CYCL DEF 7.0 NULPUNT
  CYCL DEF 7.1 X+0
  ;  
  TOOL CALL 7 Z ; MEETPROBE 
  ;  
  TCH PROBE 426 METING RAND BUITEN ~
    Q263=+40  ;1E PUNT 1E AS ~
    Q264=+3   ;1E PUNT IN 2E AS ~
    Q265=-40  ;2e PUNT 1e AS ~
    Q266=+3   ;2e PUNT 2e AS ~
    Q272=1    ;MEETASSEN ~
    Q261=-3   ;MEETHOOGTE ~
    Q320=2    ;VEILIGHEIDSAFSTAND ~
    Q260=+50  ;VEILIGE HOOGTE ~
    Q311=80   ;NOMINALE LENGTE ~
    Q288=80.1 ;MAXIMALE MAAT ~
    Q289=79.9 ;MINIMALE MAAT ~
    Q281=1    ;MEETPROTOCOL ~
    Q309=1    ;PGM-STOP BIJ FOUT ~
    Q330=0    ;GEREEDSCHAPS-NUMMER
  ;  
  CYCL DEF 7.0 NULPUNT
  CYCL DEF 7.1 X+Q157
  ;   
  ; ------------------------------- 
  ; #1 - CENTERBOREN 
  ; ------------------------------- 
  ;  
  TOOL CALL 45 Z S10000 ; CENTERBOOR_142GR - WNT 10 704 003 
  M3 M8
  CYCL DEF 200 BOREN ~
    Q200=2    ;VEILIGHEIDSAFSTAND ~
    Q201=-0.51 ;DIEPTE ~
    Q206=200  ;AANZET DIEPTEVERPL. ~
    Q202=0.51 ;DIEPTEVERPLAATSING ~
    Q210=0    ;STILSTANDSTIJD BOVEN ~
    Q203=+0   ;COORD. OPPERVLAK ~
    Q204=25   ;2e VEILIGHEIDSAFST. ~
    Q211=0.5  ;STILSTANDSTIJD ONDER
  L X+0 Y+2.1 Z+25 F MAX M99
  ;   
  ; ------------------------------- 
  ; #2 - BOREN 
  ; ------------------------------- 
  ;  
  ; #2.1 - GAT PRELOAD 
  ; EERST TRAAG AANBOREN VOOR BETERE CENTRERING, DAN SNEL BOREN OM  ~
    BRAAMVORMING AAN UITGAANDE KANT TE VERMINDEREN 
  ;  
  TOOL CALL 26 Z S10000 ; BOOR D2.6 - WNT 11 629 02600 
  M3 M8
  CYCL DEF 200 BOREN ~
    Q200=2    ;VEILIGHEIDSAFSTAND ~
    Q201=-3   ;DIEPTE ~
    Q206=200  ;AANZET DIEPTEVERPL. ~
    Q202=1.5  ;DIEPTEVERPLAATSING ~
    Q210=0    ;STILSTANDSTIJD BOVEN ~
    Q203=+0   ;COORD. OPPERVLAK ~
    Q204=25   ;2e VEILIGHEIDSAFST. ~
    Q211=0    ;STILSTANDSTIJD ONDER
  L X+0 Y+2.1 Z+25 F MAX M99
  ;    
  TOOL CALL 26 Z S20000 ; BOOR D2.6 - WNT 11 629 02600 
  M3 M8
  CYCL DEF 200 BOREN ~
    Q200=2    ;VEILIGHEIDSAFSTAND ~
    Q201=-14.77 ;DIEPTE ~
    Q206=200  ;AANZET DIEPTEVERPL. ~
    Q202=1.5  ;DIEPTEVERPLAATSING ~
    Q210=0    ;STILSTANDSTIJD BOVEN ~
    Q203=-3   ;COORD. OPPERVLAK ~
    Q204=25   ;2e VEILIGHEIDSAFST. ~
    Q211=0    ;STILSTANDSTIJD ONDER
  L X+0 Y+2.1 Z+25 F MAX M99
  ;   
  ; #1.2 - PILOOTGATEN SLEUF ONDER ENCODER 
  ; (DIT VOOROMT CHATTERING VAN FREES D2 LANG IN HOEKEN SLEUF) 
  ;  
  TOOL CALL 23 Z S12000 ; BOOR D2 - WNT 11 770 02000 
  M3 M8
  CYCL DEF 200 BOREN ~
    Q200=2    ;VEILIGHEIDSAFSTAND ~
    Q201=-3.5 ;DIEPTE ~
    Q206=400  ;AANZET DIEPTEVERPL. ~
    Q202=2    ;DIEPTEVERPLAATSING ~
    Q210=0    ;STILSTANDSTIJD BOVEN ~
    Q203=-10.5 ;COORD. OPPERVLAK ~
    Q204=25   ;2e VEILIGHEIDSAFST. ~
    Q211=0    ;STILSTANDSTIJD ONDER
  L X-13 Y+7.3 Z+25 F MAX M99
  FN 0: Q201 = -2.5 ; DIEPTE 
  L X+13.85 Y+7.3 Z+25 F MAX M99
  ;  
  ; ------------------------------- 
  ; #2 - TAPPEN 
  ; ------------------------------- 
  ;  
  TOOL CALL 63 Z S500 ; TAP M3 - WNT 23 122 030 
  M3 M8
  CYCL DEF 209 SCHRDR.BOR. SPAANBR. ~
    Q200=2    ;VEILIGHEIDSAFSTAND ~
    Q201=-7.5 ;DRAADDIEPTE ~
    Q239=+0.5 ;SPOED ~
    Q203=+0   ;COORD. OPPERVLAK ~
    Q204=25   ;2e VEILIGHEIDSAFST. ~
    Q257=1.5  ;BOORDPTE SPAANBREUK ~
    Q256=0    ;TERUGTR.HGT SPAANBR. ~
    Q336=+0   ;HOEK SPIL
  L X+0 Y+2.1 Z+25 F MAX M99
  ;  
  ; ------------------------------- 
  ; #3 - NABOREN D2.6 
  ; ------------------------------- 
  ;  
  TOOL CALL 26 Z S20000 ; BOOR D2.6 - WNT 11 629 02600 
  M3 M8
  CYCL DEF 200 BOREN ~
    Q200=2    ;VEILIGHEIDSAFSTAND ~
    Q201=-10.5 ;DIEPTE ~
    Q206=500  ;AANZET DIEPTEVERPL. ~
    Q202=10.5 ;DIEPTEVERPLAATSING ~
    Q210=0    ;STILSTANDSTIJD BOVEN ~
    Q203=+0   ;COORD. OPPERVLAK ~
    Q204=25   ;2e VEILIGHEIDSAFST. ~
    Q211=1    ;STILSTANDSTIJD ONDER
  L X+0 Y+2.1 Z+25 F MAX M99
  ;  
  ; ------------------------------- 
  ; #4 - AFSCHUINEN 
  ; ------------------------------- 
  ;  
  TOOL CALL 46 Z S5000 ; CENTERBOOR D6 - WNT 10 702 006 
  M3
  CYCL DEF 200 BOREN ~
    Q200=1    ;VEILIGHEIDSAFSTAND ~
    Q201=-1.6 ;DIEPTE ~
    Q206=200  ;AANZET DIEPTEVERPL. ~
    Q202=1.6  ;DIEPTEVERPLAATSING ~
    Q210=0    ;STILSTANDSTIJD BOVEN ~
    Q203=+0   ;COORD. OPPERVLAK ~
    Q204=25   ;2e VEILIGHEIDSAFST. ~
    Q211=0    ;STILSTANDSTIJD ONDER
  L X+0 Y+2.1 Z+25 F MAX M99
  ;  
  ; ------------------------------- 
  ; #5 - FREZEN SLEUF ONDER ENCODER/VRIJMAKEN MOTOROPHANGING 
  ; ------------------------------- 
  ;  
  TOOL CALL 32 Z S18000 ; FREES D2 LANG - WNT 53 617 02400 
  M3 M8
  ; SLEUF NIET-KABELZIJDE 
  CYCL DEF 210 SLEUF PENDELEND ~
    Q200=1    ;VEILIGHEIDSAFSTAND ~
    Q201=-4.2 ;DIEPTE ~
    Q207=750  ;AANZET FREZEN ~
    Q202=0.2  ;DIEPTEVERPLAATSING ~
    Q215=1    ;BEWERKINGSOMVANG ~
    Q203=-10.5 ;COORD. OPPERVLAK ~
    Q204=25   ;2e VEILIGHEIDSAFST. ~
    Q216=-8.4 ;MIDDEN 1e AS ~
    Q217=+7.3 ;MIDDEN 2e AS ~
    Q218=11.2 ;LENGTE 1e ZIJKANT ~
    Q219=2.02 ;LENGTE 2e ZIJKANT ~
    Q224=+0   ;ROTATIEPOSITIE ~
    Q338=0    ;AANZET NABEWERKING
  ; SLEUF KABELZIJDE 
  ; (Q218=10.6 IPV 10.8 OM CHATTERING IN HOEKEN TE VERMIJDEN) 
  L X+Q216 Y+Q217 Z+25 F MAX M99
  CYCL DEF 210 SLEUF PENDELEND ~
    Q200=1    ;VEILIGHEIDSAFSTAND ~
    Q201=-3.2 ;DIEPTE ~
    Q207=750  ;AANZET FREZEN ~
    Q202=0.2  ;DIEPTEVERPLAATSING ~
    Q215=1    ;BEWERKINGSOMVANG ~
    Q203=-10.5 ;COORD. OPPERVLAK ~
    Q204=25   ;2e VEILIGHEIDSAFST. ~
    Q216=+9.45 ;MIDDEN 1e AS ~
    Q217=+7.3 ;MIDDEN 2e AS ~
    Q218=10.6 ;LENGTE 1e ZIJKANT ~
    Q219=2.02 ;LENGTE 2e ZIJKANT ~
    Q224=+0   ;ROTATIEPOSITIE ~
    Q338=0    ;AANZET NABEWERKING
  L X+Q216 Y+Q217 Z+25 F MAX M99
  ;  
  L X-265 Z+200 F MAX
  ;  
  STOP M30
  ;  
  END PGM ZIJ_PRELOAD MM
