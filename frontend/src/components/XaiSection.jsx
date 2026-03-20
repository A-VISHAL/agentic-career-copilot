export default function XaiSection({ matchResult }) {
  const dims = matchResult?.dimensions || [
    { name: 'Python / ML', score: 88, shap_value: 0.31 },
    { name: 'APIs / Backends', score: 72, shap_value: 0.22 },
    { name: 'Cloud (AWS)', score: 30, shap_value: 0.08 },
    { name: 'Docker / K8s', score: 15, shap_value: -0.19 },
    { name: 'System Design', score: 25, shap_value: -0.11 }
  ]

  const getBarColor = (value) => {
    if (value >= 0.15) return 'var(--c1)'
    if (value >= 0) return 'var(--c4)'
    return 'var(--c2)'
  }

  const getArrow = (value) => {
    if (value >= 0.15) return { symbol: '↑', color: 'var(--c1)' }
    if (value >= 0) return { symbol: '→', color: 'var(--c4)' }
    return { symbol: '↓', color: 'var(--c2)' }
  }

  return (
    <section className="xai-section" id="xai">
      <div className="container">
        <div className="xai-grid">
          <div>
            <div className="section-eyebrow">Explainability Engine</div>
            <h2 className="section-title">Not "74% match."<br /><em>Here's exactly why.</em></h2>
            <p style={{ color: 'var(--muted2)', fontSize: 15, lineHeight: 1.8, fontWeight: 300, marginBottom: 28 }}>
              Every match decision is broken down using SHAP feature attribution and Microsoft DiCE 
              counterfactual reasoning. You'll know exactly what's pulling your score up, what's dragging 
              it down, and the <em>single action</em> with the highest impact.
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {[
                'Compliant with EU AI Act "right to explanation" requirement',
                'Bias audit layer flags non-skill-based rejection signals',
                'Bilateral scoring — candidate fit AND role fit for candidate growth'
              ].map((item, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 12, fontSize: 14 }}>
                  <span style={{ color: 'var(--c1)', fontSize: 18 }}>✓</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="xai-visual">
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--muted)', letterSpacing: '0.1em', marginBottom: 24 }}>
              SHAP FEATURE ATTRIBUTION
            </div>

            {dims.map((dim, i) => {
              const arrow = getArrow(dim.shap_value)
              return (
                <div className="xai-score-row" key={i}>
                  <div className="xai-label">{dim.name}</div>
                  <div className="xai-bar-bg">
                    <div className="xai-bar-fill" style={{ width: `${dim.score}%`, background: getBarColor(dim.shap_value) }} />
                  </div>
                  <div className="xai-val">{dim.shap_value >= 0 ? '+' : ''}{dim.shap_value.toFixed(2)}</div>
                  <div className="xai-arrow" style={{ color: arrow.color }}>{arrow.symbol}</div>
                </div>
              )
            })}

            <div className="xai-cf-box">
              <div className="xai-cf-label">⬡ Counterfactual suggestion</div>
              <div className="xai-cf-text">
                {matchResult?.counterfactuals?.[0]?.description || 
                  <>If you add <strong>Docker to one existing project</strong> and document it on GitHub, your score increases from <strong>74% → 91%</strong>. This is the minimum-effort, maximum-impact change.</>
                }
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
