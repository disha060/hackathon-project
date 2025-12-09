import React from 'react';

export const Card = ({ children, className = '', ...props }) => {
  const baseClasses = "rounded-lg border border-gray-200 bg-white shadow-sm";
  const combinedClasses = `${baseClasses} ${className}`;
  
  return (
    <div className={combinedClasses} {...props}>
      {children}
    </div>
  );
};

export const CardContent = ({ children, className = '', ...props }) => {
  const baseClasses = "p-6 pt-0";
  const combinedClasses = `${baseClasses} ${className}`;
  
  return (
    <div className={combinedClasses} {...props}>
      {children}
    </div>
  );
};