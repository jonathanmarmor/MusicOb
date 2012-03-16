\new Voice {

\mark \markup { \override #'(font-name . "Minion Semibold") \override #'(thickness . 0.01) \override #'(box-padding . 0.4) \box { "A" } }
| %  ----------  1 ----------  1 ----------  1 ----------  1 ----------  1
\time 4/4
<d' >2 \f
<a' >4
<cis' >8[
<dis' >8](
| %  ----------  2 ----------  2 ----------  2 ----------  2 ----------  2
\override TextSpanner #'staff-padding = #3.0 \override TextSpanner #'(bound-details left text) = \markup { \override #'(font-name . "Minion Italic") { "Acc" } }
<g' >2-| \startTextSpan
<a' >4)
\override TextScript #'staff-padding = #3.0
r4 \stopTextSpan ^\markup { \override #'(font-name . "Minion Italic") { "A tempo" } }
| %  ----------  3 ----------  3 ----------  3 ----------  3 ----------  3
R1
| %  ----------  4 ----------  4 ----------  4 ----------  4 ----------  4
<bes' >2-_
\grace {
	<f' >16[(-+-^
	<a' >16]
}
<g' >2~)->-- _"Hello, from down under" \breathe
| %  ----------  5 ----------  5 ----------  5 ----------  5 ----------  5
\grace {
	s16
	s16
	s16
}
<g' >2.( \mf
<g'' >4)-. \fermata ^"Hi, from on high!"

\bar "|."
}