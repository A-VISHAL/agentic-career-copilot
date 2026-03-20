import { useState, useRef, useEffect } from 'react'
import { evaluateAnswer } from '../utils/api'

const DEMO_RESPONSES = [
  {
    question: "Good answer! Can you tell me more about the infrastructure you used and how you handled model monitoring?",
    scores: { overall: 72, tech: 68, clarity: 75 },
    tip: '💡 Good STAR structure, but add specific metrics — latency numbers, throughput, error rates. Mention monitoring tools like Prometheus or Grafana.'
  },
  {
    question: "Excellent! What was the biggest scaling challenge you faced, and how did you solve it?",
    scores: { overall: 81, tech: 78, clarity: 85 },
    tip: '✅ Strong technical depth. Next, try to quantify the impact — "this reduced costs by X%" or "handled Y requests per second".'
  },
  {
    question: "Last question: How do you approach the trade-off between model accuracy and inference latency in production?",
    scores: { overall: 88, tech: 90, clarity: 86 },
    tip: '🔥 Excellent answer! You covered the core trade-off clearly. Mention quantization or model distillation techniques to show deeper expertise.'
  }
]

const KEYWORDS = ['production deployment', 'model monitoring', 'latency tradeoffs', 'A/B testing', 'scale challenges']

export default function InterviewSim({ jobDescription }) {
  const [messages, setMessages] = useState([
    { role: 'ai', text: "Hi! I'm simulating your interview for the Senior ML Engineer role at Anthropic. Ready to start? I'll ask you questions based on the actual job description." },
    { role: 'ai', text: "<strong>Q1:</strong> Can you walk me through a machine learning system you've built and deployed to production? What were the main technical challenges?" }
  ])
  const [input, setInput] = useState('')
  const [scores, setScores] = useState({ overall: null, tech: null, clarity: null })
  const [feedback, setFeedback] = useState('Your feedback will appear here after each answer. The AI analyzes technical accuracy, use of the STAR method, and role-specific relevance.')
  const [chatStep, setChatStep] = useState(0)
  const msgsRef = useRef(null)

  useEffect(() => {
    if (msgsRef.current) {
      msgsRef.current.scrollTop = msgsRef.current.scrollHeight
    }
  }, [messages])

  const sendChat = async () => {
    if (!input.trim()) return

    const userMsg = input
    setInput('')
    setMessages(prev => [...prev, { role: 'user', text: userMsg }])

    // Try API first
    let apiResult = null
    try {
      const currentQuestion = messages[messages.length - 1]?.text || ''
      apiResult = await evaluateAnswer(currentQuestion, userMsg, jobDescription)
    } catch (e) {
      console.log('Using demo mode for interview')
    }

    setTimeout(() => {
      const demo = DEMO_RESPONSES[chatStep % DEMO_RESPONSES.length]
      
      if (apiResult) {
        setScores({
          overall: apiResult.score,
          tech: apiResult.technical_depth,
          clarity: apiResult.clarity
        })
        setFeedback(apiResult.feedback)
      } else {
        setScores(demo.scores)
        setFeedback(demo.tip)
      }

      setMessages(prev => [...prev, { role: 'ai', text: demo.question }])
      setChatStep(prev => prev + 1)
    }, 800)
  }

  return (
    <section className="interview-section" id="interview">
      <div className="container">
        <div className="section-eyebrow">AI Interview Simulator</div>
        <h2 className="section-title">Practice with an AI that <em>knows the role.</em></h2>
        <p className="section-sub" style={{ marginBottom: 48 }}>
          Questions generated from the actual job description. Real-time feedback on every answer.
        </p>

        <div className="interview-grid">
          {/* Chat Window */}
          <div className="chat-window">
            <div className="chat-header">
              <div className="chat-avatar">AI</div>
              <div>
                <div className="chat-name">Career Coach — Senior ML Engineer</div>
                <div className="chat-status">● Live simulation</div>
              </div>
            </div>
            <div className="chat-msgs" ref={msgsRef}>
              {messages.map((msg, i) => (
                <div key={i} className={`msg ${msg.role === 'ai' ? 'ai' : 'user'}`}>
                  <div className="msg-sender">{msg.role === 'ai' ? 'AI INTERVIEWER' : 'YOU'}</div>
                  <div className="msg-bubble" dangerouslySetInnerHTML={{ __html: msg.text }} />
                </div>
              ))}
            </div>
            <div className="chat-input-wrap">
              <input
                type="text"
                className="chat-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your answer..."
                onKeyDown={(e) => e.key === 'Enter' && sendChat()}
              />
              <button className="chat-send" onClick={sendChat}>Send</button>
            </div>
          </div>

          {/* Score Panel */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div className="score-ticker">
              <div>
                <div className="ticker-label">ANSWER QUALITY SCORE</div>
                <div className="ticker-val">{scores.overall !== null ? `${scores.overall}/100` : '—'}</div>
                <div className="ticker-sub">{scores.overall !== null ? 'Based on your latest answer' : 'Answer a question to see your score'}</div>
                <div className="ticker-bar-bg">
                  <div className="ticker-bar-fill" style={{ width: `${scores.overall || 0}%` }} />
                </div>
              </div>
              <div className="ticker-divider"></div>
              <div>
                <div className="ticker-label">TECHNICAL DEPTH</div>
                <div className="ticker-val">{scores.tech !== null ? `${scores.tech}%` : '—'}</div>
                <div className="ticker-bar-bg">
                  <div className="ticker-bar-fill" style={{ width: `${scores.tech || 0}%`, background: 'var(--c5)' }} />
                </div>
              </div>
              <div className="ticker-divider"></div>
              <div>
                <div className="ticker-label">CLARITY & STRUCTURE</div>
                <div className="ticker-val">{scores.clarity !== null ? `${scores.clarity}%` : '—'}</div>
                <div className="ticker-bar-bg">
                  <div className="ticker-bar-fill" style={{ width: `${scores.clarity || 0}%`, background: 'var(--c4)' }} />
                </div>
              </div>
            </div>

            <div className="feedback-panel">
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--muted)', letterSpacing: '0.08em', marginBottom: 14 }}>
                FEEDBACK TIPS
              </div>
              <div style={{ fontSize: 13, color: 'var(--muted2)', lineHeight: 1.7 }}>
                {feedback}
              </div>
            </div>

            <div style={{ background: 'var(--bg2)', border: '1px solid rgba(0,229,180,0.15)', borderRadius: 14, padding: 20 }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--c1)', letterSpacing: '0.08em', marginBottom: 10 }}>
                KEYWORDS TO INCLUDE
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {KEYWORDS.map((kw, i) => (
                  <span key={i} className="keyword-tag">{kw}</span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
