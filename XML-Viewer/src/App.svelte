<script>
  let xmlTree1, xmlTree2, xmlMain1, xmlMain2, xmlBegruendung1, xmlBegruendung2;
  let tags, tag_filter, old_ref_id, reverse_ref_dict;
  let xml1, xml2;
  function load_xml_files(xml1, xml2) {
    let parser = new DOMParser();
    xmlTree1 = parser.parseFromString(xml1, "text/xml");
    xmlMain1 = xmlTree1.getElementsByTagName("Main")[0]; //Main muss existieren
    xmlBegruendung1 = xmlMain1.getElementsByTagName("Begruendung")[0]; //Begruendung muss existieren
    xmlTree2 = parser.parseFromString(xml2, "text/xml");
    xmlMain2 = xmlTree2.getElementsByTagName("Main")[0]; //Main muss existieren
    xmlBegruendung2 = xmlMain2.getElementsByTagName("Begruendung")[0]; //Begruendung muss existieren
    

    let tagRegex = /tag="([a-zA-Z\-)]+)"/g;
    tags = new Set([...xml1.matchAll(tagRegex).map(m => m[1]), ...xml2.matchAll(tagRegex).map(m => m[1])]);
    tag_filter = Object.fromEntries([...tags].map(v => [v, true]));

    old_ref_id = "";
    reverse_ref_dict = {}
    xmlTree2.querySelectorAll("Absatz[ref]").forEach(
      par => {
        if(!reverse_ref_dict[par.getAttribute("ref")]) {
          reverse_ref_dict[par.getAttribute("ref")] = [par.getAttribute("id")];
        }
        else {
          reverse_ref_dict[par.getAttribute("ref")].push(par.getAttribute("id"));
        }
      }
    )
  }
  function scrollAndMark(ref_id) {
    let par = document.getElementById(ref_id);

    let el = par;
    while (el) {
      if (el.tagName === 'DETAILS') el.open = true;
      el = el.parentElement;
    }
    par.scrollIntoView();

    if(old_ref_id.length > 0) {
      document.getElementById(old_ref_id).className = document.getElementById(old_ref_id).className.replace(" bg-yellow-200", "");
    }
    par.className += " bg-yellow-200";
    old_ref_id = ref_id;
  }
  function setXML(num, file) {
    if(!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
      if(num === 1) xml1 = e.target.result;
      else load_xml_files(xml1, e.target.result);
    };
    reader.readAsText(file);
  }
</script>


<div class="w-screen flex flex-row h-screen p-4 justify-center">
  {#if xmlTree1}
    <div class="w-1/4 h-full overflow-y-auto">
      <details class="collapse collapse-plus bg-base-100 border border-base-300" name="accordion-rubrum" open>
            <summary class="collapse-title font-semibold">
              {#if xmlTree1.getElementsByTagName("Aktenzeichen").length > 0 && 
                xmlTree1.getElementsByTagName("DokumentUeberschrift").length > 0}
                {xmlTree1.getElementsByTagName("DokumentUeberschrift")[0].textContent.trim()} 
                {xmlTree1.getElementsByTagName("Aktenzeichen")[0].textContent.trim()}
              {:else}
                Rubrum
              {/if}
            </summary>
            <div class="collapse-content">
              {#each xmlTree1.getElementsByTagName("Partei") as party, i}
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
                    {#if xmlTree1.getElementsByTagName("Datum").length > 0}
                      <p>
                        {#if xmlTree1.getElementsByTagName("DokumentUeberschrift").length > 0}
                          <b>{xmlTree1.getElementsByTagName("DokumentUeberschrift")[0].textContent.trim()}</b> vom 
                        {/if}
                        {new Date(xmlTree1.getElementsByTagName("Datum")[0].textContent.trim() + 
                        'T00:00:00').toLocaleDateString('de-CH', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}</p>
                    {/if}
                    {#if xmlTree2.getElementsByTagName("Spruchkoerper").length > 0}
                      <p class="mt-2"><b>{xmlTree1.getElementsByTagName("Gericht")[0].textContent.trim()}</b>, 
                      {xmlTree2.getElementsByTagName("Kammer").length > 0 ? xmlTree2.getElementsByTagName("Kammer")[0].textContent.trim() : ""},
                      {xmlTree2.getElementsByTagName("Adresse").length > 0 ? xmlTree2.getElementsByTagName("Adresse")[0].textContent.trim() : ""}</p>
                      {#each xmlTree1.getElementsByTagName("Mitglied") as member}
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
    <div class="flex-grow h-full ml-4 flex flex-row">
        {#each [[xmlBegruendung1, xmlMain1, xmlTree1], [xmlBegruendung2, xmlMain2, xmlTree2]] as [xmlBegruendung, xmlMain, xmlTree], j}
          <div class="h-full overflow-y-auto w-1/2 mx-2 prose prose-lg ">
            {#each xmlBegruendung.children as child}
              <details class="collapse collapse-plus bg-base-100 border border-base-300 mt-4" name={`accordion-${j}-${child.tagName}`} open>
                <summary class="collapse-title font-semibold">{child.tagName}</summary>
                <div class="collapse-content">
                  {#if xmlMain.getElementsByTagName(child.tagName)[0].getElementsByTagName("Section").length < 2}
                    {#each [...xmlMain.getElementsByTagName(child.tagName)[0]
                      .getElementsByTagName("Section")[0].getElementsByTagName("Absatz")].filter(
                        par => !par.hasAttribute("tag") || tag_filter[par.getAttribute("tag")]
                      ) as par}
                      <p id={par.getAttribute("id")} class="p-2 rounded-lg" class:bg-red-200={
                            j === 0 &&
                            (!par.hasAttribute("id") ||
                            !reverse_ref_dict[par.getAttribute("id")])
                          }>
                        {#if par.hasAttribute("tag")}
                          <span class="badge badge-accent">
                            {par.getAttribute("tag")}
                          </span>
                        {/if}  
                        {@html par.innerHTML}
                        {#if par.hasAttribute("ref")}
                          <button class="btn btn-warning btn-sm" onclick={() => scrollAndMark(par.getAttribute("ref"))}>=></button>
                        {/if}
                        {#if reverse_ref_dict[par.getAttribute("id")]}
                          {#each reverse_ref_dict[par.getAttribute("id")] as id}
                            <button class="btn btn-warning btn-sm" onclick={() => scrollAndMark(id)}>=></button>
                          {/each}
                        {/if}
                      </p>
                    {/each}
                  {:else}
                    {#each xmlMain.getElementsByTagName(child.tagName)[0].getElementsByTagName("Section") as sec, i}
                    <details class="collapse collapse-plus bg-base-100 border border-base-300 mt-4" name={`accordion-${child.tagName}-${i}-${j}`} open>
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
                          <p id={par.getAttribute("id")} class="p-2 rounded-lg" class:bg-red-200={
                            !par.hasAttribute("id") ||
                            !reverse_ref_dict[par.getAttribute("id")]
                          }>
                          {#if par.hasAttribute("tag")}
                            <span class="badge badge-accent">
                              {par.getAttribute("tag")}
                            </span>
                          {/if}
                          {@html par.innerHTML}
                          {#if par.hasAttribute("ref")}
                            <button class="btn btn-warning btn-sm" onclick={() => scrollAndMark(par.getAttribute("ref"))}>=></button>
                          {/if}
                          {#if reverse_ref_dict[par.getAttribute("id")]}
                          {#each reverse_ref_dict[par.getAttribute("id")] as id}
                            <button class="btn btn-warning btn-sm" onclick={() => scrollAndMark(id)}>=></button>
                          {/each}
                        {/if}
                          </p>
                        {/each}
                        </div>
                    </details>
                    {/each}
                  {/if}
                </div>
              </details>
            {/each}
        </div>
        {/each}
    </div>
  {:else}
    <div class="card w-96 bg-base-100 card-lg shadow-sm place-self-center justify-self-center">
      <div class="card-body">
        <h2 class="card-title">XML-Vergleich</h2>
        <p>Bitte laden Sie zwei XML-Dateien hoch, in der zeitlichen Reihenfolge.</p>
        <div class="justify-end card-actions flex flex-row items-center justify-between">
          <input type="file" class="file-input file-input-secondary" onchange={e => setXML(1, e.target.files[0])} />
          <input type="file" class="file-input file-input-primary" onchange={e => setXML(2, e.target.files[0])} />
        </div>
      </div>
    </div>
  {/if}
</div>


