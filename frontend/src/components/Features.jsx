const features = [
  {
    span: 'span8', accent: 'accent-c1', badge: 'badge-win', badgeText: '🏆 WINNING FEATURE',
    icon: '🧠', title: 'Counterfactual Explainability',
    desc: 'The only job platform that tells you "If you add X, your score goes from Y to Z." Powered by SHAP feature attribution and Microsoft DiCE counterfactual engine. Makes AI hiring decisions transparent, fair, and actionable — not a black box.'
  },
  {
    span: 'span4', accent: 'accent-c3', badge: 'badge-novel', badgeText: '⚡ NOVELTY POINT',
    icon: '⚖️', title: 'Bias Audit Layer',
    desc: 'Every recommendation is automatically audited for demographic bias signals using Microsoft Fairlearn. EU AI Act compliant by design.'
  },
  {
    span: 'span4', accent: 'accent-c3', badge: 'badge-novel', badgeText: '⚡ NOVELTY POINT',
    icon: '↔️', title: 'Bilateral Matching',
    desc: 'Scores both ways: how good are you for the role AND how good is the role for your career growth trajectory.'
  },
  {
    span: 'span4', accent: 'accent-c4', badge: 'badge-core', badgeText: '🔥 CORE',
    icon: '📈', title: 'Skill Velocity Tracker',
    desc: 'Live market data shows which skills are rising fastest in demand. "Docker mentions grew 34% this quarter" — prioritize what matters now.'
  },
  {
    span: 'span4', accent: 'accent-c1', badge: 'badge-win', badgeText: '🏆 WINNING FEATURE',
    icon: '🤖', title: 'Agentic Autopilot',
    desc: 'LangGraph-powered AI agent tracks deadlines, drafts applications, monitors job board changes, sends follow-up reminders autonomously.'
  },
  {
    span: 'span6', accent: 'accent-c4', badge: 'badge-core', badgeText: '🔥 CORE',
    icon: '✍️', title: 'Anti-Generic Resume Engine',
    desc: 'Specifically trained to detect and remove AI-generated, clichéd language. Rewrites using your real voice, real metrics, and real project outcomes. Solves the "generic AI resume" problem that\'s actively hurting candidates in 2026.'
  },
  {
    span: 'span6', accent: 'accent-c1', badge: 'badge-win', badgeText: '🏆 WINNING FEATURE',
    icon: '🎯', title: 'AI Mock Interview Simulator',
    desc: 'Role-specific interview simulator that generates questions directly from the job description. Gives verbal and written feedback on answer quality, confidence signals, and technical accuracy.'
  }
]

export default function Features() {
  return (
    <section className="bento-section" id="features">
      <div className="container">
        <div className="section-eyebrow">Core Features</div>
        <h2 className="section-title" style={{ marginBottom: 48 }}>
          Everything you need.<br /><em>Nothing you don't.</em>
        </h2>

        <div className="bento-grid">
          {features.map((f, i) => (
            <div className={`bento-card ${f.span}`} key={i}>
              <div className={`bento-accent-line ${f.accent}`}></div>
              <span className={`bento-badge ${f.badge}`}>{f.badgeText}</span>
              <div className="bento-icon">{f.icon}</div>
              <div className="bento-title">{f.title}</div>
              <div className="bento-desc">{f.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
