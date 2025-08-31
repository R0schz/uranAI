export const LogoIcon = () => (
  <svg style={{ display: 'none' }}>
    <defs>
      <symbol id="logo-icon" viewBox="0 0 100 100">
        <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{ stopColor: '#c850c0' }} />
          <stop offset="100%" style={{ stopColor: '#4158d0' }} />
        </linearGradient>
        <filter id="iconGlow">
          <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        <path d="M 50 5 A 45 45 0 1 0 50 95 A 35 35 0 1 1 50 5 Z" fill="url(#logoGrad)"></path>
        <path d="M 60 25 L 70 45 L 55 55 L 75 70" stroke="white" strokeWidth="1.5" fill="none" strokeLinecap="round" filter="url(#iconGlow)"></path>
        <circle cx="60" cy="25" r="3.5" fill="white" filter="url(#iconGlow)"></circle>
        <circle cx="70" cy="45" r="2.5" fill="white" filter="url(#iconGlow)"></circle>
        <circle cx="55" cy="55" r="2" fill="white" filter="url(#iconGlow)"></circle>
        <circle cx="75" cy="70" r="3" fill="white" filter="url(#iconGlow)"></circle>
      </symbol>
    </defs>
  </svg>
);
