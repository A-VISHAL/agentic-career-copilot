import { useState } from 'react'
import { uploadResume, getSampleResume } from '../utils/api'

const API_BASE = 'http://localhost:8000'

const PipelineDashboard = () => {
  const [loading, setLoading] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [pipelineData, setPipelineData] = useState(null)
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [resumeId, setResumeId] = useState(null)

  const steps = [
    { id: 1, name: 'Upload Resume', icon: '📄', status: 'pending' },
    { id: 2, name: 'Resume Parsing', icon: '🔍', status: 'pending' },
    { id: 3, name: 'JD Parsing', icon: '📋', status: 'pending' },
    { id: 4, name: 'Semantic Matching', icon: '🎯', status: 'pending' },
    { id: 5, name: 'Explainability (SHAP+DiCE)', icon: '💡', status: 'pending' },
    { id: 6, name: 'Skill Gap Analysis', icon: '📊', status: 'pending' },
    { id: 7, name: 'Resume Optimization', icon: '✨', status: 'pending' },
    { id: 8, name: 'Recruiter Simulation', icon: '👔', status: 'pending' },
    { id: 9, name: 'Application Generation', icon: '📝', status: 'pending' },
    { id: 10, name: 'Agentic Workflow', icon: '🤖', status: 'pending' },
    { id: 11, name: 'Database Storage', icon: '💾', status: 'pending' },
    { id: 12, name: 'Visualization', icon: '📈', status: 'pending' }
  ]

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setResumeFile(file)
    setLoading(true)
    setCurrentStep(1)

    try {
      const response = await uploadResume(file)
      setResumeId(response.resume_id)
      setCurrentStep(2)
    } catch (error) {
      console.error('Upload error:', error)
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

    try {
      // Use sample if no resume uploaded
      let currentResumeId = resumeId
      if (!currentResumeId) {
        const sampleResponse = await getSampleResume()
        currentResumeId = sampleResponse.resume_id
        setResumeId(currentResumeId)
      }

      // Run full pipeline
      const formData = new FormData()
      formData.append('resume_id', currentResumeId)
      formData.append('job_description', jobDescription || 'Senior ML Engineer with Python, PyTorch, and FastAPI experience. 3+ years required.')

      // Simulate step-by-step progress
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
      alert('Pipeline execution failed')
    } finally {
      setLoading(false)
    }
  }

  const useSampleData = async () => {
    setLoading(true)
    try {
      const response = await getSampleResume()
      setResumeId(response.resume_id)
      setJobDescription('Senior ML Engineer with 3+ years experience. Required: Python, PyTorch, FastAPI, NLP, Docker, AWS. Preferred: React, PostgreSQL.')
      setCurrentStep(1)
    } catch (error) {
      console.error('Sample data error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            🚀 Agentic Career Copilot Pipeline
          </h1>
          <p className="text-xl text-gray-300">
            Complete 12-step architecture from resume upload to application generation
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-8 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-6">Step 1: Input Layer</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            {/* Resume Upload */}
            <div>
              <label className="block text-white font-semibold mb-2">
                Upload Resume (PDF/DOCX)
              </label>
              <input
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={handleResumeUpload}
                className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-purple-600 file:text-white hover:file:bg-purple-700"
              />
              {resumeFile && (
                <p className="mt-2 text-green-400">✓ {resumeFile.name}</p>
              )}
            </div>

            {/* Job Description */}
            <div>
              <label className="block text-white font-semibold mb-2">
                Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste job description here..."
                className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg text-white placeholder-gray-400 h-32"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4 mt-6">
            <button
              onClick={runFullPipeline}
              disabled={loading}
              className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {loading ? '⏳ Processing...' : '🚀 Run Full Pipeline'}
            </button>
            <button
              onClick={useSampleData}
              disabled={loading}
              className="bg-white/20 text-white px-6 py-4 rounded-lg font-semibold hover:bg-white/30 disabled:opacity-50 transition-all"
            >
              Use Sample Data
            </button>
          </div>
        </div>

        {/* Pipeline Steps Visualization */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-8 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-6">Pipeline Progress</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className={`p-4 rounded-lg text-center transition-all ${
                  index < currentStep
                    ? 'bg-green-500/30 border-2 border-green-400'
                    : index === currentStep
                    ? 'bg-purple-500/30 border-2 border-purple-400 animate-pulse'
                    : 'bg-white/10 border border-white/20'
                }`}
              >
                <div className="text-4xl mb-2">{step.icon}</div>
                <div className="text-white text-sm font-semibold">{step.name}</div>
                {index < currentStep && (
                  <div className="text-green-400 text-xs mt-1">✓ Complete</div>
                )}
                {index === currentStep && loading && (
                  <div className="text-purple-400 text-xs mt-1">⏳ Processing</div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Results Display */}
        {pipelineData && (
          <div className="space-y-6">
            {/* Step 4: Match Score */}
            <ResultCard
              title="Step 4: Semantic Matching"
              icon="🎯"
              data={pipelineData.step_4_matching}
            >
              <div className="text-center mb-6">
                <div className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500">
                  {pipelineData.step_4_matching.overall_score}%
                </div>
                <div className="text-gray-300 mt-2">Overall Match Score</div>
              </div>
              <div className="grid md:grid-cols-5 gap-4">
                {pipelineData.step_4_matching.dimensions.map((dim, i) => (
                  <div key={i} className="bg-white/10 p-4 rounded-lg">
                    <div className="text-white font-semibold text-sm mb-2">{dim.name}</div>
                    <div className="text-2xl font-bold text-purple-400">{dim.score}%</div>
                  </div>
                ))}
              </div>
            </ResultCard>

            {/* Step 5: Explainability */}
            <ResultCard
              title="Step 5: Explainability (SHAP + DiCE)"
              icon="💡"
              data={pipelineData.step_5_explainability}
            >
              <div className="grid md:grid-cols-2 gap-6">
                {/* Positive Features */}
                <div>
                  <h4 className="text-green-400 font-semibold mb-3">✅ Why You Matched</h4>
                  <div className="space-y-2">
                    {pipelineData.step_5_explainability.shap_analysis.positive_features.slice(0, 5).map((f, i) => (
                      <div key={i} className="bg-green-500/20 p-3 rounded-lg">
                        <div className="text-white font-semibold">{f.feature}</div>
                        <div className="text-green-300 text-sm">{f.reason}</div>
                        <div className="text-green-400 text-xs mt-1">Impact: +{(f.shap_value * 100).toFixed(1)}%</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Negative Features */}
                <div>
                  <h4 className="text-red-400 font-semibold mb-3">❌ Why You Didn't Match</h4>
                  <div className="space-y-2">
                    {pipelineData.step_5_explainability.shap_analysis.negative_features.slice(0, 5).map((f, i) => (
                      <div key={i} className="bg-red-500/20 p-3 rounded-lg">
                        <div className="text-white font-semibold">{f.feature}</div>
                        <div className="text-red-300 text-sm">{f.reason}</div>
                        <div className="text-red-400 text-xs mt-1">Impact: {(f.shap_value * 100).toFixed(1)}%</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Counterfactuals */}
              <div className="mt-6">
                <h4 className="text-purple-400 font-semibold mb-3">🔮 Counterfactual Suggestions</h4>
                <div className="space-y-3">
                  {pipelineData.step_5_explainability.counterfactuals.slice(0, 3).map((cf, i) => (
                    <div key={i} className="bg-purple-500/20 p-4 rounded-lg border border-purple-400/30">
                      <div className="flex justify-between items-start mb-2">
                        <div className="text-white font-semibold">{cf.change}</div>
                        <div className="text-purple-400 font-bold">
                          {cf.current_score}% → {cf.projected_score}%
                        </div>
                      </div>
                      <div className="text-gray-300 text-sm mb-2">{cf.timeline}</div>
                      <ul className="text-gray-400 text-sm space-y-1">
                        {cf.action_items.map((item, j) => (
                          <li key={j}>• {item}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </ResultCard>

            {/* Step 6: Skill Gap */}
            <ResultCard
              title="Step 6: Skill Gap Analysis"
              icon="📊"
              data={pipelineData.step_6_skill_gap}
            >
              <div className="grid md:grid-cols-3 gap-6">
                <div className="bg-green-500/20 p-4 rounded-lg">
                  <div className="text-green-400 font-semibold mb-2">Matched Skills</div>
                  <div className="text-3xl font-bold text-white mb-2">{pipelineData.step_6_skill_gap.matched.length}</div>
                  <div className="flex flex-wrap gap-2">
                    {pipelineData.step_6_skill_gap.matched.slice(0, 8).map((skill, i) => (
                      <span key={i} className="bg-green-500/30 px-2 py-1 rounded text-xs text-green-300">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="bg-red-500/20 p-4 rounded-lg">
                  <div className="text-red-400 font-semibold mb-2">Missing Skills</div>
                  <div className="text-3xl font-bold text-white mb-2">{pipelineData.step_6_skill_gap.missing.length}</div>
                  <div className="flex flex-wrap gap-2">
                    {pipelineData.step_6_skill_gap.missing.slice(0, 8).map((skill, i) => (
                      <span key={i} className="bg-red-500/30 px-2 py-1 rounded text-xs text-red-300">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="bg-purple-500/20 p-4 rounded-lg">
                  <div className="text-purple-400 font-semibold mb-2">Priority to Learn</div>
                  <div className="text-3xl font-bold text-white mb-2">{pipelineData.step_6_skill_gap.priority.length}</div>
                  <div className="flex flex-wrap gap-2">
                    {pipelineData.step_6_skill_gap.priority.map((skill, i) => (
                      <span key={i} className="bg-purple-500/30 px-2 py-1 rounded text-xs text-purple-300">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </ResultCard>

            {/* Step 8: Recruiter Simulation */}
            <ResultCard
              title="Step 8: Recruiter Simulation"
              icon="👔"
              data={pipelineData.step_8_recruiter_sim}
            >
              <div className="grid md:grid-cols-2 gap-6">
                {/* ATS Screening */}
                <div className="bg-white/10 p-6 rounded-lg">
                  <h4 className="text-white font-semibold mb-4">🤖 ATS Screening</h4>
                  <div className={`text-4xl font-bold mb-2 ${
                    pipelineData.step_8_recruiter_sim.ats.passed_ats ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {pipelineData.step_8_recruiter_sim.ats.passed_ats ? '✅ PASSED' : '❌ FILTERED'}
                  </div>
                  <div className="text-gray-300">
                    Keyword Match: {pipelineData.step_8_recruiter_sim.ats.keyword_match_rate}%
                  </div>
                </div>

                {/* Recruiter Decision */}
                <div className="bg-white/10 p-6 rounded-lg">
                  <h4 className="text-white font-semibold mb-4">👔 Recruiter Decision</h4>
                  <div className={`text-4xl font-bold mb-2 ${
                    pipelineData.step_8_recruiter_sim.recruiter.decision === 'ACCEPT' ? 'text-green-400' :
                    pipelineData.step_8_recruiter_sim.recruiter.decision === 'MAYBE' ? 'text-yellow-400' :
                    'text-red-400'
                  }`}>
                    {pipelineData.step_8_recruiter_sim.recruiter.decision}
                  </div>
                  <div className="text-gray-300">
                    Interview Likelihood: {pipelineData.step_8_recruiter_sim.recruiter.interview_likelihood}%
                  </div>
                </div>
              </div>

              <div className="mt-6 space-y-4">
                {pipelineData.step_8_recruiter_sim.recruiter.feedback.map((fb, i) => (
                  <div key={i} className="bg-white/10 p-4 rounded-lg text-gray-300">
                    {fb}
                  </div>
                ))}
              </div>
            </ResultCard>

            {/* Step 10: Agentic Workflow */}
            <ResultCard
              title="Step 10: Agentic Workflow"
              icon="🤖"
              data={pipelineData.step_10_agentic}
            >
              <div className="grid md:grid-cols-3 gap-6 mb-6">
                <div className="bg-blue-500/20 p-4 rounded-lg text-center">
                  <div className="text-blue-400 font-semibold mb-2">Applications Tracked</div>
                  <div className="text-4xl font-bold text-white">
                    {pipelineData.step_10_agentic.tracking.total_applications}
                  </div>
                </div>
                <div className="bg-green-500/20 p-4 rounded-lg text-center">
                  <div className="text-green-400 font-semibold mb-2">Response Rate</div>
                  <div className="text-4xl font-bold text-white">
                    {pipelineData.step_10_agentic.tracking.metrics.response_rate}%
                  </div>
                </div>
                <div className="bg-purple-500/20 p-4 rounded-lg text-center">
                  <div className="text-purple-400 font-semibold mb-2">Interview Rate</div>
                  <div className="text-4xl font-bold text-white">
                    {pipelineData.step_10_agentic.tracking.metrics.interview_rate}%
                  </div>
                </div>
              </div>

              {/* Applications Timeline */}
              <div className="space-y-3">
                <h4 className="text-white font-semibold mb-3">📋 Application Timeline</h4>
                {pipelineData.step_10_agentic.tracking.applications.map((app, i) => (
                  <div key={i} className="bg-white/10 p-4 rounded-lg flex justify-between items-center">
                    <div>
                      <div className="text-white font-semibold">{app.company} - {app.role}</div>
                      <div className="text-gray-400 text-sm">{app.notes}</div>
                    </div>
                    <div className="text-right">
                      <div className={`font-semibold ${
                        app.status === 'interview_scheduled' ? 'text-green-400' :
                        app.status === 'rejected' ? 'text-red-400' :
                        'text-yellow-400'
                      }`}>
                        {app.status.replace('_', ' ').toUpperCase()}
                      </div>
                      <div className="text-gray-400 text-sm">Match: {app.match_score}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </ResultCard>
          </div>
        )}
      </div>
    </div>
  )
}

// Helper component for result cards
const ResultCard = ({ title, icon, children }) => (
  <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
    <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
      <span className="text-4xl">{icon}</span>
      {title}
    </h3>
    {children}
  </div>
)

export default PipelineDashboard
