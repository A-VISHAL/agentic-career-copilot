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
    return <PipelineDashboard onNavigateHome={() => setShowPipeline(false)} />
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
