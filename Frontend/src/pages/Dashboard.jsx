import React, { useState } from 'react';
import TaskInput from '../components/TaskInput';
import CodeViewer from '../components/CodeViewer';
import TerminalOutput from '../components/TerminalOutput';
import StepProgress from '../components/StepProgress';
import LoadingSpinner from '../components/LoadingSpinner';
import { Lightbulb, CheckCircle2, AlertCircle } from 'lucide-react';

const Dashboard = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [hasGenerated, setHasGenerated] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  
  const planningSteps = [
    {
      title: 'Setup Backend Environment',
      description: 'Initialize Node.js project with Express framework'
    },
    {
      title: 'Create Database Schema',
      description: 'Design and implement MongoDB collections'
    },
    {
      title: 'Implement API Endpoints',
      description: 'Create REST API routes for CRUD operations'
    },
    {
      title: 'Add Authentication',
      description: 'Implement JWT-based authentication system'
    }
  ];
  
  const sampleCode = `// Student Management API - Express.js
import express from 'express';
import mongoose from 'mongoose';

const app = express();
app.use(express.json());

// Student Schema
const studentSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  age: { type: Number, required: true },
  course: { type: String, required: true },
  enrollmentDate: { type: Date, default: Date.now }
});

const Student = mongoose.model('Student', studentSchema);

// Routes
app.get('/api/students', async (req, res) => {
  try {
    const students = await Student.find();
    res.json(students);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/students', async (req, res) => {
  try {
    const student = new Student(req.body);
    await student.save();
    res.status(201).json(student);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});`;

  const sampleLogs = [
    { type: 'info', message: '> Starting development server...', timestamp: '12:00:01' },
    { type: 'success', message: '✓ Server initialized successfully', timestamp: '12:00:02' },
    { type: 'info', message: '> Connecting to MongoDB...', timestamp: '12:00:03' },
    { type: 'success', message: '✓ Database connected', timestamp: '12:00:04' },
    { type: 'info', message: '> Server running on http://localhost:3000', timestamp: '12:00:05' },
  ];
  
  const debugSuggestions = [
    {
      type: 'warning',
      title: 'Missing Error Validation',
      description: 'Add input validation for student data to prevent invalid entries.',
      suggestion: 'Use express-validator or Joi for request validation'
    },
    {
      type: 'info',
      title: 'Performance Optimization',
      description: 'Consider adding indexes to frequently queried fields like email.',
      suggestion: 'Add studentSchema.index({ email: 1 }) for better query performance'
    }
  ];
  
  const handleTaskSubmit = (task) => {
    setIsGenerating(true);
    setHasGenerated(false);
    setCurrentStep(0);
    
    // Simulate AI processing
    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev >= planningSteps.length - 1) {
          clearInterval(stepInterval);
          setTimeout(() => {
            setIsGenerating(false);
            setHasGenerated(true);
          }, 500);
          return prev;
        }
        return prev + 1;
      });
    }, 1500);
  };
  
  return (
    <div className="min-h-screen bg-dark-primary pt-16">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8 animate-fadeInUp">
          <h1 className="text-4xl font-black mb-3 gradient-text" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>AI Development Dashboard</h1>
          <p className="text-gray-400 text-lg">Describe your software task and let AI handle the rest</p>
        </div>
        
        {/* Task Input */}
        <div className="mb-8">
          <TaskInput onSubmit={handleTaskSubmit} isLoading={isGenerating} />
        </div>
        
        {isGenerating && (
          <LoadingSpinner message="AI is analyzing your task and generating a plan..." />
        )}
        
        {(isGenerating || hasGenerated) && (
          <div className="space-y-8">
            {/* Section 1: AI Planning Output */}
            <section className="glass border border-white/10 rounded-2xl p-8 card-hover animate-fadeInUp">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-gradient-to-br from-accent-blue to-accent-purple rounded-xl flex items-center justify-center">
                  <Lightbulb size={22} className="text-white" />
                </div>
                <h2 className="text-2xl font-bold">AI Planning Output</h2>
              </div>
              <StepProgress steps={planningSteps} currentStep={currentStep} />
            </section>
            
            {hasGenerated && (
              <>
                {/* Section 2: Generated Code Viewer */}
                <section className="animate-fadeInUp" style={{ animationDelay: '0.1s' }}>
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 bg-gradient-to-br from-accent-green to-accent-blue rounded-xl flex items-center justify-center">
                      <CheckCircle2 size={22} className="text-white" />
                    </div>
                    <h2 className="text-2xl font-bold">Generated Code</h2>
                  </div>
                  <div className="space-y-4">
                    <CodeViewer 
                      code={sampleCode} 
                      language="javascript" 
                      fileName="server.js"
                    />
                    
                    {/* Additional code files tabs */}
                    <div className="flex gap-3 overflow-x-auto pb-2">
                      <button className="px-5 py-2.5 bg-gradient-to-r from-accent-blue to-accent-purple rounded-xl text-sm font-bold shadow-lg shadow-accent-blue/30">
                        server.js
                      </button>
                      <button className="px-5 py-2.5 glass border border-white/10 rounded-xl text-sm font-medium hover:border-accent-blue/50 transition-all">
                        models/Student.js
                      </button>
                      <button className="px-5 py-2.5 glass border border-white/10 rounded-xl text-sm font-medium hover:border-accent-blue/50 transition-all">
                        routes/students.js
                      </button>
                      <button className="px-5 py-2.5 glass border border-white/10 rounded-xl text-sm font-medium hover:border-accent-blue/50 transition-all">
                        config/database.js
                      </button>
                    </div>
                  </div>
                </section>
                
                {/* Section 3: Execution Logs */}
                <section className="animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 bg-gradient-to-br from-accent-green to-accent-blue rounded-xl flex items-center justify-center">
                      <AlertCircle size={22} className="text-white" />
                    </div>
                    <h2 className="text-2xl font-bold">Execution Logs</h2>
                  </div>
                  <TerminalOutput logs={sampleLogs} />
                </section>
                
                {/* Section 4: Debug Suggestions */}
                <section className="animate-fadeInUp" style={{ animationDelay: '0.3s' }}>
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 bg-gradient-to-br from-accent-purple to-pink-500 rounded-xl flex items-center justify-center">
                      <AlertCircle size={22} className="text-white" />
                    </div>
                    <h2 className="text-2xl font-bold">Debug Suggestions</h2>
                  </div>
                  <div className="space-y-4">
                    {debugSuggestions.map((suggestion, index) => (
                      <div 
                        key={index}
                        className="glass border border-white/10 rounded-2xl p-6 hover:border-accent-blue transition-all card-hover"
                      >
                        <div className="flex items-start gap-4">
                          <div className={`w-3 h-3 rounded-full mt-2 flex-shrink-0 shadow-lg ${
                            suggestion.type === 'warning' ? 'bg-yellow-500 shadow-yellow-500/50' : 'bg-accent-blue shadow-accent-blue/50'
                          } animate-pulse`} />
                          <div className="flex-1">
                            <h3 className="text-lg font-bold mb-3">{suggestion.title}</h3>
                            <p className="text-gray-400 mb-4 leading-relaxed">{suggestion.description}</p>
                            <div className="glass border border-accent-blue/30 rounded-xl p-4">
                              <p className="text-sm text-accent-blue font-medium">💡 {suggestion.suggestion}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </section>
              </>
            )}
          </div>
        )}
        
        {!isGenerating && !hasGenerated && (
          <div className="text-center py-20">
            <div className="w-24 h-24 bg-gradient-to-br from-accent-blue to-accent-purple rounded-full flex items-center justify-center mx-auto mb-6 opacity-20">
              <Lightbulb size={48} />
            </div>
            <h3 className="text-xl font-semibold mb-2">Ready to Start Building</h3>
            <p className="text-gray-400">Enter your software task above to begin</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
