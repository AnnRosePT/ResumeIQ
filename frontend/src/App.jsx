import { useState } from 'react'
import {
  ArrowUpRight, BrainCircuit, CheckCircle2, ChevronRight, CircleHelp,
  FileText, FileUp, Gauge, Github, LoaderCircle, ShieldCheck, Sparkles,
  Target, TriangleAlert, X,
} from 'lucide-react'

const demoJob = `We are looking for a junior full-stack developer.
Required skills: Python, React, JavaScript, FastAPI, SQL, Git and REST API.
Responsibilities include building responsive user interfaces, developing backend services,
writing tests, collaborating with a team and documenting software projects.
Knowledge of Docker, AWS and Agile is preferred.`

function ScoreRing({ score }) {
  return <div className="score-ring" style={{ '--score': `${score * 3.6}deg` }}>
    <div className="score-inner"><strong>{score}</strong><span>/ 100</span></div>
  </div>
}

function TagList({ items, type = 'neutral', empty }) {
  if (!items?.length) return <p className="muted small">{empty || 'No items detected.'}</p>
  return <div className="tags">{items.map(item => <span className={`tag ${type}`} key={item}>{item}</span>)}</div>
}

export default function App() {
  const [file, setFile] = useState(null)
  const [job, setJob] = useState('')
  const [report, setReport] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [dragging, setDragging] = useState(false)

  function chooseFile(next) {
    setError('')
    if (!next) return
    if (!/\.(pdf|docx|txt)$/i.test(next.name)) {
      setError('Choose a PDF, DOCX, or TXT file.')
      return
    }
    if (next.size > 5 * 1024 * 1024) {
      setError('The file is larger than 5 MB.')
      return
    }
    setFile(next)
    setReport(null)
  }

  async function analyze() {
    setError('')
    setReport(null)
    if (!file) return setError('Upload a resume before analyzing.')
    if (job.trim().length < 40) return setError('Add a job description of at least 40 characters.')
    const body = new FormData()
    body.append('resume', file)
    body.append('job_description', job)
    setLoading(true)
    try {
      const response = await fetch('/api/analyze', { method: 'POST', body })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Analysis failed. Please try again.')
      setReport(data)
      setTimeout(() => document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' }), 80)
    } catch (err) {
      setError(err.message || 'Could not connect to the API. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const r = report?.report

  return <div className="app-shell">
    <header className="topbar">
      <a className="brand" href="#"><span className="brand-icon"><BrainCircuit size={21}/></span>Resume<span>IQ</span></a>
      <nav><a href="#how-it-works">How it works</a><a href="#about">About</a></nav>
      <a className="github-link" href="https://github.com/" target="_blank" rel="noreferrer"><Github size={16}/> GitHub <ArrowUpRight size={14}/></a>
    </header>

    <main>
      <section className="hero">
        <div className="eyebrow"><Sparkles size={14}/> SMARTER RESUME INSIGHTS</div>
        <h1>Make your next application<br/><span>count.</span></h1>
        <p>Understand how your resume aligns with a role. Get clear, practical feedback — not guesswork.</p>
        <div className="hero-points"><span><ShieldCheck size={15}/> Private demo processing</span><span><Target size={15}/> Explainable matching</span></div>
      </section>

      <section className="workspace">
        <div className="section-heading"><div><span className="step">01</span><h2>Upload your resume</h2></div><span className="hint">PDF, DOCX or TXT · Max 5 MB</span></div>
        <label className={`dropzone ${dragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
          onDragOver={e => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={e => { e.preventDefault(); setDragging(false); chooseFile(e.dataTransfer.files[0]) }}>
          <input type="file" accept=".pdf,.docx,.txt" onChange={e => chooseFile(e.target.files[0])}/>
          <div className="upload-icon">{file ? <FileText size={25}/> : <FileUp size={25}/>}</div>
          <div className="upload-copy"><strong>{file ? file.name : 'Drop your resume here'}</strong><span>{file ? `${(file.size / 1024).toFixed(0)} KB · Ready to analyze` : 'or click to browse your files'}</span></div>
          {file ? <button className="remove-file" type="button" onClick={e => { e.preventDefault(); setFile(null); setReport(null) }} aria-label="Remove file"><X size={17}/></button> : <span className="browse">Browse files</span>}
        </label>

        <div className="section-heading job-heading"><div><span className="step">02</span><h2>Add the job description</h2></div><button className="text-button" onClick={() => { setJob(demoJob); setError('') }}>Use sample role <ChevronRight size={14}/></button></div>
        <textarea value={job} onChange={e => setJob(e.target.value)} placeholder="Paste the job description here — include responsibilities, required skills and qualifications..." rows={7}/>
        <div className="textarea-footer"><span>{job.length.toLocaleString()} / 20,000 characters</span><span>At least 40 characters</span></div>

        {error && <div className="error"><TriangleAlert size={16}/>{error}</div>}
        <button className="analyze-button" onClick={analyze} disabled={loading}>
          {loading ? <><LoaderCircle className="spin" size={18}/> Analyzing resume...</> : <><Sparkles size={17}/> Analyze my resume <ArrowUpRight size={17}/></>}
        </button>
        <p className="privacy-note"><ShieldCheck size={14}/> Your file is processed in memory by this demo and is not saved to disk.</p>
      </section>

      {r && <section className="results" id="results">
        <div className="results-title"><div><div className="eyebrow"><CheckCircle2 size={14}/> ANALYSIS COMPLETE</div><h2>Your match overview</h2><p className="muted">{report.filename} · {report.characters_analyzed.toLocaleString()} characters analyzed</p></div><span className="result-pill">Resume report <FileText size={14}/></span></div>
        <div className="overview-grid">
          <div className="score-card"><ScoreRing score={r.score}/><div><span className="muted small">Overall alignment</span><h3>{r.score_label}</h3><p>{r.summary}</p></div></div>
          <div className="metric-card"><div className="metric-icon"><Target size={18}/></div><span className="muted small">Keyword coverage</span><strong>{r.keywords.coverage_percent}%</strong><span className="muted tiny">Selected job keywords found</span></div>
        </div>
        <div className="report-grid">
          <article className="report-card"><div className="card-title"><CheckCircle2 size={17}/><h3>Matched skills</h3></div><TagList items={r.skills.matched} type="good" empty="No listed skills matched yet."/></article>
          <article className="report-card"><div className="card-title warning-title"><CircleHelp size={17}/><h3>Skills to address</h3></div><TagList items={r.skills.missing} type="warning" empty="No missing skills from the detected list."/></article>
          <article className="report-card"><div className="card-title"><FileText size={17}/><h3>Resume sections</h3></div><div className="section-checks">{Object.entries(r.sections).map(([name, found]) => <div key={name}><span>{name[0].toUpperCase()+name.slice(1)}</span>{found ? <CheckCircle2 className="check" size={16}/> : <X className="missing" size={16}/>}</div>)}</div></article>
          <article className="report-card"><div className="card-title"><Target size={17}/><h3>Keyword signals</h3></div><TagList items={r.keywords.matched} type="neutral" empty="No selected keywords found."/></article>
        </div>
        <article className="suggestions-card"><div className="card-title"><Sparkles size={17}/><h3>Suggestions to strengthen your resume</h3></div><ul>{r.suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul></article>
        <p className="method-note"><ShieldCheck size={15}/>{r.methodology}</p>
      </section>}

      <section className="how" id="how-it-works"><div className="eyebrow">SIMPLE BY DESIGN</div><h2>Three steps to clearer feedback.</h2><div className="how-grid"><div><span>01</span><h3>Upload</h3><p>Add a PDF, DOCX or TXT version of your resume.</p></div><div><span>02</span><h3>Compare</h3><p>Paste a job description to identify relevant language and skills.</p></div><div><span>03</span><h3>Improve</h3><p>Use the report as a guide while keeping every claim accurate.</p></div></div></section>
      <section className="disclaimer" id="about"><ShieldCheck size={18}/><p><strong>A note on responsible use</strong><br/>ResumeIQ is an educational text-analysis tool. Its heuristic score is not an ATS score or a hiring recommendation. It does not assess candidate quality or predict job performance. Always review applications with human judgment and consistent, job-related criteria.</p></section>
    </main>
    <footer><a className="brand footer-brand" href="#"><span className="brand-icon"><BrainCircuit size={18}/></span>Resume<span>IQ</span></a><span>Built for clearer career conversations.</span><span>© 2026 ResumeIQ</span></footer>
  </div>
}
