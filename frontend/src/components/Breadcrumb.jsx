const Breadcrumb = ({ items, separator = '/' }) => {
  return (
    <nav 
      aria-label="Breadcrumb" 
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        fontSize: '18px',
        whiteSpace: 'nowrap',
        marginTop: 0
      }}
    >
      {items.map((item, index) => (
        <span 
          key={index} 
          style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            gap: '8px'
          }}
        >
          {item.onClick ? (
            <button
              onClick={item.onClick}
              style={{
                background: 'none',
                border: 'none',
                color: '#B8C5E0',
                cursor: 'pointer',
                textDecoration: 'underline',
                padding: 0,
                fontSize: '18px',
                fontFamily: 'inherit',
                transition: 'color 0.2s ease',
                fontWeight: '600'
              }}
              onMouseEnter={(e) => e.target.style.color = '#EDF2FF'}
              onMouseLeave={(e) => e.target.style.color = '#B8C5E0'}
            >
              {item.label}
            </button>
          ) : (
            <span 
              style={{ 
                color: index === items.length - 1 ? '#EDF2FF' : '#B8C5E0',
                fontWeight: index === items.length - 1 ? '700' : '600',
                textShadow: '0 2px 8px rgba(0, 0, 0, 0.3)'
              }}
            >
              {item.label}
            </span>
          )}
          {index < items.length - 1 && (
            <span style={{ color: '#B8C5E0', fontWeight: '400' }}>{separator}</span>
          )}
        </span>
      ))}
    </nav>
  )
}

export default Breadcrumb
