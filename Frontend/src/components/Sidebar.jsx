import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  History, 
  Settings, 
  PlusCircle, 
  Network,
  User,
  X
} from 'lucide-react';

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  const menuItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/architecture', icon: Network, label: 'Architecture' },
    { path: '/history', icon: History, label: 'Task History' },
    { path: '/profile', icon: User, label: 'Profile' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ];
  
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`
        fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 glass border-r border-white/10 backdrop-blur-xl
        transform transition-transform duration-300 z-40
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="flex flex-col h-full p-4">
          <button 
            onClick={onClose}
            className="lg:hidden absolute top-4 right-4 p-2 hover:bg-white/10 rounded-xl"
          >
            <X size={20} />
          </button>
          
          <Link
            to="/dashboard"
            className="flex items-center gap-3 px-5 py-4 mb-6 bg-gradient-to-r from-accent-blue via-accent-purple to-pink-500 rounded-xl hover:shadow-lg hover:shadow-accent-blue/30 transition-all font-bold group"
            onClick={onClose}
          >
            <PlusCircle size={20} className="group-hover:rotate-90 transition-transform duration-300" />
            <span>New Task</span>
          </Link>
          
          <nav className="flex-1 space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={onClose}
                  className={`flex items-center gap-3 px-5 py-3.5 rounded-xl transition-all font-medium group ${
                    isActive(item.path)
                      ? 'bg-gradient-to-r from-accent-blue/20 to-accent-purple/20 text-white border border-accent-blue/50'
                      : 'hover:bg-white/5 text-gray-400 hover:text-white'
                  }`}
                >
                  <Icon size={20} className={`${isActive(item.path) ? 'text-accent-blue' : 'group-hover:scale-110 transition-transform'}`} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
          
          <div className="pt-4 border-t border-white/10">
            <div className="px-5 py-4 glass rounded-xl border border-white/10">
              <p className="text-sm text-gray-400 mb-2">Status</p>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-accent-green rounded-full animate-pulse shadow-lg shadow-accent-green/50" />
                <span className="text-sm font-bold gradient-text">AI Ready</span>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
