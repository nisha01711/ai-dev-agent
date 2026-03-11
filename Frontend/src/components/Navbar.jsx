import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, LayoutDashboard, Network, History, User, Settings, Menu } from 'lucide-react';

const Navbar = ({ onMenuClick }) => {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/10 backdrop-blur-xl">
      <div className="max-w-full px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-8">
            <button 
              onClick={onMenuClick}
              className="lg:hidden p-2 hover:bg-white/10 rounded-xl transition-colors"
            >
              <Menu size={24} />
            </button>
            <Link to="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 bg-gradient-to-br from-accent-blue via-accent-purple to-pink-500 rounded-xl flex items-center justify-center shadow-lg shadow-accent-blue/30 group-hover:shadow-accent-purple/50 transition-all group-hover:scale-110">
                <span className="text-xl font-black">AI</span>
              </div>
              <span className="text-xl font-black gradient-text" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>AI Dev Agent</span>
            </Link>
            
            <div className="hidden md:flex items-center gap-2">
              <Link 
                to="/" 
                className={`px-5 py-2.5 rounded-xl transition-all font-medium ${
                  isActive('/') 
                    ? 'bg-gradient-to-r from-accent-blue to-accent-purple text-white shadow-lg shadow-accent-blue/30' 
                    : 'hover:bg-white/5'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Home size={18} />
                  <span>Home</span>
                </div>
              </Link>
              <Link 
                to="/dashboard" 
                className={`px-5 py-2.5 rounded-xl transition-all font-medium ${
                  isActive('/dashboard') 
                    ? 'bg-gradient-to-r from-accent-blue to-accent-purple text-white shadow-lg shadow-accent-blue/30' 
                    : 'hover:bg-white/5'
                }`}
              >
                <div className="flex items-center gap-2">
                  <LayoutDashboard size={18} />
                  <span>Dashboard</span>
                </div>
              </Link>
              <Link 
                to="/architecture" 
                className={`px-5 py-2.5 rounded-xl transition-all font-medium ${
                  isActive('/architecture') 
                    ? 'bg-gradient-to-r from-accent-blue to-accent-purple text-white shadow-lg shadow-accent-blue/30' 
                    : 'hover:bg-white/5'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Network size={18} />
                  <span>Architecture</span>
                </div>
              </Link>
              <Link 
                to="/history" 
                className={`px-5 py-2.5 rounded-xl transition-all font-medium ${
                  isActive('/history') 
                    ? 'bg-gradient-to-r from-accent-blue to-accent-purple text-white shadow-lg shadow-accent-blue/30' 
                    : 'hover:bg-white/5'
                }`}
              >
                <div className="flex items-center gap-2">
                  <History size={18} />
                  <span>History</span>
                </div>
              </Link>
              <Link 
                to="/profile" 
                className={`px-5 py-2.5 rounded-xl transition-all font-medium ${
                  isActive('/profile') 
                    ? 'bg-gradient-to-r from-accent-blue to-accent-purple text-white shadow-lg shadow-accent-blue/30' 
                    : 'hover:bg-white/5'
                }`}
              >
                <div className="flex items-center gap-2">
                  <User size={18} />
                  <span>Profile</span>
                </div>
              </Link>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            {location.pathname === '/' && (
              <>
                <Link 
                  to="/login"
                  className="hidden sm:block px-5 py-2.5 hover:bg-white/5 rounded-xl transition-all font-medium"
                >
                  Sign In
                </Link>
                <Link 
                  to="/signup"
                  className="px-6 py-2.5 bg-gradient-to-r from-accent-blue via-accent-purple to-pink-500 rounded-xl transition-all hover:shadow-lg hover:shadow-accent-blue/30 font-bold"
                >
                  Get Started
                </Link>
              </>
            )}
            {location.pathname !== '/' && (
              <button className="p-2.5 hover:bg-white/5 rounded-xl transition-colors">
                <Settings size={20} />
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
