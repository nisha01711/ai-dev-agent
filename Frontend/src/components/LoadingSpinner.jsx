import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="relative">
        <div className="w-16 h-16 border-4 border-accent-blue/30 border-t-accent-blue rounded-full animate-spin" />
        <div className="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-accent-purple rounded-full animate-spin" style={{ animationDuration: '1s', animationDirection: 'reverse' }} />
      </div>
      <p className="text-gray-400 mt-6 text-lg font-medium animate-pulse">{message}</p>
    </div>
  );
};

export default LoadingSpinner;
