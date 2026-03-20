import { useState } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Marquee from './components/Marquee'
import Pipeline from './components/Pipeline'
import Demo from './components/Demo'
import XaiSection from './components/XaiSection'
import Features from './components/Features'
import JobListings from './components/JobListings'
import InterviewSim from './components/InterviewSim'
import TechStack from './components/TechStack'
import CtaSection from './components/CtaSection'
import Footer from './components/Footer'
import PipelineDashboard from './components/PipelineDashboard'

function App() {
  const [resumeData, setResumeData] = useState(null)
  const [resumeId, setResumeId] = useState(null)
  const [matchResult, setMatchResult] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [showPipeline, setShowPipeline] = useState(false)

  if (showPipeline) {
    return (
      <>
        <div style={{
          position: 'fixed',
          top: '20px',
          left: '20px',
          zIndex: 1000
        }}>
          <button
            onClick={() => setShowPipeline(false)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              background: 'rgba(255,255,255,0.1)',
              backdropFilter: 'blur(10px)',
              color: '#EDF2FF',
              padding: '12px 24px',
              borderRadius: '8px',
              fontWeight: '600',
              fontSize: '14px',
              border: '1px solid rgba(255,255,255,0.2)',
              cursor: 'pointer',
              transition: 'all 0.2s',
              fontFamily: 'var(--font-display)'
            }}
            onMouseEnter={(e) => {
              e.target.style.background = 'rgba(255,255,255,0.15)'
              e.target.style.borderColor = 'rgba(0,229,180,0.4)'
              e.target.style.transform = 'translateX(-2px)'
            }}
            onMouseLeave={(e) => {
              e.target.style.background = 'rgba(255,255,255,0.1)'
              e.target.style.borderColor = 'rgba(255,255,255,0.2)'
              e.target.style.transform = 'translateX(0)'
            }}
          >
            <span style={{ fontSize: '16px' }}>←</span>
            <span>Back to Home</span>
          </button>
        </div>
        <PipelineDashboard />
      </>
    )
  }

  return (
    <>
      <Navbar onPipelineClick={() => setShowPipeline(true)} />
      <Hero onPipelineClick={() => setShowPipeline(true)} />
      <Marquee />
      <Pipeline />
      <Demo 
        resumeData={resumeData}
        setResumeData={setResumeData}
        resumeId={resumeId}
        setResumeId={setResumeId}
        matchResult={matchResult}
        setMatchResult={setMatchResult}
        jobDescription={jobDescription}
        setJobDescription={setJobDescription}
      />
      <XaiSection matchResult={matchResult} />
      <Features />
      <JobListings />
      <InterviewSim jobDescription={jobDescription} />
      <TechStack />
      <CtaSection />
      <Footer />
    </>
  )
}

export default App
