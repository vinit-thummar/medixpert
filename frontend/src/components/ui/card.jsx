import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../lib/utils';

const Card = React.forwardRef(({ 
  className, 
  children, 
  hover = false, 
  gradient = false,
  ...props 
}, ref) => (
  <motion.div
    ref={ref}
    className={cn(
      'rounded-xl border bg-card text-card-foreground shadow-sm',
      gradient && 'bg-gradient-to-br from-white to-gray-50',
      hover && 'transition-all duration-200 hover:shadow-lg hover:scale-[1.02]',
      className
    )}
    whileHover={hover ? { y: -2 } : undefined}
    {...props}
  >
    {children}
  </motion.div>
));
Card.displayName = 'Card';

const CardHeader = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col space-y-1.5 p-6', className)}
    {...props}
  />
));
CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn('text-2xl font-semibold leading-none tracking-tight', className)}
    {...props}
  />
));
CardTitle.displayName = 'CardTitle';

const CardDescription = React.forwardRef(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn('text-sm text-muted-foreground', className)}
    {...props}
  />
));
CardDescription.displayName = 'CardDescription';

const CardContent = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
));
CardContent.displayName = 'CardContent';

const CardFooter = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex items-center p-6 pt-0', className)}
    {...props}
  />
));
CardFooter.displayName = 'CardFooter';

const StatsCard = ({ 
  title, 
  value, 
  change, 
  changeType = 'positive', 
  icon: Icon,
  gradient = 'blue'
}) => {
  const gradients = {
    blue: 'from-blue-500 to-cyan-500',
    purple: 'from-purple-500 to-pink-500',
    green: 'from-green-500 to-emerald-500',
    orange: 'from-orange-500 to-red-500'
  };

  return (
    <Card hover gradient className="overflow-hidden">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p className="text-2xl font-bold text-gray-900">{value}</p>
            {change && (
              <p className={cn(
                'text-sm font-medium mt-1',
                changeType === 'positive' ? 'text-green-600' : 'text-red-600'
              )}>
                {change}
              </p>
            )}
          </div>
          {Icon && (
            <div className={cn(
              'w-12 h-12 rounded-lg flex items-center justify-center bg-gradient-to-r',
              gradients[gradient]
            )}>
              <Icon className="w-6 h-6 text-white" />
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export { 
  Card, 
  CardHeader, 
  CardFooter, 
  CardTitle, 
  CardDescription, 
  CardContent,
  StatsCard 
};

