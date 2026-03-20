const Breadcrumb = ({ items, separator = '/' }) => {
  return (
    <nav 
      aria-label="Breadcrumb" 
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        fontSize: '14px',
        marginTop: '12px'
      }}
    >
      {items.map((item, index) => (
        <div 
          key={index} 
          style={{ 
            display: 'flex', 
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
                color: '#7A8CAA',
                cursor: 'pointer',
                textDecoration: 'underline',
                padding: 0,
                fontSize: '14px',
                fontFamily: 'inherit',
                transition: 'color 0.2s ease'
              }}
              onMouseEnter={(e) => e.target.style.color = '#EDF2FF'}
              onMouseLeave={(e) => e.target.style.color = '#7A8CAA'}
            >
              {item.label}
            </button>
          ) : (
            <span 
              style={{ 
                color: index === items.length - 1 ? '#EDF2FF' : '#7A8CAA' 
              }}
            >
              {item.label}
            </span>
          )}
          {index < items.length - 1 && (
            <span style={{ color: '#7A8CAA' }}>{separator}</span>
          )}
        </div>
      ))}
    </nav>
  )
}

export default Breadcrumb
