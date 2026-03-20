export default function Navbar({ onPipelineClick }) {
  return (
    <nav>
      <div className="nav-logo">
        <div className="logo-dot"></div>
        NexusCareer
      </div>
      <div className="nav-links">
        <a href="#how-it-works">How it works</a>
        <a href="#demo">Live demo</a>
        <a href="#features">Features</a>
        <a href="#interview">Interview AI</a>
        {onPipelineClick && (
          <button 
            onClick={onPipelineClick}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--c1)',
              fontSize: '13px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'color 0.2s',
              fontFamily: 'inherit',
              padding: '0'
            }}
            onMouseEnter={(e) => e.target.style.color = 'var(--text)'}
            onMouseLeave={(e) => e.target.style.color = 'var(--c1)'}
          >
            🚀 Full Pipeline
          </button>
        )}
      </div>
      <a href="#demo" className="nav-cta">Try it free →</a>
    </nav>
  )
}
