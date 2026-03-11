import React from 'react';
import ArchitectureDiagram from '../components/ArchitectureDiagram';
import { Network } from 'lucide-react';

const Architecture = () => {
  return (
    <div className="min-h-screen bg-dark-primary pt-16">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Network size={32} className="text-accent-blue" />
            <h1 className="text-3xl font-bold">System Architecture</h1>
          </div>
          <p className="text-gray-400">Visual representation of your application architecture</p>
        </div>
        
        <div className="bg-dark-secondary border border-dark-border rounded-xl overflow-hidden">
          <ArchitectureDiagram />
        </div>
        
        {/* Architecture Details */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-dark-secondary border border-dark-border rounded-xl p-6">
            <h3 className="text-xl font-semibold mb-4">Technology Stack</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Frontend:</span>
                <span className="font-medium">React + Tailwind CSS</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Backend:</span>
                <span className="font-medium">Node.js / Python</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Database:</span>
                <span className="font-medium">PostgreSQL / MongoDB</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">API:</span>
                <span className="font-medium">REST / GraphQL</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Deployment:</span>
                <span className="font-medium">Docker / Kubernetes</span>
              </div>
            </div>
          </div>
          
          <div className="bg-dark-secondary border border-dark-border rounded-xl p-6">
            <h3 className="text-xl font-semibold mb-4">Performance Metrics</h3>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-400">Response Time</span>
                  <span className="font-medium">45ms</span>
                </div>
                <div className="w-full bg-dark-tertiary rounded-full h-2">
                  <div className="bg-accent-green h-2 rounded-full" style={{ width: '90%' }} />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-400">Throughput</span>
                  <span className="font-medium">1.2K req/s</span>
                </div>
                <div className="w-full bg-dark-tertiary rounded-full h-2">
                  <div className="bg-accent-blue h-2 rounded-full" style={{ width: '75%' }} />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-400">Error Rate</span>
                  <span className="font-medium">0.1%</span>
                </div>
                <div className="w-full bg-dark-tertiary rounded-full h-2">
                  <div className="bg-accent-green h-2 rounded-full" style={{ width: '95%' }} />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-400">Uptime</span>
                  <span className="font-medium">99.9%</span>
                </div>
                <div className="w-full bg-dark-tertiary rounded-full h-2">
                  <div className="bg-accent-green h-2 rounded-full" style={{ width: '99%' }} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Architecture;
