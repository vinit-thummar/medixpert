import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../../lib/utils';
import { AlertCircle, CheckCircle } from 'lucide-react';

const FormField = ({ 
  label, 
  error, 
  success, 
  required, 
  children, 
  className,
  ...props 
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn('space-y-2', className)}
      {...props}
    >
      {label && (
        <label className="text-sm font-medium text-gray-700 block">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      
      <div className="relative">
        {children}
        
        {/* Success/Error Icons */}
        <AnimatePresence>
          {(error || success) && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="absolute right-3 top-1/2 transform -translate-y-1/2"
            >
              {error && <AlertCircle className="w-5 h-5 text-red-500" />}
              {success && <CheckCircle className="w-5 h-5 text-green-500" />}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Error/Success Messages */}
      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="text-sm text-red-600 flex items-center gap-1"
          >
            <AlertCircle className="w-4 h-4" />
            {error}
          </motion.p>
        )}
        {success && (
          <motion.p
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="text-sm text-green-600 flex items-center gap-1"
          >
            <CheckCircle className="w-4 h-4" />
            {success}
          </motion.p>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

const FormInput = React.forwardRef(({ 
  className, 
  error, 
  success, 
  ...props 
}, ref) => {
  return (
    <input
      ref={ref}
      className={cn(
        'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200',
        error && 'border-red-500 focus-visible:ring-red-500',
        success && 'border-green-500 focus-visible:ring-green-500',
        className
      )}
      {...props}
    />
  );
});
FormInput.displayName = 'FormInput';

const FormTextarea = React.forwardRef(({ 
  className, 
  error, 
  success, 
  ...props 
}, ref) => {
  return (
    <textarea
      ref={ref}
      className={cn(
        'flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200',
        error && 'border-red-500 focus-visible:ring-red-500',
        success && 'border-green-500 focus-visible:ring-green-500',
        className
      )}
      {...props}
    />
  );
});
FormTextarea.displayName = 'FormTextarea';

const FormSelect = React.forwardRef(({ 
  className, 
  error, 
  success, 
  children,
  ...props 
}, ref) => {
  return (
    <select
      ref={ref}
      className={cn(
        'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200',
        error && 'border-red-500 focus-visible:ring-red-500',
        success && 'border-green-500 focus-visible:ring-green-500',
        className
      )}
      {...props}
    >
      {children}
    </select>
  );
});
FormSelect.displayName = 'FormSelect';

const FormCheckbox = React.forwardRef(({ 
  className, 
  label,
  error,
  ...props 
}, ref) => {
  return (
    <div className="flex items-center space-x-2">
      <input
        ref={ref}
        type="checkbox"
        className={cn(
          'h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 transition-colors',
          error && 'border-red-500',
          className
        )}
        {...props}
      />
      {label && (
        <label className="text-sm text-gray-700">
          {label}
        </label>
      )}
    </div>
  );
});
FormCheckbox.displayName = 'FormCheckbox';

// Validation utilities
export const validators = {
  required: (value) => value ? null : 'This field is required',
  email: (value) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value) ? null : 'Please enter a valid email address';
  },
  minLength: (min) => (value) => 
    value && value.length >= min ? null : `Must be at least ${min} characters`,
  maxLength: (max) => (value) => 
    value && value.length <= max ? null : `Must be no more than ${max} characters`,
  password: (value) => {
    if (!value) return 'Password is required';
    if (value.length < 8) return 'Password must be at least 8 characters';
    if (!/(?=.*[a-z])/.test(value)) return 'Password must contain at least one lowercase letter';
    if (!/(?=.*[A-Z])/.test(value)) return 'Password must contain at least one uppercase letter';
    if (!/(?=.*\d)/.test(value)) return 'Password must contain at least one number';
    return null;
  },
  phone: (value) => {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(value) ? null : 'Please enter a valid phone number';
  }
};

export { 
  FormField, 
  FormInput, 
  FormTextarea, 
  FormSelect, 
  FormCheckbox 
};

