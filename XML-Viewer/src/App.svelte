<script>
  let testXML = `<?xml version="1.0" encoding="UTF-8"?>
<Dok doctype="entscheid">
    <Rubrum>
        <Verfahren>
            <Aktenzeichen>6B_650/2025</Aktenzeichen>
            <Parteien>
                <Partei id="b9c06149-2249-4a72-80d8-0c9e84f2d2b2">
                    <Rollen>
                        <Rolle>Beschwerdeführer</Rolle>
                    </Rollen>
                    <Name>ANONYM</Name>
                    <Rechtsvertretung>Rechtsanwältin Angelina Grossenbacher</Rechtsvertretung>
                </Partei>
                <Partei id="fab0cdf0-9cb9-4954-b387-2a19649251f2">
                    <Rollen>
                        <Rolle>Beschwerdegegnerin</Rolle>
                    </Rollen>
                    <Name>Generalstaatsanwaltschaft des Kantons Bern</Name>
                    <Anschrift>Nordring 8, Postfach, 3001 Bern</Anschrift>
                    <Stellvertretung></Stellvertretung>
                    <Rechtsvertretung></Rechtsvertretung>
                </Partei>
            </Parteien>
        </Verfahren>
        <Dokument>
            <DokumentUeberschrift>Urteil</DokumentUeberschrift> //Subtypen?
            <Datum>2025-11-26</Datum> // ... des Entscheids
            <Spruchkoerper>
                <Gericht>Bundesgericht</Gericht>
                <Adresse>Av. du Tribunal federal 29, 1000 Lausanne 14</Adresse> // TBD
                <Kammer>I. strafrechtliche Abteilung</Kammer>
                <Zusammensetzung>
                    <Mitglied role="presiding judge">Muschietti</Mitglied>
                    <Mitglied role="judge">Rüedi</Mitglied>
                    <Mitglied role="judge">Guidon</Mitglied>
                    <Mitglied role="clerk">Matt</Mitglied>
                </Zusammensetzung>
            </Spruchkoerper>
        </Dokument>
    </Rubrum>
    <Main>
        <Dispositiv>
            <DispositivZiffer type="hauptsache" id="ed9b194d-3e88-44d4-9fd3-d86c86a9a44e">Die Beschwerde wird abgewiesen, soweit darauf eingetreten wird.</DispositivZiffer> //Sachentscheid//
            <DispositivZiffer type="kosten" id="74c27c88-af81-4c67-8904-f6d93a8a4341">Der Beschwerdeführer trägt die Gerichtskosten von Fr. 3'000.--.</DispositivZiffer> //Kostenentscheid//
        </Dispositiv>
        <Eroeffnung>
            <EroeffnungZiffer adrid="b9c06149-2249-4a72-80d8-0c9e84f2d2b2" />
            <EroeffnungZiffer adrid="fab0cdf0-9cb9-4954-b387-2a19649251f2" />
            <EroeffnungZiffer adrname="Obergericht des Kantons Bern, 2. Strafkammer" />
        </Eroeffnung>
        <Begruendung>
            <Prozessuales>
                <Section> //Sachverhalt//
                   <Absatz id="d58b97a1-806b-42cb-9bb9-987667820cd4" tag="facts">Am 28. Februar 2024 sprach das Regionalgericht Berner Jura-Seeland B.________ von den Vorwürfen der Veruntreuung und der Irreführung der Rechtspflege frei und seinem amtlichen Verteidiger, Rechtsanwalt A.________, eine Entschädigung von Fr. 10'459.30 zu. Das Obergericht des Kantons Bern, welches die Berufung der Generalstaatsanwaltschaft abwies, reduzierte die erstinstanzliche amtliche Entschädigung am 23. April 2025 auf Fr. 7'170.45. Die Entschädigung im Berufungsverfahren setzte es auf Fr. 2'904.30 fest.</Absatz>
                   <Absatz id="3f25d6a1-7ada-4523-b136-b9b0cc6532cb" tag="facts">Mit Beschwerde in Strafsachen beantragt Rechtsanwalt A.________, ihm seien für das erstinstanzliche Verfahren eine Entschädigung von Fr. 10'459.30 und für das Berufungsverfahren eine solche von Fr. 3'850.20 zuzusprechen. Eventualiter sei die Sache zu neuer Entscheidung an das Obergericht zurückzuweisen.</Absatz> 
                </Section>
            </Prozessuales> //Erwägungen//
            <Formelles>
                <Section>
                   <Absatz id="0fd03e07-50fd-4731-b20d-5e8dc6266106" tag="legal">Die Beschwerde richtet sich gegen einen kantonal letztinstanzlichen Endentscheid (Art. 80 und Art. 90 BGG), worin die Vorinstanz (auch) über die Höhe der amtlichen Entschädigung in beiden kantonalen Verfahren befunden hat. Gemäss Art. 135 Abs. 3 StPO in der am 1. Januar 2024 in Kraft getretenen Fassung kann die amtliche Verteidigung gegen den Entschädigungsentscheid das Rechtsmittel ergreifen, das gegen den Endentscheid zulässig ist. Es handelt sich somit um eine Angelegenheit im Sinne von Art. 78 Abs. 1 BGG. wogegen die Beschwerde in Strafsachen zulässig ist. Der bisherige aArt. 135 Abs. 3 lit. b StPO, welcher zu einer Gabelung des Instanzenzugs führen konnte (vgl. BGE 140 IV 213 E. 1.7), wurde aufgehoben (vgl. Botschaft zur Änderung der Strafprozessordnung vom 28. August 2019, BBl. 2019 6697 S. 6733). Auf die Beschwerde ist - unter Vorbehalt der genügenden Begründung (Art. 42 Abs. 1 und 2 BGG) - einzutreten.</Absatz> 
                    <Absatz id="f5e23436-05c6-4cef-bfdd-d1b0e7a20309" tag="legal">Der Beschwerdeführer rügt, die erstinstanzliche Entschädigung sei nicht mehr Gegenstand des Berufungsverfahrens gewesen, sodass die Vorinstanz darüber nicht habe befinden dürfen. Zudem habe sie das Honorar zu Unrecht nach Art. 135 StPO zu einem tieferen Stundensatz anstatt wie die Erstinstanz nach Art. 429 Abs. 1 lit. a StPO festgesetzt. In diesem Zusammenhang habe die Vorinstanz ferner sein rechtliches Gehör verletzt.</Absatz>
                </Section>
            </Formelles>
            <Materielles>
                <Section tag="ruege">
                    <Absatz id="e6a6b324-0c11-4447-9788-7149becb436f" tag="legal">Im Berufungsverfahren gilt grundsätzlich die Dispositionsmaxime und das Berufungsgericht überprüft das erstinstanzliche Urteil nur in den angefochtenen Punkten (Art. 404 Abs. 1 StPO). Soweit die Einschränkung der Berufung auf einzelne Punkte eindeutig und der Grundsatz der Untrennbarkeit oder inneren Einheit nicht verletzt ist, muss die Einschränkung durch das Berufungsgericht respektiert werden (BGE 147 IV 93 E. 1.5.2; Urteil 6B_1143/2021 vom 11. März 2022 E. 2.2.2; je mit Hinweisen).</Absatz>
                    <Absatz id="bda5afdf-be1e-4452-bdfd-6ba26a058c99">(...)</Absatz>
                </Section>
            </Materielles>
        </Begruendung>
        <Entscheid>Die Beschwerde ist abzuweisen, soweit darauf einzutreten ist. Ausgangsgemäss hat der Beschwerdeführer die Gerichtskosten zu tragen (Art. 66 Abs. 1 BGG).</Entscheid>
    </Main>
</Dok>`;

  let parser = new DOMParser();
  let xmlTree = parser.parseFromString(testXML, "text/xml");
  console.log(xmlTree);
  let xmlMain = xmlTree.getElementsByTagName("Main")[0]; //Main muss existieren
  let xmlBegruendung = xmlMain.getElementsByTagName("Begruendung")[0]; //Begruendung muss existieren
  let tagRegex = /tag="([a-zA-Z\-)]+)"/g;
  let tags = new Set([...testXML.matchAll(tagRegex).map(m => m[1])]);
  let tag_filter = Object.fromEntries([...tags].map(v => [v, true]));
</script>


<div class="w-full flex flex-row h-screen p-4">
  <div class="w-1/3 h-full overflow-y-auto">
    <details class="collapse collapse-plus bg-base-100 border border-base-300" name="accordion-rubrum" open>
          <summary class="collapse-title font-semibold">
            {#if xmlTree.getElementsByTagName("Aktenzeichen").length > 0 && 
              xmlTree.getElementsByTagName("DokumentUeberschrift").length > 0}
              {xmlTree.getElementsByTagName("DokumentUeberschrift")[0].textContent.trim()} 
              {xmlTree.getElementsByTagName("Aktenzeichen")[0].textContent.trim()}
            {:else}
              Rubrum
            {/if}
          </summary>
          <div class="collapse-content">
            {#each xmlTree.getElementsByTagName("Partei") as party, i}
              <details class="collapse collapse-plus bg-base-100 border border-base-300 mb-2" name={`accordion-party-${i}`} open>
                <summary class="collapse-title font-semibold">
                  {#if party.getElementsByTagName("Name").length > 0}
                    {party.getElementsByTagName("Name")[0].textContent.trim()}
                  {:else}
                    Partei {i + 1}
                  {/if}
                </summary>
                <div class="collapse-content">
                  <div class="flex flex-row items-center mb-4">
                    {#each party.getElementsByTagName("Rolle") as role}
                      <div class="badge badge-accent">{role.textContent.trim()}</div>
                    {/each}
                  </div>
                  {#each ["Anschrift", "Stellvertretung", "Rechtsvertretung"] as t}
                    {#if party.getElementsByTagName(t).length > 0 &&
                      party.getElementsByTagName(t)[0].textContent.trim().length > 0}
                      <p><b>{t}</b>: {party.getElementsByTagName(t)[0].textContent.trim()}</p>
                    {/if}
                  {/each}        
                </div>
              </details>
            {/each}
              <details class="collapse collapse-plus bg-base-100 border border-base-300" name={`accordion-doc-info`} open>
                <summary class="collapse-title font-semibold">Dokument</summary>
                <div class="collapse-content">
                  {#if xmlTree.getElementsByTagName("Datum").length > 0}
                    <p>
                      {#if xmlTree.getElementsByTagName("DokumentUeberschrift").length > 0}
                        <b>{xmlTree.getElementsByTagName("DokumentUeberschrift")[0].textContent.trim()}</b> vom 
                      {/if}
                      {new Date(xmlTree.getElementsByTagName("Datum")[0].textContent.trim() + 
                      'T00:00:00').toLocaleDateString('de-CH', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}</p>
                  {/if}
                  {#if xmlTree.getElementsByTagName("Spruchkoerper").length > 0}
                    <p class="mt-2"><b>{xmlTree.getElementsByTagName("Gericht")[0].textContent.trim()}</b>, 
                    {xmlTree.getElementsByTagName("Kammer")[0].textContent.trim()},
                    {xmlTree.getElementsByTagName("Adresse")[0].textContent.trim()}</p>
                    {#each xmlTree.getElementsByTagName("Mitglied") as member}
                      <div class="flex flex-row items-center mt-2">
                        <div class="badge badge-accent mr-2">{member.getAttribute("role")}</div>
                        <span>{member.textContent.trim()}</span>
                      </div>
                    {/each}
                  {/if}
                </div>
              </details>
          </div>
    </details>
    <details class="collapse collapse-plus bg-base-100 border border-base-300 mt-4" name="accordion-filter" open>
          <summary class="collapse-title font-semibold">Filter</summary>
          <div class="collapse-content">
            {#each Object.keys(tag_filter) as k}
              <div class="flex flex-row items-center justify-between w-full mt-2">
                <p>{k}</p>
                <input type="checkbox" class="checkbox" bind:checked={tag_filter[k]} />
              </div>
            {/each}
          </div>
    </details>
  </div>
  <div class="prose prose-lg flex-grow h-full overflow-y-auto ml-4">
      <h2>Begründung</h2>
      {#each xmlBegruendung.children as child}
        <details class="collapse collapse-plus bg-base-100 border border-base-300 mt-4" name={`accordion-${child.tagName}`} open>
          <summary class="collapse-title font-semibold">{child.tagName}</summary>
          <div class="collapse-content">
            {#if xmlMain.getElementsByTagName(child.tagName)[0].getElementsByTagName("Section").length < 2}
              {#each [...xmlMain.getElementsByTagName(child.tagName)[0]
                .getElementsByTagName("Section")[0].getElementsByTagName("Absatz")].filter(
                  par => !par.hasAttribute("tag") || tag_filter[par.getAttribute("tag")]
                ) as par}
                <p>
                  {#if par.hasAttribute("tag")}
                    <span class="badge badge-accent">
                      {par.getAttribute("tag")}
                    </span>
                  {/if}  
                  {@html par.innerHTML}
                </p>
              {/each}
            {:else}
              {#each xmlMain.getElementsByTagName(child.tagName)[0].getElementsByTagName("Section") as sec, i}
              <details class="collapse collapse-plus bg-base-100 border border-base-300 mt-4" name={`accordion-${child.tagName}-${i}`} open>
                <summary class="collapse-title font-semibold">
                  {sec.hasAttribute("title") ? sec.getAttribute("title") : "Sektion"}
                  {#if sec.hasAttribute("tag")}
                    <div class="absolute top-2 right-2 badge badge-accent">
                      {sec.getAttribute("tag")}
                    </div>
                  {/if}
                </summary>
                <div class="collapse-content">
                  {#each [...sec.getElementsByTagName("Absatz")].filter(par => !par.hasAttribute("tag") || tag_filter[par.getAttribute("tag")]) as par}
                    {#if par.hasAttribute("tag")}
                      <div class="badge badge-accent">
                        {par.getAttribute("tag")}
                      </div>
                    {/if}
                    <div>{@html par.innerHTML}</div>
                  {/each}
                  </div>
              </details>
              {/each}
            {/if}
          </div>
        </details>
      {/each}
  </div>

</div>


