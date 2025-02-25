import React from 'react';

const Logo = ({ size = 'md', variant = 'default' }) => {
  const sizeClasses = {
    sm: 'h-6 w-6',
    md: 'h-8 w-8',
    lg: 'h-10 w-10',
    xl: 'h-12 w-12'
  };
  
  // 根据变体决定颜色
  const textColor = variant === 'default' ? 'text-white' : 'text-primary-700';
  
  // 白色主题
  const nutColor = variant === 'default' ? '#FFFFFF' : '#0369A1'; // 主体颜色
  const lineColor = variant === 'default' ? '#94A3B8' : '#0369A1'; // 线条颜色
  
  return (
    <div className="flex items-center">
      <div className={`${sizeClasses[size]} relative`}>
        <svg 
          className={textColor}
          viewBox="0 0 24 24" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* 榛子主体 - 简化形状 */}
          <path 
            d="M12 21C8 21 5 18 5 14V7L12 3L19 7V14C19 18 16 21 12 21Z" 
            fill={nutColor} 
            stroke={lineColor}
            strokeWidth="0.75"
            strokeLinejoin="round"
          />
          
          {/* 榛子纹理线条 */}
          <path 
            d="M8 9V14M12 7V18M16 9V14" 
            stroke={lineColor} 
            strokeWidth="1" 
            strokeLinecap="round"
          />
          
          {/* 顶部小尖 */}
          <path 
            d="M12 3L12 1.5" 
            stroke={lineColor} 
            strokeWidth="0.75" 
            strokeLinecap="round"
          />
        </svg>
      </div>
      <span className={`ml-2 font-bold text-lg ${textColor}`}>Hazel</span>
    </div>
  );
};

export default Logo; 