import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles, Code2, Bug, Network } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';

const Landing = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'AI Task Planner',
      description: 'Intelligent planning system that breaks down complex software tasks into actionable steps.'
    },
    {
      icon: Code2,
      title: 'Code Generator',
      description: 'Generate production-ready code automatically based on your requirements and specifications.'
    },
    {
      icon: Bug,
      title: 'Debug Assistant',
      description: 'AI-powered debugging that identifies issues and suggests fixes in real-time.'
    },
    {
      icon: Network,
      title: 'Multi-Agent System',
      description: 'Coordinated AI agents working together to deliver complete software solutions.'
    }
  ];
  
  return (
    <div className="min-h-screen bg-dark-primary">
      {/* Hero Section */}
      <section className="relative overflow-hidden min-h-screen flex items-center">
        {/* Animated background gradients */}
        <div className="absolute inset-0 bg-gradient-to-br from-accent-blue/10 via-accent-purple/10 to-pink-500/10" />
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-accent-blue/20 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-purple/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
        
        <div className="relative max-w-7xl mx-auto px-6 py-20">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-5 py-2.5 glass rounded-full mb-8 border border-white/10 animate-fadeInUp">
              <Sparkles size={16} className="text-accent-blue animate-pulse" />
              <span className="text-sm font-medium bg-gradient-to-r from-accent-blue to-accent-purple bg-clip-text text-transparent">Powered by Advanced AI Technology</span>
            </div>
            
            <h1 className="text-6xl md:text-8xl font-black mb-8 leading-tight animate-fadeInUp" style={{ animationDelay: '0.1s', fontFamily: "'Space Grotesk', sans-serif" }}>
              <span className="gradient-text drop-shadow-2xl">AI Software Engineer</span>
            </h1>
            
            <p className="text-2xl md:text-3xl text-gray-300 mb-12 leading-relaxed animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
              Plan, Code, Debug, and Build Software <span className="text-accent-blue font-semibold">Automatically</span>
            </p>
            
            <div className="flex flex-col sm:flex-row items-center gap-4 justify-center animate-fadeInUp" style={{ animationDelay: '0.3s' }}>
              <Link
                to="/signup"
                className="group relative inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-accent-blue via-accent-purple to-pink-500 rounded-2xl text-lg font-bold hover:shadow-2xl hover:shadow-accent-blue/50 transition-all transform hover:scale-105 overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-pink-500 via-accent-purple to-accent-blue opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <span className="relative">Start Building</span>
                <ArrowRight size={22} className="relative group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                to="/login"
                className="group inline-flex items-center gap-3 px-10 py-5 glass border border-white/20 rounded-2xl text-lg font-bold hover:bg-white/10 transition-all hover:border-accent-blue/50"
              >
                <span>Sign In</span>
              </Link>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto animate-fadeInUp" style={{ animationDelay: '0.4s' }}>
              <div className="group text-center p-6 glass rounded-2xl border border-white/10 hover:border-accent-blue/50 transition-all card-hover">
                <div className="text-4xl font-black gradient-text mb-2">10K+</div>
                <div className="text-sm text-gray-400 font-medium">Tasks Completed</div>
              </div>
              <div className="group text-center p-6 glass rounded-2xl border border-white/10 hover:border-accent-purple/50 transition-all card-hover">
                <div className="text-4xl font-black gradient-text mb-2">50+</div>
                <div className="text-sm text-gray-400 font-medium">Languages</div>
              </div>
              <div className="group text-center p-6 glass rounded-2xl border border-white/10 hover:border-accent-green/50 transition-all card-hover">
                <div className="text-4xl font-black gradient-text mb-2">99.9%</div>
                <div className="text-sm text-gray-400 font-medium">Uptime</div>
              </div>
              <div className="group text-center p-6 glass rounded-2xl border border-white/10 hover:border-pink-500/50 transition-all card-hover">
                <div className="text-4xl font-black gradient-text mb-2">24/7</div>
                <div className="text-sm text-gray-400 font-medium">Available</div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      {/* Features Section */}
      <section className="py-32 px-6 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-accent-blue/5 to-transparent" />
        <div className="max-w-7xl mx-auto relative">
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-black mb-6" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              <span className="gradient-text">Powerful Features</span>
            </h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">Everything you need to build software with AI at lightning speed</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <FeatureCard
                key={index}
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
              />
            ))}
          </div>
        </div>
      </section>
      
      {/* How It Works Section */}
      <section className="py-32 px-6 bg-gradient-to-b from-dark-secondary via-dark-primary to-dark-secondary relative overflow-hidden">
        <div className="absolute top-0 left-1/2 w-96 h-96 bg-accent-purple/10 rounded-full blur-3xl -translate-x-1/2" />
        <div className="max-w-7xl mx-auto relative">
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-black mb-6" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              <span className="gradient-text">How It Works</span>
            </h2>
            <p className="text-xl text-gray-300">Simple steps to get started building with AI</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="group text-center relative">
              <div className="relative inline-flex items-center justify-center w-24 h-24 mb-8">
                <div className="absolute inset-0 bg-gradient-to-br from-accent-blue to-accent-purple rounded-2xl blur-xl opacity-50 group-hover:opacity-100 transition-opacity" />
                <div className="relative w-20 h-20 bg-gradient-to-br from-accent-blue to-accent-purple rounded-2xl flex items-center justify-center text-3xl font-black shadow-2xl group-hover:scale-110 transition-transform">
                  1
                </div>
              </div>
              <h3 className="text-2xl font-bold mb-4 group-hover:text-accent-blue transition-colors">Describe Your Task</h3>
              <p className="text-gray-400 text-lg leading-relaxed">Tell the AI what you want to build in natural language</p>
            </div>
            
            <div className="group text-center relative">
              <div className="relative inline-flex items-center justify-center w-24 h-24 mb-8">
                <div className="absolute inset-0 bg-gradient-to-br from-accent-purple to-pink-500 rounded-2xl blur-xl opacity-50 group-hover:opacity-100 transition-opacity" />
                <div className="relative w-20 h-20 bg-gradient-to-br from-accent-purple to-pink-500 rounded-2xl flex items-center justify-center text-3xl font-black shadow-2xl group-hover:scale-110 transition-transform">
                  2
                </div>
              </div>
              <h3 className="text-2xl font-bold mb-4 group-hover:text-accent-purple transition-colors">AI Plans & Codes</h3>
              <p className="text-gray-400 text-lg leading-relaxed">Watch as AI plans the architecture and generates code</p>
            </div>
            
            <div className="group text-center relative">
              <div className="relative inline-flex items-center justify-center w-24 h-24 mb-8">
                <div className="absolute inset-0 bg-gradient-to-br from-accent-green to-accent-blue rounded-2xl blur-xl opacity-50 group-hover:opacity-100 transition-opacity" />
                <div className="relative w-20 h-20 bg-gradient-to-br from-accent-green to-accent-blue rounded-2xl flex items-center justify-center text-3xl font-black shadow-2xl group-hover:scale-110 transition-transform">
                  3
                </div>
              </div>
              <h3 className="text-2xl font-bold mb-4 group-hover:text-accent-green transition-colors">Test & Debug</h3>
              <p className="text-gray-400 text-lg leading-relaxed">Automatic testing and AI-powered debugging for robust code</p>
            </div>
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="py-32 px-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-accent-blue/10 via-accent-purple/10 to-pink-500/10" />
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-accent-blue/20 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2 animate-pulse-slow" />
        
        <div className="max-w-5xl mx-auto text-center relative">
          <div className="glass p-12 md:p-20 rounded-3xl border border-white/10">
            <h2 className="text-5xl md:text-6xl font-black mb-8" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              <span className="gradient-text">Ready to Build Something Amazing?</span>
            </h2>
            <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto leading-relaxed">
              Join thousands of developers using AI to build software faster and smarter.
            </p>
            <div className="flex flex-col sm:flex-row items-center gap-6 justify-center">
              <Link
                to="/signup"
                className="group relative inline-flex items-center gap-3 px-12 py-6 bg-gradient-to-r from-accent-blue via-accent-purple to-pink-500 rounded-2xl text-xl font-black hover:shadow-2xl hover:shadow-accent-blue/50 transition-all transform hover:scale-105 overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-pink-500 via-accent-purple to-accent-blue opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                <span className="relative">Get Started Now</span>
                <ArrowRight size={24} className="relative group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                to="/login"
                className="inline-flex items-center gap-3 px-12 py-6 glass border border-white/20 rounded-2xl text-xl font-black hover:bg-white/10 transition-all hover:border-accent-blue/50"
              >
                <span>Sign In</span>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Landing;
