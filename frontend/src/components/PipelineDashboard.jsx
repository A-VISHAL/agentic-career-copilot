import { useState, useEffect } from 'react'
import { uploadResume, getSampleResume } from '../utils/api'
import NavigationButton from './NavigationButton'
import Breadcrumb from './Breadcrumb'
import ProgressBar from './ProgressBar'
import StepCard from './StepCard'

const API_BASE = 'http://localhost:8000'

const PipelineDashboard = ({ onNavigateHome }) => {
  const [loading, setLoading] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [pipelineData, setPipelineData] = useState(null)
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [resumeId, setResumeId] = useState(null)
  const [error, setError] = useState(null)
  const [errorStep, setErrorStep] = useState(null)

  // Keyboard navigation - Escape key focuses navigation button
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        document.querySelector('[aria-label="Navigate back to home page"]')?.focus()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  const steps = [
    { id: 1, name: 'Upload', icon: '📄' },
    { id: 2, name: 'Parse Resume', icon: '🔍' },
    { id: 3, name: 'Parse JD', icon: '📋' },
    { id: 4, name: 'Match', icon: '🎯' },
    { id: 5, name: 'Explain', icon: '💡' },
    { id: 6, name: 'Skill Gap', icon: '📊' },
    { id: 7, name: 'Optimize', icon: '✨' },
    { id: 8, name: 'Recruiter', icon: '👔' },
    { id: 9, name: 'Generate', icon: '📝' },
    { id: 10, name: 'Agentic', icon: '🤖' },
    { id: 11, name: 'Store', icon: '💾' },
    { id: 12, name: 'Visualize', icon: '📈' }
  ]

  const breadcrumbItems = [
    { label: 'Pipeline Dashboard' }
  ]

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setResumeFile(file)
    setLoading(true)
    setCurrentStep(1)
    setError(null)
    setErrorStep(null)

    try {
      const response = await uploadResume(file)
      setResumeId(response.resume_id)
      setCurrentStep(2)
    } catch (error) {
      console.error('Upload error:', error)
      setError('Failed to upload resume')
      setErrorStep(1)
      alert('Failed to upload resume')
    } finally {
      setLoading(false)
    }
  }

  const runFullPipeline = async () => {
    if (!resumeId && !jobDescription) {
      alert('Please upload a resume and enter a job description')
      return
    }

    setLoading(true)
    setCurrentStep(3)
    setError(null)
    setErrorStep(null)

    try {
      let currentResumeId = resumeId
      if (!currentResumeId) {
        const sampleResponse = await getSampleResume()
        currentResumeId = sampleResponse.resume_id
        setResumeId(currentResumeId)
      }

      const formData = new FormData()
      formData.append('resume_id', currentResumeId)
      formData.append('job_description', jobDescription || 'Senior ML Engineer with Python, PyTorch, and FastAPI experience. 3+ years required.')

      for (let i = 3; i <= 12; i++) {
        setCurrentStep(i)
        await new Promise(resolve => setTimeout(resolve, 500))
      }

      const response = await fetch(`${API_BASE}/api/pipeline/full`, {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      setPipelineData(data)
      setCurrentStep(12)
    } catch (error) {
      console.error('Pipeline error:', error)
      setError(error.message || 'Pipeline execution failed')
      setErrorStep(currentStep)
      alert('Pipeline execution failed')
    } finally {
      setLoading(false)
    }
  }

  const handleRetry = () => {
    setError(null)
    setErrorStep(null)
    runFullPipeline()
  }

  const useSampleData = async () => {
    setLoading(true)
    setError(null)
    setErrorStep(null)
    try {
      const response = await getSampleResume()
      setResumeId(response.resume_id)
      setJobDescription('Senior ML Engineer with 3+ years experience. Required: Python, PyTorch, FastAPI, NLP, Docker, AWS. Preferred: React, PostgreSQL.')
      setCurrentStep(1)
    } catch (error) {
      console.error('Sample data error:', error)
      setError('Failed to load sample data')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #03050A 0%, #0F182C 100%)', padding: '60px 20px', animation: 'fadeIn 0.4s ease-out' }}>
      {/* Skip to content link */}
      <a
        href="#main-content"
        style={{
          position: 'absolute',
          left: '-9999px',
          zIndex: 999,
          padding: '1em',
          background: '#6B6BFF',
          color: '#fff',
          textDecoration: 'none',
          borderRadius: '4px',
          fontWeight: '600'
        }}
        onFocus={(e) => {
          e.target.style.left = '10px'
          e.target.style.top = '10px'
        }}
        onBlur={(e) => {
          e.target.style.left = '-9999px'
        }}
      >
        Skip to main content
      </a>

      {/* Navigation */}
      <button
        onClick={onNavigateHome}
        style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          background: 'rgba(107, 107, 255, 0.3)',
          color: '#EDF2FF',
          padding: '14px 24px',
          borderRadius: '8px',
          fontWeight: '700',
          fontSize: '16px',
          border: '2px solid rgba(107, 107, 255, 0.5)',
          cursor: 'pointer',
          minWidth: '44px',
          minHeight: '44px'
        }}
      >
        <span style={{ fontSize: '18px' }}>←</span>
        <span>Back to Home</span>
      </button>
      
      <span 
        style={{ 
          position: 'absolute',
          top: '32px',
          right: '20px',
          zIndex: 1000,
          color: '#EDF2FF', 
          fontSize: '18px', 
          fontWeight: '700' 
        }}
      >
        Pipeline Dashboard
      </span>

      {/* Main content */}
      <div id="main-content" style={{ maxWidth: '1400px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <h1 style={{ fontSize: '48px', fontWeight: '800', color: '#EDF2FF', marginBottom: '16px', letterSpacing: '-0.03em' }}>
            🚀 Agentic Career Copilot Pipeline
          </h1>
          <p style={{ fontSize: '18px', color: '#7A8CAA' }}>
            Complete 12-step architecture from resume upload to application generation
          </p>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.05)', backdropFilter: 'blur(10px)', borderRadius: '16px', padding: '32px', marginBottom: '32px', border: '1px solid rgba(255,255,255,0.1)' }}>
          <h2 style={{ fontSize: '24px', fontWeight: '700', color: '#EDF2FF', marginBottom: '24px' }}>Step 1: Input Layer</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
            <div>
              <label style={{ display: 'block', color: '#EDF2FF', fontWeight: '600', marginBottom: '8px' }}>
                Upload Resume (PDF/DOCX)
              </label>
              <input
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={handleResumeUpload}
                style={{ width: '100%', padding: '12px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px', color: '#EDF2FF' }}
              />
              {resumeFile && (
                <p style={{ marginTop: '8px', color: '#00E5B4' }}>✓ {resumeFile.name}</p>
              )}
            </div>

            <div>
              <label style={{ display: 'block', color: '#EDF2FF', fontWeight: '600', marginBottom: '8px' }}>
                Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste job description here..."
                style={{ width: '100%', padding: '12px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px', color: '#EDF2FF', minHeight: '120px', fontFamily: 'inherit' }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', gap: '16px', marginTop: '24px', flexWrap: 'wrap' }}>
            <button
              onClick={runFullPipeline}
              disabled={loading}
              style={{ flex: '1', background: 'linear-gradient(135deg, #6B6BFF 0%, #FF5C6B 100%)', color: '#fff', padding: '16px 32px', borderRadius: '8px', fontWeight: '700', fontSize: '16px', border: 'none', cursor: loading ? 'not-allowed' : 'pointer', opacity: loading ? 0.6 : 1 }}
            >
              {loading ? '⏳ Processing...' : '🚀 Run Full Pipeline'}
            </button>
            <button
              onClick={useSampleData}
              disabled={loading}
              style={{ background: 'rgba(255,255,255,0.1)', color: '#EDF2FF', padding: '16px 24px', borderRadius: '8px', fontWeight: '600', border: '1px solid rgba(255,255,255,0.2)', cursor: loading ? 'not-allowed' : 'pointer', opacity: loading ? 0.6 : 1 }}
            >
              Use Sample Data
            </button>
          </div>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.05)', backdropFilter: 'blur(10px)', borderRadius: '16px', padding: '32px', marginBottom: '32px', border: '1px solid rgba(255,255,255,0.1)' }}>
          <h2 style={{ fontSize: '24px', fontWeight: '700', color: '#EDF2FF', marginBottom: '24px' }}>Pipeline Progress</h2>
          
          <div className="step-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '16px' }}>
            {steps.map((step, index) => (
              <StepCard
                key={step.id}
                step={step}
                index={index}
                currentStep={currentStep}
                loading={loading}
                error={error}
                onRetry={index === errorStep ? handleRetry : null}
              />
            ))}
          </div>

          <ProgressBar 
            currentStep={currentStep} 
            totalSteps={steps.length} 
            isLoading={loading} 
          />
        </div>

        {pipelineData && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <ResultCard title="Step 4: Semantic Matching" icon="🎯">
              <div style={{ textAlign: 'center', marginBottom: '24px' }}>
                <div style={{ fontSize: '64px', fontWeight: '800', background: 'linear-gradient(135deg, #00E5B4 0%, #6B6BFF 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                  {pipelineData.step_4_matching.overall_score}%
                </div>
                <div style={{ color: '#7A8CAA', marginTop: '8px' }}>Overall Match Score</div>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '16px' }}>
                {pipelineData.step_4_matching.dimensions.map((dim, i) => (
                  <div key={i} style={{ background: 'rgba(255,255,255,0.05)', padding: '16px', borderRadius: '8px' }}>
                    <div style={{ color: '#EDF2FF', fontWeight: '600', fontSize: '13px', marginBottom: '8px' }}>{dim.name}</div>
                    <div style={{ fontSize: '24px', fontWeight: '700', color: '#6B6BFF' }}>{dim.score}%</div>
                  </div>
                ))}
              </div>
            </ResultCard>

            {pipelineData.step_5_explainability && (
              <ResultCard title="Step 5: Explainability (SHAP + DiCE)" icon="💡">
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
                  <div>
                    <h4 style={{ color: '#00E5B4', fontWeight: '600', marginBottom: '12px' }}>✅ Why You Matched</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      {pipelineData.step_5_explainability.shap_analysis.positive_features.slice(0, 5).map((f, i) => (
                        <div key={i} style={{ background: 'rgba(0,229,180,0.1)', padding: '12px', borderRadius: '8px' }}>
                          <div style={{ color: '#EDF2FF', fontWeight: '600' }}>{f.feature}</div>
                          <div style={{ color: '#00E5B4', fontSize: '12px' }}>{f.reason}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 style={{ color: '#FF5C6B', fontWeight: '600', marginBottom: '12px' }}>❌ Why You Didn't Match</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      {pipelineData.step_5_explainability.shap_analysis.negative_features.slice(0, 5).map((f, i) => (
                        <div key={i} style={{ background: 'rgba(255,92,107,0.1)', padding: '12px', borderRadius: '8px' }}>
                          <div style={{ color: '#EDF2FF', fontWeight: '600' }}>{f.feature}</div>
                          <div style={{ color: '#FF5C6B', fontSize: '12px' }}>{f.reason}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </ResultCard>
            )}

            {pipelineData.step_8_recruiter_sim && (
              <ResultCard title="Step 8: Recruiter Simulation" icon="👔">
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px' }}>
                  <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '12px' }}>
                    <h4 style={{ color: '#EDF2FF', fontWeight: '600', marginBottom: '16px' }}>🤖 ATS Screening</h4>
                    <div style={{ fontSize: '36px', fontWeight: '800', marginBottom: '8px', color: pipelineData.step_8_recruiter_sim.ats.passed_ats ? '#00E5B4' : '#FF5C6B' }}>
                      {pipelineData.step_8_recruiter_sim.ats.passed_ats ? '✅ PASSED' : '❌ FILTERED'}
                    </div>
                    <div style={{ color: '#7A8CAA' }}>
                      Keyword Match: {pipelineData.step_8_recruiter_sim.ats.keyword_match_rate}%
                    </div>
                  </div>

                  <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '12px' }}>
                    <h4 style={{ color: '#EDF2FF', fontWeight: '600', marginBottom: '16px' }}>👔 Recruiter Decision</h4>
                    <div style={{ fontSize: '36px', fontWeight: '800', marginBottom: '8px', color: pipelineData.step_8_recruiter_sim.recruiter.decision === 'ACCEPT' ? '#00E5B4' : pipelineData.step_8_recruiter_sim.recruiter.decision === 'MAYBE' ? '#FFB547' : '#FF5C6B' }}>
                      {pipelineData.step_8_recruiter_sim.recruiter.decision}
                    </div>
                    <div style={{ color: '#7A8CAA' }}>
                      Interview Likelihood: {pipelineData.step_8_recruiter_sim.recruiter.interview_likelihood}%
                    </div>
                  </div>
                </div>
              </ResultCard>
            )}
          </div>
        )}
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.8; transform: scale(1.05); }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @media (prefers-reduced-motion: reduce) {
          * {
            animation: none !important;
            transition: none !important;
          }
        }

        @media (max-width: 767px) {
          .step-grid {
            grid-template-columns: repeat(2, 1fr) !important;
          }
          .nav-container {
            top: 12px !important;
            left: 12px !important;
            right: 12px !important;
            width: calc(100vw - 24px) !important;
            padding: 12px 16px !important;
            flex-wrap: nowrap !important;
          }
          .nav-container button {
            padding: 10px 16px !important;
            font-size: 14px !important;
          }
          .nav-container nav {
            font-size: 14px !important;
          }
        }

        @media (min-width: 768px) and (max-width: 1023px) {
          .step-grid {
            grid-template-columns: repeat(4, 1fr) !important;
          }
        }

        @media (min-width: 1024px) {
          .step-grid {
            grid-template-columns: repeat(6, 1fr) !important;
          }
        }
      `}</style>
    </div>
  )
}

const ResultCard = ({ title, icon, children }) => (
  <div style={{ background: 'rgba(255,255,255,0.05)', backdropFilter: 'blur(10px)', borderRadius: '16px', padding: '32px', border: '1px solid rgba(255,255,255,0.1)' }}>
    <h3 style={{ fontSize: '24px', fontWeight: '700', color: '#EDF2FF', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
      <span style={{ fontSize: '36px' }}>{icon}</span>
      {title}
    </h3>
    {children}
  </div>
)

export default PipelineDashboard
