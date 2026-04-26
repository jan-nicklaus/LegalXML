# LegalXML

Dieses Repository beinhaltet das Ergebnis der Challenge *Eigenes Dateiformat für Schweizer Rechtsschriften*: XML als Scharnier für den Abgleich von Rechtsdokumenten. Rechtsschriften sind Eingaben an das Gericht. Ähnlich wie Urteile folgen sie einem einheitlichen Aufbau (Rechtsbegehren, Formelles, Prozessuales, Materielles). 

*Sinn und Zweck, wieso ein strukturiertes Scharnierformat?*
Rechtsschriften und Urteile bestehen mehrheitlich aus Text. Im Verlauf eines Verfahrens werden diese Texte zwischen den Beteiligten ausgetauscht; es wird wechselseitig auf sie Textteile Bezug genommen — und zwar nicht auf beliebige Stellen, sondern auf solche, die einen engeren inhaltlichen Bezug haben. Sachverhaltselemente korrespondieren mit anderen Sachverhaltselementen, rechtliche Argumente werden gegenüber anderen rechtlichen Argumenten erwidert.

Für diesen Austausch und den damit verbundenen Abgleich wird ein Mapping benötigt, für das Mapping wäre eine minimale Struktur hilfreich. Dabei ist unerheblich, ob die Texte bzw. Textteile originär strukturiert entstehen oder ob sie aus anderen Dateiformaten wie PDF-Formate abgeleitet werden. Entscheidend ist, dass die typischen Bezüge maschinell nachvollziehbar werden — und damit auch, dass die Strukturierung bewusst minimal ausgestaltet wird: gerade so präzise wie nötig, nicht so detailliert wie möglich. Das Ziel ist also nicht, Rechtsschriften und Entscheide vollständig in strukturierter Form abzubilden.

Urteile und Rechtsschriften eignen sich deshalb sehr gut für eine Strukturierung mit Hilfe von XML. Beispiele dazu, wie wir uns eine Strukturierung von Schweizer Rechtsschriften und Urteilen vorstellen, finden sich im Ordner *Beispiele*. Als Datengrundlage dient uns das Urteil des Bundesgerichts mit Aktenzeichen 6B_650/2025 vom 26. November 2025. Dank der Plattform entscheidsuche.ch liegt uns in diesem Fall sogar eine Rechtsschrift vor. Daneben finden sich weitere Beispiele aus sog. Moot Courts (= simulierte Gerichtsverhandlung).

*Was sich mit strukturierten Daten erreichen lässt*
- Für Rechtsanwender: Bessere Auffindbarkeit durch Metadaten und einheitliche Identifier
- Für Entwickler: Sauber strukturierte Dokumente, mit denen sich Applikation mit semantischer Funktionalität entwickeln lassen
- Für die Forschung: Saubere Metadaten liefern eine Datengrundlage für die Forschung. Siehe auch [Federal Supreme Court Dataset](https://zenodo.org/records/11092977)