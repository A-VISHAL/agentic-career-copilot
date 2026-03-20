export default function CtaSection() {
  return (
    <section className="cta-section">
      <div className="container">
        <h2>Stop sending into<br />the void.</h2>
        <p>Join thousands of builders getting hired smarter, faster, and with full transparency into every decision.</p>
        <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
          <a href="#demo" className="btn-primary" style={{ fontSize: 16, padding: '16px 36px' }}>
            Analyze my resume — it's free →
          </a>
          <a href="#how-it-works" className="btn-ghost" style={{ fontSize: 16, padding: '16px 32px' }}>
            See full demo
          </a>
        </div>
      </div>
    </section>
  )
}
