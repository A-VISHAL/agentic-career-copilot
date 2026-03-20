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
            className="text-purple-400 hover:text-purple-300 font-semibold"
          >
            🚀 Full Pipeline
          </button>
        )}
      </div>
      <a href="#demo" className="nav-cta">Try it free →</a>
    </nav>
  )
}
