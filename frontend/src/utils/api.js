const API_BASE = 'http://localhost:8000';

async function apiCall(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...(options.headers || {}),
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      console.warn('Backend not available, using demo mode');
      return null;
    }
    throw error;
  }
}

// ─── RESUME ───

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  return apiCall('/api/resume/upload', {
    method: 'POST',
    body: formData,
  });
}

export async function getSampleResume() {
  return apiCall('/api/resume/sample');
}

// ─── MATCHING ───

export async function matchResume(resumeId, jobDescription) {
  const formData = new FormData();
  if (resumeId) formData.append('resume_id', resumeId);
  formData.append('job_description', jobDescription);
  
  return apiCall('/api/match', {
    method: 'POST',
    body: formData,
  });
}

// ─── RESUME IMPROVEMENT ───

export async function improveResume(resumeId, jobDescription) {
  const formData = new FormData();
  if (resumeId) formData.append('resume_id', resumeId);
  if (jobDescription) formData.append('job_description', jobDescription);
  
  return apiCall('/api/resume/improve', {
    method: 'POST',
    body: formData,
  });
}

// ─── COVER LETTER ───

export async function generateCoverLetter(resumeText, jobDescription, tone = 'professional') {
  return apiCall('/api/cover-letter', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
      tone,
    }),
  });
}

// ─── INTERVIEW ───

export async function getInterviewQuestions(jobDescription, numQuestions = 5) {
  const formData = new FormData();
  formData.append('job_description', jobDescription);
  formData.append('num_questions', numQuestions);
  
  return apiCall('/api/interview/questions', {
    method: 'POST',
    body: formData,
  });
}

export async function evaluateAnswer(question, answer, jobContext = '') {
  const formData = new FormData();
  formData.append('question', question);
  formData.append('answer', answer);
  formData.append('job_context', jobContext);
  
  return apiCall('/api/interview/evaluate', {
    method: 'POST',
    body: formData,
  });
}

// ─── ROADMAP ───

export async function getRoadmap(resumeId, jobDescription) {
  const formData = new FormData();
  if (resumeId) formData.append('resume_id', resumeId);
  formData.append('job_description', jobDescription);
  
  return apiCall('/api/roadmap', {
    method: 'POST',
    body: formData,
  });
}

// ─── JOBS ───

export async function searchJobs(query = '', category = 'all') {
  const params = new URLSearchParams({ query, category });
  return apiCall(`/api/jobs?${params}`);
}

export async function getSkillTrends() {
  return apiCall('/api/skills/trends');
}

// ─── CHAT ───

export async function chatWithCoach(messages, resumeContext = '', jobContext = '') {
  return apiCall('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages,
      resume_context: resumeContext,
      job_context: jobContext,
      mode: 'coach',
    }),
  });
}

// ─── HEALTH ───

export async function healthCheck() {
  return apiCall('/health');
}
