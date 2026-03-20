const items = [
  'Semantic Matching', 'Counterfactual XAI', 'Skill Gap Analysis', 'Bias Audit Layer',
  'Agentic Autopilot', 'Resume Intelligence', 'Mock Interview AI', 'Career Roadmapping',
  'ATS Optimization', 'Bilateral Scoring'
]

export default function Marquee() {
  return (
    <div className="marquee-wrap">
      <div className="marquee-track">
        {[...items, ...items].map((item, i) => (
          <div className="marquee-item" key={i}>{item}</div>
        ))}
      </div>
    </div>
  )
}
