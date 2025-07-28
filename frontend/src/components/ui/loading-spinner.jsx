import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../lib/utils';

const LoadingSpinner = ({ size = 'md', className, ...props }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  };

  return (
    <motion.div
      className={cn(
        'inline-block border-2 border-current border-t-transparent rounded-full',
        sizeClasses[size],
        className
      )}
      animate={{ rotate: 360 }}
      transition={{
        duration: 1,
        repeat: Infinity,
        ease: 'linear'
      }}
      {...props}
    />
  );
};

const LoadingOverlay = ({ isLoading, children, message = 'Loading...' }) => {
  if (!isLoading) return children;

  return (
    <div className="relative">
      <div className="opacity-50 pointer-events-none">
        {children}
      </div>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="absolute inset-0 flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm"
      >
        <LoadingSpinner size="lg" className="text-blue-600 mb-4" />
        <p className="text-gray-600 font-medium">{message}</p>
      </motion.div>
    </div>
  );
};

const LoadingButton = ({ isLoading, children, disabled, className, ...props }) => {
  return (
    <button
      disabled={disabled || isLoading}
      className={cn(
        'relative inline-flex items-center justify-center',
        className
      )}
      {...props}
    >
      {isLoading && (
        <LoadingSpinner size="sm" className="absolute text-current" />
      )}
      <span className={isLoading ? 'opacity-0' : 'opacity-100'}>
        {children}
      </span>
    </button>
  );
};

export { LoadingSpinner, LoadingOverlay, LoadingButton };

