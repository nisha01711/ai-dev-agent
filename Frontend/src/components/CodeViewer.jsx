import React, { useState } from 'react';
import { Copy, Check, FileCode } from 'lucide-react';

const CodeViewer = ({ code, language = 'javascript', fileName = 'index.js' }) => {
  const [copied, setCopied] = useState(false);
  
  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  return (
    <div className="glass border border-white/10 rounded-2xl overflow-hidden shadow-lg">
      <div className="flex items-center justify-between px-5 py-4 bg-dark-tertiary/50 border-b border-white/10 backdrop-blur-xl">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-br from-accent-blue to-accent-purple rounded-lg flex items-center justify-center">
            <FileCode size={16} className="text-white" />
          </div>
          <span className="font-bold">{fileName}</span>
          <span className="text-xs px-3 py-1 bg-accent-blue/20 text-accent-blue rounded-full font-medium">{language}</span>
        </div>
        <button
          onClick={handleCopy}
          className="p-2.5 hover:bg-white/10 rounded-lg transition-colors group"
        >
          {copied ? (
            <Check size={16} className="text-accent-green" />
          ) : (
            <Copy size={16} className="text-gray-400 group-hover:text-white" />
          )}
        </button>
      </div>
      <div className="p-6 overflow-x-auto bg-black/30">
        <pre className="text-sm font-mono leading-relaxed">
          <code className="text-gray-300">{code}</code>
        </pre>
      </div>
    </div>
  );
};

export default CodeViewer;
