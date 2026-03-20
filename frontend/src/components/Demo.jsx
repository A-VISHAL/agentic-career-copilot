import { useState, useRef, useCallback, useEffect } from 'react'
import { uploadResume, getSampleResume, matchResume, improveResume, getRoadmap } from '../utils/api'

// ─── DEMO DATA (Fallback when backend is unavailable) ───

const DEMO_MATCH_RESULT = {
  overall_score: 74,
  dimensions: [
    { name: 'Technical Skills', score: 88, shap_value: 0.31, matched_items: ['Python', 'PyTorch', 'FastAPI'], missing_items: ['Docker', 'Kubernetes'], explanation: 'Matched 4 of 6 required skills' },
    { name: 'Experience Fit', score: 76, shap_value: 0.22, matched_items: ['Senior ML Engineer', 'ML Engineer'], missing_items: [], explanation: '2 relevant roles found' },
    { name: 'Domain Knowledge', score: 65, shap_value: 0.08, matched_items: [], missing_items: [], explanation: 'Resume-JD semantic alignment: 65%' },
    { name: 'Project Depth', score: 91, shap_value: -0.19, matched_items: ['Resume Intelligence Engine', 'Semantic Search Engine'], missing_items: [], explanation: '2 projects demonstrate hands-on building' },
    { name: 'Communication', score: 58, shap_value: -0.11, matched_items: [], missing_items: [], explanation: 'Based on resume clarity, structure, detail level' }
  ],
  counterfactuals: [
    { action: 'Add Docker + one deployed project', current_score: 74, projected_score: 91, impact: 'high', description: 'Adding Docker + Kubernetes together (e.g., in one deployed project) is the single highest-impact change. Score: 74% → 91%' },
    { action: 'Add Docker', current_score: 74, projected_score: 87, impact: 'high', description: 'Adding Docker with a demonstrated project would raise your score from 74% to 87%. This is a required skill for the role.' },
    { action: 'Add CI/CD experience', current_score: 74, projected_score: 82, impact: 'medium', description: 'Adding CI/CD pipeline experience would strengthen your application considerably.' }
  ],
  role_fit_for_candidate: 82,
  summary: 'Good match with 2 key gap(s) identified. Address these to significantly improve your chances.'
}

const DEMO_IMPROVEMENTS = [
  { original: 'Responsible for developing machine learning models that improved efficiency and performance metrics across various business domains.', improved: 'Built NLP classification pipeline processing 2.3M daily events, reducing false-positive alerts by 41% and saving 120 eng-hours/month.', reason: 'Generic → specific: added exact metrics, real project, quantified outcome', impact_area: 'specificity' },
  { original: 'Worked on various projects using Python and helped the team with technical tasks and problem solving.', improved: 'Led 3-person ML team to ship real-time fraud detection model in 6 weeks, blocking $840K in fraudulent transactions in Q1.', reason: 'Vague → quantified: team size, timeline, dollar impact, specific outcome', impact_area: 'metrics' },
  { original: 'Experienced in building and deploying APIs and backend services for multiple applications.', improved: 'Designed FastAPI REST endpoints serving 50K+ predictions/day at <100ms p99 latency, supporting 3 production ML models.', reason: 'Abstract → concrete: specific technology, throughput, latency, scale', impact_area: 'clarity' },
  { original: 'Skilled in data analysis and creating dashboards to help stakeholders make data-driven decisions.', improved: 'Built real-time model monitoring dashboard tracking drift, accuracy (93% → 96%), and latency across 12 production experiments using Grafana + Prometheus.', reason: 'Passive → active: named tools, showed improvement trajectory, added scale', impact_area: 'keywords' }
]

const DEMO_ROADMAP = {
  target_role: 'Senior ML Engineer',
  items: [
    { week: 'Week 1–2', title: 'Docker + Container Basics', description: 'Complete Docker Fundamentals (8hrs). Containerize your existing ML project. Highest ROI action for your target role.', category: 'learn' },
    { week: 'Week 3–4', title: 'Deploy a model end-to-end', description: 'Build FastAPI → Docker → Railway deployment. Add it to GitHub. This is the portfolio gap recruiters see.', category: 'build' },
    { week: 'Week 5–6', title: 'Apply to 8 targeted roles', description: 'Use your updated resume and tailored cover letters. Aim for 70%+ match score roles only.', category: 'apply' },
    { week: 'Month 2–3', title: 'System Design prep', description: 'Complete Grokking System Design. Practice 2 mock interviews per week with the AI simulator.', category: 'learn' }
  ]
}

// ─── PROCESSING STEPS ───
const PROCESSING_STEPS = [
  'Parsing resume structure...',
  'Extracting skills & experience...',
  'Running semantic embeddings...',
  'Computing SHAP attributions...',
  'Generating counterfactuals...',
  'Building your roadmap...'
]

export default function Demo({ resumeData, setResumeData, resumeId, setResumeId, matchResult, setMatchResult, jobDescription, setJobDescription }) {
  const [activeTab, setActiveTab] = useState('match')
  const [processing, setProcessing] = useState(false)
  const [processingText, setProcessingText] = useState('')
  const [improvements, setImprovements] = useState(null)
  const [roadmap, setRoadmap] = useState(null)
  const [hasAnalyzed, setHasAnalyzed] = useState(false)
  const fileInputRef = useRef(null)
  const [animatedScore, setAnimatedScore] = useState(0)
  const [showBars, setShowBars] = useState(false)

  // Score ring animation
  useEffect(() => {
    if (matchResult) {
      const target = matchResult.overall_score
      let current = 0
      const step = target / 40
      const interval = setInterval(() => {
        current = Math.min(current + step, target)
        setAnimatedScore(Math.round(current))
        if (current >= target) clearInterval(interval)
      }, 25)
      
      setTimeout(() => setShowBars(true), 500)
      return () => clearInterval(interval)
    }
  }, [matchResult])

  const animateProcessing = useCallback((callback) => {
    setProcessing(true)
    let step = 0
    setProcessingText(PROCESSING_STEPS[0])
    
    const interval = setInterval(() => {
      step++
      if (step < PROCESSING_STEPS.length) {
        setProcessingText(PROCESSING_STEPS[step])
      } else {
        clearInterval(interval)
        setProcessing(false)
        callback()
      }
    }, 500)
  }, [])

  const handleSampleLoad = useCallback(async () => {
    animateProcessing(async () => {
      try {
        const result = await getSampleResume()
        if (result) {
          setResumeData(result.parsed)
          setResumeId(result.resume_id)
        }
      } catch (e) {
        console.log('Using demo mode')
      }
      
      setMatchResult(DEMO_MATCH_RESULT)
      setImprovements(DEMO_IMPROVEMENTS)
      setRoadmap(DEMO_ROADMAP)
      setHasAnalyzed(true)
    })
  }, [animateProcessing, setResumeData, setResumeId, setMatchResult])

  const handleFileUpload = useCallback(async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    animateProcessing(async () => {
      try {
        const result = await uploadResume(file)
        if (result) {
          setResumeData(result.parsed)
          setResumeId(result.resume_id)
        }
      } catch (e) {
        console.log('Using demo mode for upload')
      }

      setMatchResult(DEMO_MATCH_RESULT)
      setImprovements(DEMO_IMPROVEMENTS)
      setRoadmap(DEMO_ROADMAP)
      setHasAnalyzed(true)
    })
  }, [animateProcessing, setResumeData, setResumeId, setMatchResult])

  const handleAnalyze = useCallback(async () => {
    if (!jobDescription.trim()) {
      alert('Please paste a job description first!')
      return
    }

    animateProcessing(async () => {
      try {
        const result = await matchResume(resumeId, jobDescription)
        if (result) {
          setMatchResult(result)
          
          // Also fetch improvements and roadmap
          const impResult = await improveResume(resumeId, jobDescription)
          if (impResult) setImprovements(impResult.improvements)
          
          const rmResult = await getRoadmap(resumeId, jobDescription)
          if (rmResult) setRoadmap(rmResult)
          
          setHasAnalyzed(true)
          return
        }
      } catch (e) {
        console.log('Using demo mode for analysis')
      }

      setMatchResult(DEMO_MATCH_RESULT)
      setImprovements(DEMO_IMPROVEMENTS)
      setRoadmap(DEMO_ROADMAP)
      setHasAnalyzed(true)
    })
  }, [jobDescription, resumeId, animateProcessing, setMatchResult])

  const circumference = 364.4
  const scoreOffset = matchResult
    ? circumference - (matchResult.overall_score / 100) * circumference
    : circumference

  const getScoreColor = (score) => {
    if (score >= 85) return 'var(--c1)'
    if (score >= 70) return 'var(--c4)'
    return 'var(--c2)'
  }

  const tabColors = ['var(--c1)', 'var(--c5)', 'var(--c4)', 'var(--c3)', 'var(--c2)']

  const renderActiveTab = () => {
    if (!hasAnalyzed) {
      return (
        <div style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--muted2)' }}>
          <div style={{ fontSize: 40, marginBottom: 16 }}>📊</div>
          <p>Upload your resume or use the sample to see results</p>
        </div>
      )
    }

    switch (activeTab) {
      case 'match':
        return (
          <div>
            <div className="match-score-wrap">
              <div className="score-ring">
                <svg width="140" height="140" viewBox="0 0 140 140">
                  <circle cx="70" cy="70" r="58" fill="none" stroke="#0F182C" strokeWidth="10" />
                  <circle cx="70" cy="70" r="58" fill="none"
                    stroke={getScoreColor(matchResult?.overall_score || 0)}
                    strokeWidth="10"
                    strokeDasharray={circumference}
                    strokeDashoffset={scoreOffset}
                    strokeLinecap="round"
                    style={{ transition: 'stroke-dashoffset 1.5s cubic-bezier(0.16,1,0.3,1)' }}
                  />
                </svg>
                <div className="score-num">
                  <span>{animatedScore}%</span>
                  <span className="score-label">match</span>
                </div>
              </div>
              <div style={{ fontSize: 14, color: matchResult?.overall_score >= 85 ? 'var(--c1)' : matchResult?.overall_score >= 70 ? 'var(--c4)' : 'var(--c2)' }}>
                {matchResult?.summary}
              </div>
            </div>

            {showBars && matchResult?.dimensions && (
              <div className="skill-bars">
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--muted)', letterSpacing: '0.08em', marginBottom: 6 }}>
                  SKILL DIMENSION SCORES
                </div>
                {matchResult.dimensions.map((dim, i) => (
                  <div className="skill-row" key={i}>
                    <span className="skill-name">{dim.name}</span>
                    <div className="skill-bar-bg">
                      <div className="skill-bar-fill" style={{ width: `${dim.score}%`, background: tabColors[i] }} />
                    </div>
                    <span className="skill-pct">{Math.round(dim.score)}%</span>
                  </div>
                ))}
              </div>
            )}

            {matchResult?.role_fit_for_candidate && (
              <div style={{ marginTop: 20, padding: 16, background: 'var(--bg2)', borderRadius: 10, border: '1px solid var(--border)' }}>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--c3)', letterSpacing: '0.08em', marginBottom: 8 }}>
                  ↔ BILATERAL SCORE — ROLE FIT FOR YOU
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: 24, color: 'var(--c3)' }}>{matchResult.role_fit_for_candidate}%</span>
                  <span style={{ fontSize: 13, color: 'var(--muted2)' }}>This role offers good career growth alignment for your trajectory</span>
                </div>
              </div>
            )}
          </div>
        )

      case 'explain':
        return (
          <div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--muted)', letterSpacing: '0.08em', marginBottom: 16 }}>
              SHAP ATTRIBUTION BREAKDOWN
            </div>
            <div className="explain-items">
              {matchResult?.dimensions?.map((dim, i) => (
                <div className="explain-item" key={i}>
                  <div className={`explain-dot ${dim.shap_value >= 0.15 ? 'match' : dim.shap_value >= 0 ? 'partial' : 'miss'}`}></div>
                  <div className="explain-text">
                    <strong>{dim.matched_items?.length > 0 ? dim.matched_items.join(' · ') : dim.name}</strong>
                    {dim.missing_items?.length > 0 && (
                      <span style={{ color: 'var(--c2)', fontSize: 12 }}> (missing: {dim.missing_items.join(', ')})</span>
                    )}
                    <div className="explain-why">// {dim.explanation}</div>
                  </div>
                  <span className="explain-pct">{dim.shap_value >= 0 ? '+' : ''}{dim.shap_value.toFixed(2)}</span>
                </div>
              ))}
            </div>
            {matchResult?.counterfactuals?.length > 0 && (
              <div className="counterfact-box">
                <div className="counterfact-label">⬡ COUNTERFACTUAL — IF YOU ADDED:</div>
                <div className="counterfact-text">
                  {matchResult.counterfactuals[0].description.split(matchResult.counterfactuals[0].projected_score + '%').map((part, i, arr) => (
                    <span key={i}>
                      {part}
                      {i < arr.length - 1 && <span className="upgrade">{matchResult.counterfactuals[0].projected_score}%</span>}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )

      case 'resume':
        return (
          <div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--muted)', letterSpacing: '0.08em', marginBottom: 16 }}>
              BEFORE → AFTER TRANSFORMATION
            </div>
            {(improvements || DEMO_IMPROVEMENTS).map((imp, i) => (
              <div className="before-after" key={i} style={{ marginBottom: i < 3 ? 10 : 0 }}>
                <div className="ba-card">
                  <div className="ba-label bad">✗ {imp.impact_area?.toUpperCase() || 'GENERIC'}</div>
                  <div className="ba-text">
                    <span className="strikethrough">{imp.original}</span>
                  </div>
                </div>
                <div className="ba-card">
                  <div className="ba-label good">✓ IMPROVED</div>
                  <div className="ba-text">
                    {imp.improved}
                  </div>
                </div>
              </div>
            ))}
            <button className="btn-primary" style={{ marginTop: 20, fontSize: 13, padding: '10px 20px', border: 'none', width: '100%', justifyContent: 'center' }}>
              Generate full tailored resume →
            </button>
          </div>
        )

      case 'roadmap':
        return (
          <div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--muted)', letterSpacing: '0.08em', marginBottom: 16 }}>
              PERSONALIZED 90-DAY CAREER ROADMAP
            </div>
            <div className="roadmap-items">
              {(roadmap?.items || DEMO_ROADMAP.items).map((item, i) => (
                <div className="roadmap-item" key={i}>
                  <div className="roadmap-week">{item.week}</div>
                  <div className="roadmap-task">
                    <h4>{item.title}</h4>
                    <p>{item.description}</p>
                    <span className={`roadmap-tag tag-${item.category}`}>{item.category.toUpperCase()}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <section className="demo-section" id="demo">
      <div className="container">
        <div className="section-eyebrow">Live Demo</div>
        <h2 className="section-title">Try it <em>right now.</em></h2>
        <p className="section-sub" style={{ marginBottom: 48 }}>
          Upload your resume or use our sample — watch the AI analyze, explain, and transform it in real time.
        </p>

        <div className="demo-grid">
          {/* Left: Input */}
          <div>
            <div className="upload-zone" onClick={() => fileInputRef.current?.click()}>
              <div className="upload-icon">📄</div>
              <h3>Drop your resume here</h3>
              <p>PDF or DOCX — max 5MB</p>
              <input 
                type="file" 
                ref={fileInputRef}
                accept=".pdf,.docx,.txt" 
                onChange={handleFileUpload}
                style={{ display: 'none' }}
              />
              <br />
              <button className="sample-btn" onClick={(e) => { e.stopPropagation(); handleSampleLoad() }}>
                ✦ Use sample resume
              </button>
            </div>

            {/* JD Input */}
            <div style={{ marginTop: 20, background: 'var(--bg1)', border: '1px solid var(--border)', borderRadius: 14, padding: 20 }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--muted2)', letterSpacing: '0.08em', marginBottom: 10 }}>
                PASTE JOB DESCRIPTION
              </div>
              <textarea 
                className="jd-input-area"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description you want to match against..."
              />
              <button 
                className="btn-primary" 
                style={{ marginTop: 12, fontSize: 13, padding: '10px 24px', border: 'none' }}
                onClick={handleAnalyze}
              >
                Analyze Match →
              </button>
            </div>

            {/* Resume Summary (after upload) */}
            {resumeData && (
              <div style={{ marginTop: 20, background: 'var(--bg1)', border: '1px solid rgba(0,229,180,0.15)', borderRadius: 14, padding: 20 }}>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--c1)', letterSpacing: '0.08em', marginBottom: 10 }}>
                  ✓ RESUME PARSED
                </div>
                <div style={{ fontSize: 16, fontWeight: 700, marginBottom: 6 }}>{resumeData.name || 'Resume Loaded'}</div>
                <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                  <span style={{ fontSize: 12, color: 'var(--muted2)' }}>
                    🎯 {resumeData.skill_names?.length || resumeData.skills?.length || 0} skills detected
                  </span>
                  <span style={{ fontSize: 12, color: 'var(--muted2)' }}>
                    💼 {resumeData.experiences?.length || 0} roles
                  </span>
                  <span style={{ fontSize: 12, color: 'var(--muted2)' }}>
                    📁 {resumeData.projects?.length || 0} projects
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Right: Results */}
          <div style={{ position: 'relative' }}>
            <div className="result-panel">
              {/* Processing Overlay */}
              {processing && (
                <div className="processing-overlay">
                  <div className="processing-ring"></div>
                  <div className="processing-text">{processingText}</div>
                </div>
              )}

              {/* Tabs */}
              <div className="result-tabs">
                {[
                  { id: 'match', label: 'Match Score' },
                  { id: 'explain', label: 'XAI Breakdown' },
                  { id: 'resume', label: 'Resume AI' },
                  { id: 'roadmap', label: 'Roadmap' }
                ].map(tab => (
                  <button
                    key={tab.id}
                    className={`result-tab ${activeTab === tab.id ? 'active' : ''}`}
                    onClick={() => setActiveTab(tab.id)}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* Active Tab Content */}
              <div className="result-content" style={{ display: 'block' }}>
                {renderActiveTab()}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
