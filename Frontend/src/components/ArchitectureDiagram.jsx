import React from 'react';
import { Database, Server, Globe, Zap, ArrowRight } from 'lucide-react';

const ArchitectureDiagram = () => {
  const components = [
    {
      id: 1,
      name: 'Frontend',
      icon: Globe,
      color: 'from-blue-500 to-blue-600',
      description: 'React + Tailwind',
      connections: [2]
    },
    {
      id: 2,
      name: 'API Gateway',
      icon: Zap,
      color: 'from-purple-500 to-purple-600',
      description: 'REST API',
      connections: [3, 4]
    },
    {
      id: 3,
      name: 'Backend Services',
      icon: Server,
      color: 'from-green-500 to-green-600',
      description: 'Node.js / Python',
      connections: [4]
    },
    {
      id: 4,
      name: 'Database',
      icon: Database,
      color: 'from-red-500 to-red-600',
      description: 'PostgreSQL / MongoDB',
      connections: []
    }
  ];
  
  return (
    <div className="relative p-8">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {components.map((component, index) => {
          const Icon = component.icon;
          return (
            <div key={component.id} className="relative">
              <div className="bg-dark-secondary border border-dark-border rounded-xl p-6 hover:border-accent-blue transition-all duration-300 group">
                <div className={`w-16 h-16 bg-gradient-to-br ${component.color} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon size={32} className="text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{component.name}</h3>
                <p className="text-sm text-gray-400">{component.description}</p>
              </div>
              
              {/* Connection arrows */}
              {component.connections.length > 0 && (
                <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                  <ArrowRight size={24} className="text-accent-blue" />
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      {/* Additional info */}
      <div className="mt-12 p-6 bg-dark-secondary border border-dark-border rounded-xl">
        <h4 className="text-lg font-semibold mb-4">System Flow</h4>
        <div className="space-y-2 text-sm text-gray-400">
          <p>1. Frontend sends user requests to the API Gateway</p>
          <p>2. API Gateway routes requests to appropriate Backend Services</p>
          <p>3. Backend Services process logic and interact with Database</p>
          <p>4. Data flows back through the same path to the Frontend</p>
        </div>
      </div>
    </div>
  );
};

export default ArchitectureDiagram;
