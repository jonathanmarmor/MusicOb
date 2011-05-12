\version "2.12.3"
% Éditions musique SISYPHE

#(ly:set-option 'point-and-click #f) % switch off hyperlinks from noteheads to lilypond source files
#(set-global-staff-size 20) % 20 is default

\paper {
%	annotate-spacing = ##t
	#(set-paper-size "arch a")
%   #(set-paper-size "letter")
%	#(define top-margin (* 0.8 in)) % original margin requested by Andre
	#(define top-margin (* 0.6 in))
%	#(define bottom-margin (* 0.8 in)) % original margin requested by Andre
	#(define bottom-margin (* 0.4 in))
	#(define left-margin (* 0.8 in))
	#(define line-width (* 7.4 in))

	page-top-space = 0.0\in
	foot-separation = 0.25\in
	head-separation = 0.0\in
	after-title-space = 0.0\in
	between-title-space = 0.0\in
%	horizontal-shift = 0.0\in
%	between-system-padding = 7\cm % forces one system per page when staff size is 20 
    between-system-padding = 4\mm % Default is 4mm
%	between-system-padding = #1
%	between-system-space = 3\cm %#30 Changing this doesn't appear to do anything
	ragged-bottom = ##f
	ragged-last-bottom = ##f
	first-page-number = 3
	print-first-page-number = ##t

	bookTitleMarkup = \markup {	
		\column {
			\fill-line {
				\line {
					\override #'(font-name . "Granjon") 
					\override #'(font-size . 12) 
					{ \fromproperty #'header:maintitle }
				}				
			}
			\fill-line {
				\line { \null }
				\line { \null }
				\line {
					\override #'(font-name . "Granjon Bold") 
					{ \fromproperty #'header:thecomposer }
				}
			}
		}
	}
	scoreTitleMarkup = \markup {
		\column {
			\fill-line {
				\line {
					\override #'(font-name . "Granjon Bold")
					\override #'(font-size . 10) 
					{ \fromproperty #'header:movementtitle }
				}				
			}
			\line { \null }
		}
	}
	oddHeaderMarkup = \markup {
		\on-the-fly #not-first-page {
			\column {
				\fill-line {
					{ 
						\override #'(font-name . "Granjon Bold")
						\override #'(font-size . 1)
						{ " " }
					}
					{ 
						\override #'(font-name . "Granjon Bold")
						\override #'(font-size . 2)
						{ \fromproperty #'header:instrumentname }
					}
					{ 
						\override #'(font-name . "Granjon Bold")
						\override #'(font-size . 1)
						{ \on-the-fly #print-page-number-check-first \fromproperty #'page:page-number-string }
					}						
				}
%				\line { \null }
				\line { \null }
			}
		}
		\column {
			\fill-line {
				\override #'(font-name . "Granjon Bold")
				\override #'(font-size . 2)
				{ \fromproperty #'header:instrumentname }
			}
%			\line { \null }
			\line { \null }
		}
	}
	evenHeaderMarkup = \markup {
		\on-the-fly #not-first-page {
			\column {
				\fill-line {
					{ 
						\override #'(font-name . "Granjon Bold")
						\override #'(font-size . 1)
						{ \on-the-fly #print-page-number-check-first \fromproperty #'page:page-number-string }
					}
					{ 
						\override #'(font-name . "Granjon Bold")
						\override #'(font-size . 2)
						{ \fromproperty #'header:instrumentname }
					}
					{ 
						\override #'(font-name . "Granjon Bold")
						\override #'(font-size . 1)
						{ " " }
					}						
				}
%				\line { \null }
				\line { \null }
			}
		}
		\column {
			\fill-line {
				\override #'(font-name . "Granjon Bold")
				\override #'(font-size . 2)
				{ \fromproperty #'header:instrumentname }
			}
%			\line { \null }
			\line { \null }
		}
	}
	oddFooterMarkup = \markup { 
		\on-the-fly #first-page {
			\fill-line {
				\column {
					%\line { \null }
					\line { \null }
					\line { \override #'(font-name . "Granjon Bold") { \char ##x00A9 "2010 Éditions musique SISYPHE" } }
					\line { \override #'(font-name . "Granjon Bold") { "Vancouver, Canada" } }
					\line { \override #'(font-name . "Granjon Bold") { "emsis.ca" } }
				}
				\center-column {
					%\line { \null }
					\line { \null }
					\line { \null }
					\line { \null }
					\line { \override #'(font-name . "Granjon Bold") { "EMSIS no. 1234567" } }
				}
				\right-column {
					%\line { \null }
					\line { \null }
					\line { \override #'(font-name . "Granjon Bold") { "Tous droits réservés pour tous pays" } }
					\line { \override #'(font-name . "Granjon Bold") { "All rights reserved all countries" } }
					\line { \override #'(font-name . "Granjon Bold") { "Imprimé au Canada - Printed in Canada" } }
				}
			}				
		}
		\column {
			%\line { \null }
			\line { \null }
			\line { \null }
			\line { \null }
			\fill-line { \override #'(font-name . "Granjon Bold") { "EMSIS no. 1234567" } }
		}
	}
	evenFooterMarkup = \markup { 
		\column {
			%\line { \null }
			\line { \null }
			\line { \null }
			\line { \null }
			\fill-line { \override #'(font-name . "Granjon Bold") { "EMSIS no. 1234567" } }
		}
	}
}

\book {
	\header { 
		maintitle = "Test Piece"
		thecomposer = "Jonathan Marmor"
		tagline = ""
	}

	\bookpart {
		\header { 
			movementtitle = "Amsterdam" 
			instrumentname = "katie"
		}
		\score {
			<<
				\set Score.autoBeaming = ##f
				#(set-accidental-style 'modern 'Score)
				\override Score.Stem #'stemlet-length = #0.75
				\override Score.PaperColumn #'keep-inside-line = ##t
				\tempo 4 = 60

			\new Staff {
				\numericTimeSignature
				\set Staff.instrumentName = \markup { \override #'(font-name . "Granjon Bold") { "Clarinet" } }
				\set Staff.shortInstrumentName = \markup { \override #'(font-name . "Granjon Bold") { \hcenter-in #5 "cl" } }
				\set Staff.midiInstrument = #"clarinet"
				\set Staff.extraNatural = ##f
				\clef treble
				\override TextScript #'staff-padding = #2.0
				\override Staff.VerticalAxisGroup #'minimum-Y-extent = #'(-5 . 5.5)  % sets minimum space between staves within a system
				\transpose c bes,
				\include "./parts_music/katie/mv1_music.ly"
			}
			>>
			\layout { }
            \midi { }
		}
	}

	\bookpart {
		\header { 
			movementtitle = "Beirut" 
			instrumentname = "katie"
		}
		\score {
			<<
				\set Score.autoBeaming = ##f
				#(set-accidental-style 'modern 'Score)
				\override Score.Stem #'stemlet-length = #0.75
				\override Score.PaperColumn #'keep-inside-line = ##t
				\tempo 4 = 85

			\new Staff {
				\numericTimeSignature
				\set Staff.instrumentName = \markup { \override #'(font-name . "Granjon Bold") { "Clarinet" } }
				\set Staff.shortInstrumentName = \markup { \override #'(font-name . "Granjon Bold") { \hcenter-in #5 "cl" } }
				\set Staff.midiInstrument = #"clarinet"
				\set Staff.extraNatural = ##f
				\clef treble
				\override TextScript #'staff-padding = #2.0
				\override Staff.VerticalAxisGroup #'minimum-Y-extent = #'(-5 . 5.5)  % sets minimum space between staves within a system
				\transpose c bes,
				\include "./parts_music/katie/mv2_music.ly"
			}
			>>
			\layout { }
            \midi { }
		}
	}
}