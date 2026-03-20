const stack = [
  { layer: 'NLP LAYER', name: 'sentence-transformers', desc: 'Semantic embeddings for deep resume ↔ JD matching' },
  { layer: 'NLP LAYER', name: 'spaCy + PyMuPDF', desc: 'Resume parsing, NER, skill extraction from PDF/DOCX' },
  { layer: 'EXPLAINABILITY', name: 'SHAP Library', desc: 'Feature attribution for every match score decision' },
  { layer: 'EXPLAINABILITY', name: 'DiCE (MSFT)', desc: 'Diverse counterfactual explanations engine' },
  { layer: 'FAIRNESS', name: 'Fairlearn (MSFT)', desc: 'Bias auditing across all recommendations' },
  { layer: 'LLM', name: 'OpenAI GPT-4o', desc: 'Resume rewriting, cover letters, career coaching' },
  { layer: 'AGENTIC', name: 'LangGraph', desc: 'Multi-step autonomous agent workflows' },
  { layer: 'BACKEND', name: 'FastAPI', desc: 'Async REST API, job queue for processing' },
  { layer: 'FRONTEND', name: 'React + Vite', desc: 'Fast, responsive, demo-ready UI' },
  { layer: 'DATA', name: 'Adzuna API', desc: 'Live job listings + skill trend data' },
  { layer: 'DATABASE', name: 'Supabase', desc: 'User profiles, history, roadmap tracking' },
  { layer: 'DEPLOY', name: 'Railway', desc: 'Fast free-tier deployment for live demo' },
]

export default function TechStack() {
  return (
    <section className="tech-section">
      <div className="container">
        <div className="section-eyebrow">Technical Architecture</div>
        <h2 className="section-title">Built on <em>serious infrastructure.</em></h2>
        <div className="tech-cols">
          {stack.map((item, i) => (
            <div className="tech-card" key={i}>
              <div className="tech-layer">{item.layer}</div>
              <div className="tech-name">{item.name}</div>
              <div className="tech-desc">{item.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
