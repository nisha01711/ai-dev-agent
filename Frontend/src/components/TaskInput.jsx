import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

const TaskInput = ({ onSubmit, isLoading }) => {
  const [task, setTask] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (task.trim() && !isLoading) {
      onSubmit(task);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-accent-blue via-accent-purple to-pink-500 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
        <div className="relative">
          <textarea
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="Build a REST API for student management..."
            className="w-full px-6 py-5 glass border border-white/20 rounded-2xl text-white placeholder-gray-500 focus:outline-none focus:border-accent-blue resize-none text-lg backdrop-blur-xl"
            rows="4"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!task.trim() || isLoading}
            className="absolute bottom-5 right-5 px-8 py-3 bg-gradient-to-r from-accent-blue via-accent-purple to-pink-500 rounded-xl font-bold disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-accent-blue/30 transition-all flex items-center gap-2"
          >
            {isLoading ? (
              <>
                <Loader2 size={20} className="animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Send size={20} />
                <span>Generate Plan</span>
              </>
            )}
          </button>
        </div>
      </div>
    </form>
  );
};

export default TaskInput;
