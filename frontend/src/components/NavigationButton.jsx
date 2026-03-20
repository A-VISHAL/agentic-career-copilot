import { useState } from 'react'

const NavigationButton = ({ onClick, label, icon, ariaLabel, className = '' }) => {
  const [isHovered, setIsHovered] = useState(false)
  const [isFocused, setIsFocused] = useState(false)

  const buttonStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    background: isHovered ? 'rgba(107, 107, 255, 0.4)' : 'rgba(107, 107, 255, 0.25)',
    backdropFilter: 'blur(10px)',
    color: '#EDF2FF',
    padding: '14px 24px',
    borderRadius: '8px',
    fontWeight: '700',
    fontSize: '16px',
    border: isFocused ? '2px solid #6B6BFF' : '2px solid rgba(107, 107, 255, 0.5)',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    outline: 'none',
    minWidth: '44px',
    minHeight: '44px',
    boxShadow: isHovered ? '0 4px 16px rgba(107, 107, 255, 0.4)' : '0 2px 12px rgba(107, 107, 255, 0.2)',
    textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)'
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
      <span style={{ fontSize: '18px', fontWeight: 'bold' }}>{icon}</span>
      <span>{label}</span>
    </button>
  )
}

export default NavigationButton
