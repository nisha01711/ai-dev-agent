import React from 'react';
import { Terminal, AlertCircle, CheckCircle, Info } from 'lucide-react';

const TerminalOutput = ({ logs = [] }) => {
  const getIcon = (type) => {
    switch (type) {
      case 'error':
        return <AlertCircle size={14} className="text-accent-red" />;
      case 'success':
        return <CheckCircle size={14} className="text-accent-green" />;
      case 'info':
        return <Info size={14} className="text-accent-blue" />;
      default:
        return null;
    }
  };
  
  const getTextColor = (type) => {
    switch (type) {
      case 'error':
        return 'text-accent-red';
      case 'success':
        return 'text-accent-green';
      case 'info':
        return 'text-accent-blue';
      default:
        return 'text-gray-300';
    }
  };
  
  return (
    <div className="glass border border-white/10 rounded-2xl overflow-hidden shadow-lg">
      <div className="flex items-center gap-3 px-5 py-4 bg-dark-tertiary/50 border-b border-white/10 backdrop-blur-xl">
        <div className="w-8 h-8 bg-gradient-to-br from-accent-green to-accent-blue rounded-lg flex items-center justify-center">
          <Terminal size={16} className="text-white" />
        </div>
        <span className="font-bold">Execution Logs</span>
        <div className="ml-auto flex items-center gap-2">
          <div className="flex gap-2">
            <div className="w-3 h-3 rounded-full bg-accent-red shadow-lg shadow-accent-red/50" />
            <div className="w-3 h-3 rounded-full bg-yellow-500 shadow-lg shadow-yellow-500/50" />
            <div className="w-3 h-3 rounded-full bg-accent-green shadow-lg shadow-accent-green/50 animate-pulse" />
          </div>
        </div>
      </div>
      <div className="p-6 bg-black/50 font-mono text-sm h-64 overflow-y-auto backdrop-blur-sm">
        {logs.length === 0 ? (
          <div className="text-gray-500 italic flex items-center gap-2">
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse" />
            Waiting for execution...
          </div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className={`flex items-start gap-3 mb-3 ${getTextColor(log.type)} animate-fadeInUp`}>
              {getIcon(log.type)}
              <span className="flex-1 leading-relaxed">{log.message}</span>
              {log.timestamp && (
                <span className="text-xs text-gray-600 font-medium">{log.timestamp}</span>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TerminalOutput;
