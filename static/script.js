const btn = document.getElementById('btn')
const queryInput = document.getElementById('query')
const resultsEl = document.getElementById('results')
const chips = document.getElementById('chips')

let localMovies = null

async function loadLocalMovies(){
  if(localMovies) return localMovies
  // try both possible static paths
  const paths = ['/data/movies.json', '/static/data/movies.json']
  for(const p of paths){
    try{
      const res = await fetch(p)
      if(!res.ok) continue
      localMovies = await res.json()
      return localMovies
    }catch(_){/* try next */}
  }
  localMovies = []
  return localMovies
}

async function doSearch(q){
  const query = (q || queryInput.value || '').trim()
  if(!query) return
  resultsEl.innerHTML = '<p class="meta">Searching...</p>'
  try{
    const res = await fetch(`/api/search?query=${encodeURIComponent(query)}`)
    if(!res.ok) throw new Error('Search failed')
    const data = await res.json()
    if(data && data.results && data.results.length>0){
      renderResults(data.results)
      return
    }
    // no results from API - fallback to local filtering
    const local = await loadLocalMovies()
    const ql = query.toLowerCase()
    const filtered = local.filter(m => (m.genres||'').toLowerCase().includes(ql) || (m.title||'').toLowerCase().includes(ql))
    renderResults(filtered.slice(0,12))
  }catch(e){
    // on any error, attempt client-side filtering
    const local = await loadLocalMovies()
    const ql = query.toLowerCase()
    const filtered = local.filter(m => (m.genres||'').toLowerCase().includes(ql) || (m.title||'').toLowerCase().includes(ql))
    if(filtered.length) renderResults(filtered.slice(0,12))
    else resultsEl.innerHTML = `<p class="meta">Error: ${e.message}</p>`
  }
}

function renderResults(items){
  if(!items || items.length===0){
    resultsEl.innerHTML = '<p class="meta">No results found.</p>'
    return
  }
  resultsEl.innerHTML = ''
  items.forEach(it=>{
    const card = document.createElement('div')
    card.className = 'card'
    const poster = it.poster || (`https://via.placeholder.com/300x420/111111/ffffff?text=${encodeURIComponent(it.title)}`)
    card.innerHTML = `
      <img class="poster" src="${poster}" alt="${it.title} poster" />
      <h3>${it.title} <span class="meta">(${it.year || ''})</span></h3>
      <div class="meta">Genres: ${it.genres}</div>
      <div class="desc">${it.description}</div>
    `
    resultsEl.appendChild(card)
  })
}

btn.addEventListener('click', ()=>doSearch())
queryInput.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') doSearch() })

chips.addEventListener('click', (e)=>{
  if(e.target.classList.contains('chip')){
    doSearch(e.target.textContent)
  }
})
