<script>
    import { get } from "svelte/store";

  let testXML = `<xml type="judgment">
    <meta id="doctype">Judgment</meta>
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
                <Section title="Test-Titel" type="first-instance">
                   <Absatz>Das Kantonsgericht hat die Klage <b>gutgeheissen</b>.</Absatz> 
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
let docType = xmlTree.getElementById("doctype").textContent.trim();
let xmlMain = xmlTree.getElementsByTagName("Main")[0]; //Main muss existieren

function getBGColor(sec) {
  if(!sec.hasAttribute("type")) return "slate-200";
  switch(sec.getAttribute("type")) {
    case "first-instance": return "black"
  }
}
</script>


<div class="prose prose-lg m-4 w-full">
    {#if docType === "Judgment"}
    <h2>Dispositiv</h2>

    <h2>Rubrum</h2>
    {#each xmlTree.getElementsByTagName("Rubrum")[0].getelementsByTagName("Section") as sec}
    <div class={`mt-4 relative rounded-md p-4 bg-${}`}

    <h2>Begründung</h2>
    <h3>Prozessuales</h3>
    {#each xmlMain.getElementsByTagName("Prozessuales")[0].getElementsByTagName("Section") as sec}
      <div class={`mt-4 relative rounded-md bg-${getBGColor(sec)}`}>
        {#if sec.hasAttribute("type")}
          <div class="absolute top-2 right-2 badge badge-accent">
            {sec.getAttribute("type")}
          </div>
        {/if}
        {#if sec.hasAttribute("title")}
          <h4>{sec.getAttribute("title")}</h4>
        {/if}
        {#each sec.getElementsByTagName("Absatz") as par}
          <div>{@html par.innerHTML}</div>
        {/each}
      </div>
    {/each}
  {/if}
</div>



