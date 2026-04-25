<script>
  let testXML = `<xml>
    <Rubrum>
        <Aktenzeichen></Aktenzeichen>
        <EntscheidTyp>Urteil</EntscheidTyp>
        <EntscheidDatum></EntscheidDatum>
        <Spruchkoerper>
            <Gericht></Gericht>
            <Kammer></Kammer>
            <Zusammensetzung>
                <Mitglied role="judge">Mustermann</Mitglied>
            </Zusammensetzung>
        </Spruchkoerper>
        <Parteien>
            <Partei>
                <Rollen>
                    <Rolle>Gesuchsteller</Rolle>
                    <Rolle>Beschwerdeführer</Rolle>
                </Rollen>
                <Name></Name>
                <Anschrift></Anschrift>
                <Stellvertretung></Stellvertretung>
                <Rechtsvertretung></Rechtsvertretung>
            </Partei>
        </Parteien>
    </Rubrum>
    <Main>
        <Dispositiv>

        </Dispositiv>
        <Eroeffnung></Eroeffnung>
        <Begruendung>
            <Prozessuales>
                <Section>
                   <Absatz></Absatz> 
                </Section>
            </Prozessuales>
            <Formelles>
                <Section>
                   <Absatz></Absatz> 
                </Section>
            </Formelles>
            <Materielles>
                <Section type="ruege">
                    <Absatz>Die Klägerin führt aus</Absatz>
                </Section>
            </Materielles>
        </Begruendung>
    </Main>
</xml>`;

let parser = new DOMParser();
let xmlTree = parser.parseFromString(testXML, "text/xml");
</script>




<h1 class="text-red-400">Test</h1>
<button class="btn">Test</button>
