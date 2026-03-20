import { useState } from 'react'

const steps = [
  {
    num: '01',
    title: 'Deep Profile Parsing',
    desc: 'NLP extracts skills, experience, projects, and latent competencies from your resume. Goes beyond keywords to understand what you actually know.',
    tags: ['spaCy', 'PyMuPDF', 'NER', 'Entity Extraction']
  },
  {
    num: '02',
    title: 'Semantic Job Matching',
    desc: 'Embedding-based similarity matching — not keyword matching. Understands that "built ML pipelines" and "developed machine learning systems" mean the same thing.',
    tags: ['sentence-transformers', 'Cosine Similarity', 'Bidirectional Score']
  },
  {
    num: '03',
    title: 'Explainable Match Report',
    desc: 'SHAP + counterfactual reasoning tells you exactly WHY you match or don\'t — per dimension. Not "74% match" but "add Docker → 91% match".',
    tags: ['SHAP', 'DiCE (MSFT)', 'Counterfactual XAI']
  },
  {
    num: '04',
    title: 'Skill Gap Engine',
    desc: 'Identifies exactly which skills are missing, ranks them by market demand velocity, and suggests curated learning paths to close each gap.',
    tags: ['Skill Velocity', 'Live Market Data', 'Learning Paths']
  },
  {
    num: '05',
    title: 'Intelligent Application Generator',
    desc: 'Generates tailored resumes and cover letters in your real voice — not generic AI output. ATS-optimized without losing authenticity.',
    tags: ['Claude API', 'Voice Preservation', 'ATS-Aware']
  },
  {
    num: '06',
    title: 'Agentic Career Coach',
    desc: 'An always-on AI agent that tracks applications, simulates interviews, builds 30/60/90-day career roadmaps, and autonomously follows up.',
    tags: ['LangGraph', 'Multi-step Agent', 'Interview Sim']
  }
]

export default function Pipeline() {
  const [activeStep, setActiveStep] = useState(0)

  return (
    <section className="pipeline-section" id="how-it-works">
      <div className="container">
        <div className="pipeline-header">
          <div>
            <div className="section-eyebrow">How it works</div>
            <h2 className="section-title">Six stages.<br /><em>One complete journey.</em></h2>
          </div>
          <p className="section-sub">From resume to roadmap — the first end-to-end AI career intelligence system.</p>
        </div>

        <div className="pipeline">
          {steps.map((step, i) => (
            <div 
              key={i}
              className={`pipe-step ${activeStep === i ? 'active' : ''}`}
              onClick={() => setActiveStep(i)}
            >
              <div className="pipe-num">
                <div className="pipe-num-circle">{step.num}</div>
              </div>
              <div className="pipe-content">
                <h3>{step.title}</h3>
                <p>{step.desc}</p>
                <div className="pipe-tags">
                  {step.tags.map((tag, j) => (
                    <span className="pipe-tag" key={j}>{tag}</span>
                  ))}
                </div>
              </div>
              <div className="pipe-arrow">→</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
