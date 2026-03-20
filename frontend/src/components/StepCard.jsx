import { memo } from 'react'

const StepCard = memo(({ step, index, currentStep, loading, error, onRetry }) => {
  const isComplete = index < currentStep
  const isActive = index === currentStep
  const isPending = index > currentStep
  const hasError = error && index === currentStep

  const getBackgroundColor = () => {
    if (hasError) return 'rgba(255,92,107,0.2)'
    if (isComplete) return 'rgba(0,229,180,0.2)'
    if (isActive) return 'rgba(107,107,255,0.2)'
    return 'rgba(255,255,255,0.05)'
  }

  const getBorderColor = () => {
    if (hasError) return '2px solid #FF5C6B'
    if (isComplete) return '2px solid #00E5B4'
    if (isActive) return '2px solid #6B6BFF'
    return '1px solid rgba(255,255,255,0.1)'
  }

  const getStatus = () => {
    if (hasError) return 'Error'
    if (isComplete) return 'Complete'
    if (isActive) return 'In Progress'
    return 'Pending'
  }

  return (
    <div
      role="status"
      aria-label={`Step ${index + 1}: ${step.name} - ${getStatus()}`}
      aria-live="polite"
      aria-atomic="true"
      style={{
        padding: '16px',
        borderRadius: '12px',
        textAlign: 'center',
        background: getBackgroundColor(),
        border: getBorderColor(),
        opacity: isPending ? 0.5 : 1,
        animation: isActive && loading ? 'pulse 1.5s ease-in-out infinite' : 'none',
        transition: 'all 0.3s ease'
      }}
    >
      <div style={{ fontSize: '32px', marginBottom: '8px' }}>
        {hasError ? '❌' : step.icon}
      </div>
      <div style={{ color: '#EDF2FF', fontSize: '12px', fontWeight: '600' }}>
        {step.name}
      </div>
      {isComplete && (
        <div style={{ color: '#00E5B4', fontSize: '10px', marginTop: '4px' }}>
          ✓ Complete
        </div>
      )}
      {isActive && loading && (
        <div style={{ color: '#6B6BFF', fontSize: '10px', marginTop: '4px' }}>
          ⏳ Processing
        </div>
      )}
      {hasError && onRetry && (
        <button
          onClick={onRetry}
          style={{
            marginTop: '8px',
            padding: '4px 8px',
            background: '#FF5C6B',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            fontSize: '10px',
            cursor: 'pointer',
            fontWeight: '600',
            transition: 'opacity 0.2s ease'
          }}
          onMouseEnter={(e) => e.target.style.opacity = '0.8'}
          onMouseLeave={(e) => e.target.style.opacity = '1'}
        >
          Retry
        </button>
      )}
    </div>
  )
}, (prevProps, nextProps) => {
  return prevProps.currentStep === nextProps.currentStep &&
         prevProps.loading === nextProps.loading &&
         prevProps.error === nextProps.error
})

StepCard.displayName = 'StepCard'

export default StepCard
