import { useEffect, useRef } from 'react'

export default function Hero() {
  const statsRef = useRef(null)

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const counters = entry.target.querySelectorAll('.counter')
          counters.forEach(el => {
            const target = parseInt(el.dataset.target)
            let current = 0
            const step = target / 60
            const interval = setInterval(() => {
              current = Math.min(current + step, target)
              el.textContent = Math.round(current)
              if (current >= target) clearInterval(interval)
            }, 20)
          })
          observer.unobserve(entry.target)
        }
      })
    }, { threshold: 0.5 })

    if (statsRef.current) observer.observe(statsRef.current)
    return () => observer.disconnect()
  }, [])

  return (
    <section className="hero">
      <div className="hero-glow"></div>
      <div className="hero-glow2"></div>

      <div className="hero-badge fade-in-delay-1">
        <div className="hero-badge-dot"></div>
        HACKHAZARDS '26 · AI TRACK
      </div>

      <h1 className="hero-title fade-in-delay-2">
        Stop applying blindly.<br />
        <span className="line2">Start getting <span className="accent">hired.</span></span>
      </h1>

      <p className="hero-sub fade-in-delay-3">
        The first career copilot that doesn't just match you to jobs — it explains exactly why 
        you do or don't qualify, closes your skill gaps, and turns you into the candidate they want.
      </p>

      <div className="hero-actions fade-in-delay-4">
        <a href="#demo" className="btn-primary">
          <span>Analyze my resume</span>
          <span>→</span>
        </a>
        <a href="#how-it-works" className="btn-ghost">See how it works</a>
      </div>

      <div className="hero-stats fade-in-delay-5" ref={statsRef}>
        <div>
          <span className="hstat-num counter" data-target="94">0</span>%
          <span className="hstat-label">Match Accuracy</span>
        </div>
        <div>
          <span className="hstat-num counter" data-target="3">0</span>x
          <span className="hstat-label">More Interview Calls</span>
        </div>
        <div>
          <span className="hstat-num counter" data-target="75">0</span>%
          <span className="hstat-label">Resumes ATS-Rejected</span>
        </div>
        <div>
          <span className="hstat-num counter" data-target="6">0</span>
          <span className="hstat-label">AI Copilot Stages</span>
        </div>
      </div>
    </section>
  )
}
