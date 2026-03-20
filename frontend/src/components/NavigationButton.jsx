import { useState } from 'react'

const NavigationButton = ({ onClick, label, icon, ariaLabel, className = '' }) => {
  const [isHovered, setIsHovered] = useState(false)
  const [isFocused, setIsFocused] = useState(false)

  const buttonStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    background: isHovered ? 'rgba(255,255,255,0.15)' : 'rgba(255,255,255,0.1)',
    backdropFilter: 'blur(10px)',
    color: '#EDF2FF',
    padding: '16px 24px',
    borderRadius: '8px',
    fontWeight: '600',
    fontSize: '14px',
    border: isFocused ? '2px solid #6B6BFF' : '1px solid rgba(255,255,255,0.2)',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    outline: 'none',
    minWidth: '44px',
    minHeight: '44px'
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      onClick()
    }
  }

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
      onKeyDown={handleKeyDown}
      style={buttonStyle}
      aria-label={ariaLabel}
      className={className}
      tabIndex={0}
    >
      <span style={{ fontSize: '16px' }}>{icon}</span>
      <span>{label}</span>
    </button>
  )
}

export default NavigationButton
