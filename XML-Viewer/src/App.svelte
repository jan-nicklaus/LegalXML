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
                <Section title="Kantonsgericht" type="first-instance">
                   <Absatz>Das Kantonsgericht hat die Klage <b>gutgeheissen</b>.</Absatz> 
                </Section>
                <Section title="Obergericht" type="second-instance">
                   <Absatz>Das Obergericht ist auf die Beschwerde nicht eingetreten.</Absatz> 
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
</script>


<div class="prose prose-lg m-4 w-full">
    {#if docType === "Judgment"}
    <h2>Dispositiv</h2>

    <h2>Rubrum</h2>
    {#each xmlTree.getElementsByTagName("Rubrum")[0].getelementsByTagName("Section") as sec}
    <div class={`mt-4 relative rounded-md p-4 bg-${}`}

    <h2>Begründung</h2>
    {#each ["Prozessuales", "Formelles", "Materielles"] as h}
      <details class="collapse bg-base-100 border border-base-300 mt-4" name={`accordion-${h}`} open>
        <summary class="collapse-title font-semibold">{h}</summary>
        <div class="collapse-content">
          {#if xmlMain.getElementsByTagName(h)[0].getElementsByTagName("Section").length < 2}
            {#each xmlMain.getElementsByTagName(h)[0].getElementsByTagName("Section")[0].getElementsByTagName("Absatz") as par}
              <div>{@html par.innerHTML}</div>
            {/each}
          {:else}
            {#each xmlMain.getElementsByTagName(h)[0].getElementsByTagName("Section") as sec, i}
            <details class="collapse bg-base-100 border border-base-300 mt-4" name={`accordion-${h}-${i}`} open>
              <summary class="collapse-title font-semibold">
                {sec.hasAttribute("title") ? sec.getAttribute("title") : "Sektion"}
                {#if sec.hasAttribute("type")}
                  <div class="absolute top-2 right-2 badge badge-accent">
                    {sec.getAttribute("type")}
                  </div>
                {/if}
              </summary>
              <div class="collapse-content">
                {#each sec.getElementsByTagName("Absatz") as par}
                  <div>{@html par.innerHTML}</div>
                {/each}
                </div>
            </details>
            {/each}
          {/if}
        </div>
      </details>
    {/each}
  {/if}
</div>



