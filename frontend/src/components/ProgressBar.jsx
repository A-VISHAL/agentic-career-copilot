const ProgressBar = ({ currentStep, totalSteps, isLoading }) => {
  const percentage = Math.round((currentStep / totalSteps) * 100)

  return (
    <div style={{ marginTop: '24px' }}>
      <div 
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          marginBottom: '8px'
        }}
      >
        <span 
          style={{ 
            color: '#EDF2FF', 
            fontSize: '14px', 
            fontWeight: '600' 
          }}
        >
          Pipeline Progress
        </span>
        <span 
          style={{ 
            color: '#6B6BFF', 
            fontSize: '14px', 
            fontWeight: '700' 
          }}
        >
          {percentage}%
        </span>
      </div>
      <div 
        role="progressbar"
        aria-valuenow={percentage}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label="Pipeline completion progress"
        style={{
          width: '100%',
          height: '8px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '4px',
          overflow: 'hidden'
        }}
      >
        <div 
          style={{
            width: `${percentage}%`,
            height: '100%',
            background: 'linear-gradient(90deg, #6B6BFF 0%, #00E5B4 100%)',
            transition: 'width 0.5s ease-out',
            animation: isLoading ? 'shimmer 2s infinite' : 'none',
            backgroundSize: '200% 100%'
          }} 
        />
      </div>
      <style>{`
        @keyframes shimmer {
          0% {
            background-position: -200% 0;
          }
          100% {
            background-position: 200% 0;
          }
        }
      `}</style>
    </div>
  )
}

export default ProgressBar
