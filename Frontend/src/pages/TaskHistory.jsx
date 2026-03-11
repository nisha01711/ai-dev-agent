import React, { useState } from 'react';
import { History, Search, ExternalLink, CheckCircle2, Clock, XCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const TaskHistory = () => {
  const [searchQuery, setSearchQuery] = useState('');
  
  const tasks = [
    {
      id: 1,
      name: 'Build REST API for Student Management',
      status: 'completed',
      date: '2024-03-10',
      time: '14:30',
      duration: '5 mins',
      linesOfCode: 245
    },
    {
      id: 2,
      name: 'Create E-commerce Shopping Cart',
      status: 'completed',
      date: '2024-03-09',
      time: '10:15',
      duration: '8 mins',
      linesOfCode: 512
    },
    {
      id: 3,
      name: 'Implement User Authentication System',
      status: 'in-progress',
      date: '2024-03-10',
      time: '16:45',
      duration: '3 mins',
      linesOfCode: 180
    },
    {
      id: 4,
      name: 'Build Real-time Chat Application',
      status: 'completed',
      date: '2024-03-08',
      time: '09:00',
      duration: '12 mins',
      linesOfCode: 678
    },
    {
      id: 5,
      name: 'Create Dashboard Analytics',
      status: 'failed',
      date: '2024-03-07',
      time: '15:20',
      duration: '2 mins',
      linesOfCode: 0
    },
    {
      id: 6,
      name: 'Develop Payment Gateway Integration',
      status: 'completed',
      date: '2024-03-06',
      time: '11:30',
      duration: '7 mins',
      linesOfCode: 423
    }
  ];
  
  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return (
          <span className="flex items-center gap-1 px-3 py-1 bg-accent-green/20 text-accent-green rounded-full text-sm">
            <CheckCircle2 size={14} />
            Completed
          </span>
        );
      case 'in-progress':
        return (
          <span className="flex items-center gap-1 px-3 py-1 bg-accent-blue/20 text-accent-blue rounded-full text-sm">
            <Clock size={14} />
            In Progress
          </span>
        );
      case 'failed':
        return (
          <span className="flex items-center gap-1 px-3 py-1 bg-accent-red/20 text-accent-red rounded-full text-sm">
            <XCircle size={14} />
            Failed
          </span>
        );
      default:
        return null;
    }
  };
  
  const filteredTasks = tasks.filter(task =>
    task.name.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  return (
    <div className="min-h-screen bg-dark-primary pt-16">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <History size={32} className="text-accent-purple" />
            <h1 className="text-3xl font-bold">Task History</h1>
          </div>
          <p className="text-gray-400">View and manage your previous AI-generated tasks</p>
        </div>
        
        {/* Search and Filters */}
        <div className="mb-6 flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search size={20} className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" />
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-dark-secondary border border-dark-border rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-accent-blue"
            />
          </div>
          <div className="flex gap-2">
            <select className="px-4 py-3 bg-dark-secondary border border-dark-border rounded-xl text-white focus:outline-none focus:border-accent-blue">
              <option>All Status</option>
              <option>Completed</option>
              <option>In Progress</option>
              <option>Failed</option>
            </select>
            <select className="px-4 py-3 bg-dark-secondary border border-dark-border rounded-xl text-white focus:outline-none focus:border-accent-blue">
              <option>Last 7 Days</option>
              <option>Last 30 Days</option>
              <option>Last 90 Days</option>
              <option>All Time</option>
            </select>
          </div>
        </div>
        
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-dark-secondary border border-dark-border rounded-xl p-4">
            <p className="text-gray-400 text-sm mb-1">Total Tasks</p>
            <p className="text-2xl font-bold">{tasks.length}</p>
          </div>
          <div className="bg-dark-secondary border border-dark-border rounded-xl p-4">
            <p className="text-gray-400 text-sm mb-1">Completed</p>
            <p className="text-2xl font-bold text-accent-green">
              {tasks.filter(t => t.status === 'completed').length}
            </p>
          </div>
          <div className="bg-dark-secondary border border-dark-border rounded-xl p-4">
            <p className="text-gray-400 text-sm mb-1">In Progress</p>
            <p className="text-2xl font-bold text-accent-blue">
              {tasks.filter(t => t.status === 'in-progress').length}
            </p>
          </div>
          <div className="bg-dark-secondary border border-dark-border rounded-xl p-4">
            <p className="text-gray-400 text-sm mb-1">Lines of Code</p>
            <p className="text-2xl font-bold">
              {tasks.reduce((sum, t) => sum + t.linesOfCode, 0).toLocaleString()}
            </p>
          </div>
        </div>
        
        {/* Tasks Table */}
        <div className="bg-dark-secondary border border-dark-border rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-dark-tertiary border-b border-dark-border">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Task Name</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Status</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Date</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Duration</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Lines</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredTasks.map((task) => (
                  <tr key={task.id} className="border-b border-dark-border hover:bg-dark-tertiary transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-medium">{task.name}</div>
                    </td>
                    <td className="px-6 py-4">
                      {getStatusBadge(task.status)}
                    </td>
                    <td className="px-6 py-4 text-gray-400">
                      <div>{task.date}</div>
                      <div className="text-sm">{task.time}</div>
                    </td>
                    <td className="px-6 py-4 text-gray-400">{task.duration}</td>
                    <td className="px-6 py-4 text-gray-400">{task.linesOfCode}</td>
                    <td className="px-6 py-4">
                      <Link
                        to="/dashboard"
                        className="inline-flex items-center gap-2 px-4 py-2 bg-accent-blue hover:bg-accent-blue/80 rounded-lg transition-colors text-sm font-medium"
                      >
                        <ExternalLink size={14} />
                        Open
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
        {filteredTasks.length === 0 && (
          <div className="text-center py-12 text-gray-400">
            No tasks found matching your search.
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskHistory;
