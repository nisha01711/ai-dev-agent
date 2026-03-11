import React from 'react';
import { CheckCircle2 } from 'lucide-react';

const StepProgress = ({ steps, currentStep }) => {
  return (
    <div className="space-y-6">
      {steps.map((step, index) => {
        const isCompleted = index < currentStep;
        const isCurrent = index === currentStep;
        const isPending = index > currentStep;
        
        return (
          <div key={index} className="flex items-start gap-4 group">
            <div className={`
              relative flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center border-2 transition-all duration-300
              ${isCompleted ? 'bg-gradient-to-br from-accent-green to-accent-blue border-accent-green shadow-lg shadow-accent-green/30' : ''}
              ${isCurrent ? 'border-accent-blue bg-gradient-to-br from-accent-blue/20 to-accent-purple/20 shadow-lg shadow-accent-blue/30 animate-pulse' : ''}
              ${isPending ? 'border-white/20 bg-dark-tertiary' : ''}
            `}>
              {isCompleted ? (
                <CheckCircle2 size={20} className="text-white" />
              ) : (
                <span className={`text-sm font-bold ${isCurrent ? 'text-accent-blue' : 'text-gray-500'}`}>
                  {index + 1}
                </span>
              )}
              {isCurrent && (
                <div className="absolute inset-0 rounded-xl bg-accent-blue/20 animate-ping" />
              )}
            </div>
            
            <div className="flex-1 pt-1.5">
              <h4 className={`font-bold mb-2 text-lg transition-colors ${
                isCompleted || isCurrent ? 'text-white' : 'text-gray-500'
              }`}>
                {step.title}
              </h4>
              {step.description && (
                <p className="text-sm text-gray-400 leading-relaxed">{step.description}</p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default StepProgress;
