import React from 'react';

const FeatureCard = ({ icon: Icon, title, description }) => {
  return (
    <div className="group relative p-6 bg-gradient-to-br from-dark-secondary via-dark-secondary to-dark-tertiary border border-dark-border rounded-2xl hover:border-accent-blue transition-all duration-500 card-hover overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-accent-blue/5 via-accent-purple/5 to-pink-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      
      {/* Glow effect */}
      <div className="absolute -inset-1 bg-gradient-to-r from-accent-blue via-accent-purple to-pink-500 rounded-2xl blur opacity-0 group-hover:opacity-20 transition duration-500" />
      
      <div className="relative">
        <div className="w-14 h-14 bg-gradient-to-br from-accent-blue via-accent-purple to-pink-500 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-6 transition-all duration-500 shadow-lg">
          <Icon size={26} className="text-white" />
        </div>
        <h3 className="text-xl font-bold mb-3 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-accent-blue group-hover:to-accent-purple transition-all duration-300">{title}</h3>
        <p className="text-gray-400 leading-relaxed">{description}</p>
      </div>
    </div>
  );
};

export default FeatureCard;
