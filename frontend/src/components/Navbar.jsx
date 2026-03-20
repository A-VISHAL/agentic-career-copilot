export default function Navbar() {
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
      </div>
      <a href="#demo" className="nav-cta">Try it free →</a>
    </nav>
  )
}
