import { useState } from 'react'

const jobs = [
  {
    emoji: '🏢', title: 'Senior ML Engineer', company: 'Anthropic · San Francisco',
    salary: '💰 $180K–$240K', remote: '🌐 Remote OK', type: '⏰ Full-time',
    matchScore: 91, matchClass: 'match-high',
    skills: [
      { name: 'Python', match: true }, { name: 'PyTorch', match: true },
      { name: 'FastAPI', match: true }, { name: 'Docker', match: false },
      { name: 'RLHF', match: true }
    ],
    categories: ['ml', 'remote']
  },
  {
    emoji: '🔵', title: 'AI Research Engineer', company: 'DeepMind · London, UK',
    salary: '💰 £120K–£160K', remote: '🏢 Hybrid', type: '⏰ Full-time',
    matchScore: 87, matchClass: 'match-high',
    skills: [
      { name: 'Python', match: true }, { name: 'JAX', match: true },
      { name: 'TPU/XLA', match: false }, { name: 'NLP', match: true },
      { name: 'Research', match: true }
    ],
    categories: ['ml']
  },
  {
    emoji: '🟠', title: 'ML Platform Engineer', company: 'Stripe · Remote',
    salary: '💰 $150K–$200K', remote: '🌐 Remote', type: '⏰ Full-time',
    matchScore: 74, matchClass: 'match-med',
    skills: [
      { name: 'Python', match: true }, { name: 'Kubernetes', match: false },
      { name: 'Airflow', match: false }, { name: 'SQL', match: true },
      { name: 'MLflow', match: true }
    ],
    categories: ['backend', 'remote']
  },
  {
    emoji: '🟣', title: 'NLP Engineer', company: 'Cohere · Toronto',
    salary: '💰 $140K–$190K', remote: '🌐 Remote OK', type: '⏰ Full-time',
    matchScore: 94, matchClass: 'match-high',
    skills: [
      { name: 'Python', match: true }, { name: 'NLP', match: true },
      { name: 'Transformers', match: true }, { name: 'spaCy', match: true },
      { name: 'FastAPI', match: true }
    ],
    categories: ['ml', 'remote']
  },
  {
    emoji: '▲', title: 'Full Stack AI Developer', company: 'Vercel · Remote',
    salary: '💰 $130K–$180K', remote: '🌐 Remote', type: '⏰ Full-time',
    matchScore: 62, matchClass: 'match-low',
    skills: [
      { name: 'React', match: true }, { name: 'TypeScript', match: false },
      { name: 'Next.js', match: false }, { name: 'Python', match: true },
      { name: 'LLM', match: false }
    ],
    categories: ['fullstack', 'remote']
  },
  {
    emoji: '💳', title: 'Data Scientist — Fraud Detection', company: 'Revolut · London',
    salary: '💰 £90K–£130K', remote: '🌐 Remote OK', type: '⏰ Full-time',
    matchScore: 85, matchClass: 'match-high',
    skills: [
      { name: 'Python', match: true }, { name: 'scikit-learn', match: true },
      { name: 'SQL', match: true }, { name: 'ML', match: true },
      { name: 'Data Eng', match: false }
    ],
    categories: ['ml', 'remote']
  }
]

const filters = [
  { label: 'All Roles', value: 'all' },
  { label: 'ML / AI', value: 'ml' },
  { label: 'Backend', value: 'backend' },
  { label: 'Full Stack', value: 'fullstack' },
  { label: 'Remote', value: 'remote' }
]

export default function JobListings() {
  const [activeFilter, setActiveFilter] = useState('all')

  const filtered = activeFilter === 'all'
    ? jobs
    : jobs.filter(j => j.categories.includes(activeFilter))

  return (
    <section style={{ background: 'var(--bg0)', padding: '100px 0' }} id="jobs">
      <div className="container">
        <div className="section-eyebrow">Matched Opportunities</div>
        <h2 className="section-title">Your top matches, <em>explained.</em></h2>
        <p className="section-sub" style={{ marginBottom: 40 }}>
          Every listing shows your match percentage, which skills you have, and exactly what's missing.
        </p>

        <div className="jobs-filter">
          {filters.map(f => (
            <button
              key={f.value}
              className={`filter-btn ${activeFilter === f.value ? 'active' : ''}`}
              onClick={() => setActiveFilter(f.value)}
            >
              {f.label}
            </button>
          ))}
        </div>

        <div className="jobs-grid">
          {filtered.map((job, i) => (
            <div className="job-card" key={i}>
              <div className="job-card-top">
                <div className="job-company-logo">{job.emoji}</div>
                <div className={`job-match-badge ${job.matchClass}`}>{job.matchScore}% match</div>
              </div>
              <div className="job-title">{job.title}</div>
              <div className="job-company">{job.company}</div>
              <div className="job-meta">
                <span className="job-meta-item">{job.salary}</span>
                <span className="job-meta-item">{job.remote}</span>
                <span className="job-meta-item">{job.type}</span>
              </div>
              <div className="job-skill-tags">
                {job.skills.map((s, j) => (
                  <span key={j} className={`job-skill ${s.match ? 'match' : 'miss'}`}>{s.name}</span>
                ))}
              </div>
              <div className="job-card-actions">
                <button className="job-btn-primary">
                  {job.matchScore >= 80 ? 'Apply with AI →' : 'Improve & Apply →'}
                </button>
                <button className="job-btn-ghost">Save</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
